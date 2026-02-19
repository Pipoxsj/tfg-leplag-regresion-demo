"""
train_model.py
Script principal para entrenar el modelo de regresión múltiple.
Ejecutar desde la raíz del repo: python src/train_model.py
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from utils import load_data, prepare_features_target, split_data, build_preprocessor


def main():
    # 1. Cargar datos
    print("=" * 60)
    print("PASO 1: Cargando dataset...")
    print("=" * 60)
    data_path = 'data/dataset_complementario_regresion_anonimizado-2.csv'
    df = load_data(data_path)
    
    # 2. Preparar features y target
    print("\n" + "=" * 60)
    print("PASO 2: Preparando features y target...")
    print("=" * 60)
    X, y, numeric_features, categorical_features = prepare_features_target(df)
    
    # 3. Split train/test
    print("\n" + "=" * 60)
    print("PASO 3: División train/test (80/20)...")
    print("=" * 60)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)
    
    # 4. Construir preprocessor
    print("\n" + "=" * 60)
    print("PASO 4: Configurando preprocesamiento...")
    print("=" * 60)
    preprocessor = build_preprocessor(numeric_features, categorical_features)
    
    # 5. Entrenar modelo
    print("\n" + "=" * 60)
    print("PASO 5: Entrenando modelo de regresión lineal múltiple...")
    print("=" * 60)
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])
    model.fit(X_train, y_train)
    print("✓ Modelo entrenado exitosamente")
    
    # 6. Predicciones y evaluación
    print("\n" + "=" * 60)
    print("PASO 6: Evaluando modelo en test set...")
    print("=" * 60)
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n🎯 Métricas del modelo:")
    print(f"   MAE (Error Absoluto Medio):       {mae:,.2f} ARS")
    print(f"   RMSE (Raíz Error Cuadrático):     {rmse:,.2f} ARS")
    print(f"   R² (Coeficiente Determinación):   {r2:.4f}")
    
    # 7. Guardar métricas en JSON
    os.makedirs('outputs', exist_ok=True)
    metrics = {
        'MAE': round(mae, 2),
        'RMSE': round(rmse, 2),
        'R2': round(r2, 4)
    }
    with open('outputs/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    print("\n✓ Métricas guardadas en: outputs/metrics.json")
    
    # 8. Generar y guardar gráfico
    print("\n" + "=" * 60)
    print("PASO 7: Generando gráfico (valores reales vs predichos)...")
    print("=" * 60)
    plt.figure(figsize=(8, 8))
    plt.scatter(y_test, y_pred, alpha=0.4, edgecolors='k', linewidth=0.5)
    plt.xlabel('Monto real (ARS)', fontsize=12)
    plt.ylabel('Monto predicho (ARS)', fontsize=12)
    plt.title('Valores reales vs. predichos - Regresión múltiple', fontsize=14, fontweight='bold')
    
    # Línea diagonal de referencia
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Predicción perfecta')
    
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('outputs/plot.png', dpi=150)
    print("✓ Gráfico guardado en: outputs/plot.png")
    
    print("\n" + "=" * 60)
    print("🎉 Pipeline completado exitosamente")
    print("=" * 60)


if __name__ == '__main__':
    main()