"""
train_model_improved.py
Versión mejorada del pipeline analítico del TFG Leplag.

Mejoras principales:
- tratamiento de `tecnico_id` como variable categórica,
- imputación explícita para variables numéricas y categóricas,
- split agrupado por cliente cuando existe `id_cliente_anon`,
- comparación contra baseline DummyRegressor,
- guardado de artefactos adicionales: model_info.json y predictions_sample.csv.

Uso recomendado desde la raíz del repo:
    python src/train_model_improved.py
"""

from __future__ import annotations

import json
import os
from datetime import datetime

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from utils_improved import load_data, prepare_model_inputs, split_data, build_preprocessor

DATA_PATH = 'data/dataset_complementario_regresion_anonimizado-2.csv'
OUTPUT_DIR = 'outputs'
MODEL_PATH = os.path.join(OUTPUT_DIR, 'model.joblib')
METRICS_PATH = os.path.join(OUTPUT_DIR, 'metrics.json')
MODEL_INFO_PATH = os.path.join(OUTPUT_DIR, 'model_info.json')
PLOT_PATH = os.path.join(OUTPUT_DIR, 'plot.png')
PREDICTIONS_PATH = os.path.join(OUTPUT_DIR, 'predictions_sample.csv')

TEST_SIZE = 0.2
RANDOM_STATE = 42
TARGET_COL = 'monto_mensual_ars'


def compute_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return {
        'MAE': round(float(mae), 2),
        'RMSE': round(float(rmse), 2),
        'R2': round(float(r2), 4),
    }


def save_plot(y_test, y_pred):
    plt.figure(figsize=(8, 8))
    plt.scatter(y_test, y_pred, alpha=0.4, edgecolors='k', linewidth=0.5)
    plt.xlabel('Monto real (ARS)', fontsize=12)
    plt.ylabel('Monto predicho (ARS)', fontsize=12)
    plt.title('Valores reales vs. predichos - Regresión múltiple', fontsize=14, fontweight='bold')

    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Predicción perfecta')

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()
    print(f"✓ Gráfico guardado en: {PLOT_PATH}")


def save_predictions_sample(y_test, y_pred):
    pred_df = pd.DataFrame({
        'y_real': y_test.reset_index(drop=True),
        'y_pred': pd.Series(y_pred).reset_index(drop=True),
    })
    pred_df['error_absoluto'] = (pred_df['y_real'] - pred_df['y_pred']).abs()
    pred_df.to_csv(PREDICTIONS_PATH, index=False)
    print(f"✓ Predicciones guardadas en: {PREDICTIONS_PATH}")


def main():
    print('=' * 60)
    print('PASO 1: Cargando dataset...')
    print('=' * 60)
    df = load_data(DATA_PATH)

    print('\n' + '=' * 60)
    print('PASO 2: Preparando features, target y grupos...')
    print('=' * 60)
    X, y, numeric_features, categorical_features, groups = prepare_model_inputs(df, target_col=TARGET_COL)

    print('\n' + '=' * 60)
    print('PASO 3: División train/test...')
    print('=' * 60)
    X_train, X_test, y_train, y_test, groups_train, groups_test = split_data(
        X, y, groups=groups, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    print('\n' + '=' * 60)
    print('PASO 4: Configurando preprocesamiento...')
    print('=' * 60)
    preprocessor = build_preprocessor(numeric_features, categorical_features)

    print('\n' + '=' * 60)
    print('PASO 5: Baseline DummyRegressor...')
    print('=' * 60)
    dummy = DummyRegressor(strategy='mean')
    dummy.fit(X_train.select_dtypes(include=[np.number]), y_train)
    dummy_pred = dummy.predict(X_test.select_dtypes(include=[np.number]))
    baseline_metrics = compute_metrics(y_test, dummy_pred)
    print(f"✓ Baseline MAE: {baseline_metrics['MAE']}")
    print(f"✓ Baseline RMSE: {baseline_metrics['RMSE']}")
    print(f"✓ Baseline R2: {baseline_metrics['R2']}")

    print('\n' + '=' * 60)
    print('PASO 6: Entrenando modelo de regresión lineal múltiple...')
    print('=' * 60)
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    model.fit(X_train, y_train)
    print('✓ Modelo entrenado exitosamente')

    print('\n' + '=' * 60)
    print('PASO 7: Evaluando modelo en test set...')
    print('=' * 60)
    y_pred = model.predict(X_test)
    model_metrics = compute_metrics(y_test, y_pred)
    print(f"✓ MAE: {model_metrics['MAE']}")
    print(f"✓ RMSE: {model_metrics['RMSE']}")
    print(f"✓ R2: {model_metrics['R2']}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    metrics_payload = {
        'MAE': model_metrics['MAE'],
        'RMSE': model_metrics['RMSE'],
        'R2': model_metrics['R2'],
        'baseline': baseline_metrics,
    }
    with open(METRICS_PATH, 'w', encoding='utf-8') as f:
        json.dump(metrics_payload, f, indent=2, ensure_ascii=False)
    print(f"✓ Métricas guardadas en: {METRICS_PATH}")

    model_info = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'target': TARGET_COL,
        'n_total': int(len(df)),
        'n_train': int(len(X_train)),
        'n_test': int(len(X_test)),
        'test_size': TEST_SIZE,
        'random_state': RANDOM_STATE,
        'numeric_features': numeric_features,
        'categorical_features': categorical_features,
        'group_column_used': 'id_cliente_anon' if groups is not None else None,
        'model_name': 'LinearRegression',
        'baseline_name': 'DummyRegressor(mean)',
    }
    with open(MODEL_INFO_PATH, 'w', encoding='utf-8') as f:
        json.dump(model_info, f, indent=2, ensure_ascii=False)
    print(f"✓ Información del modelo guardada en: {MODEL_INFO_PATH}")

    joblib.dump(model, MODEL_PATH)
    print(f"✓ Modelo serializado en: {MODEL_PATH}")

    print('\n' + '=' * 60)
    print('PASO 8: Generando artefactos adicionales...')
    print('=' * 60)
    save_plot(y_test, y_pred)
    save_predictions_sample(y_test, y_pred)

    print('\n' + '=' * 60)
    print('🎉 Pipeline mejorado completado exitosamente')
    print('=' * 60)


if __name__ == '__main__':
    main()
