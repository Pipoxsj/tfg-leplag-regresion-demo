from pathlib import Path
import json

import pandas as pd
import streamlit as st
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = PROJECT_ROOT / 'outputs' / 'metrics.json'
MODEL_INFO_PATH = PROJECT_ROOT / 'outputs' / 'model_info.json'
PLOT_PATH = PROJECT_ROOT / 'outputs' / 'plot.png'
PREDICTIONS_PATH = PROJECT_ROOT / 'outputs' / 'predictions_sample.csv'
DATASET_PATH = PROJECT_ROOT / 'data' / 'dataset_complementario_regresion_anonimizado-2.csv'


def load_json(path):
    if not path.exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_predictions_sample():
    if not PREDICTIONS_PATH.exists():
        return None
    return pd.read_csv(PREDICTIONS_PATH)


def main():
    st.title('Analítica predictiva mejorada')
    st.write('Visualización extendida del componente analítico del prototipo Leplag.')

    metrics = load_json(METRICS_PATH)
    model_info = load_json(MODEL_INFO_PATH)
    predictions_df = load_predictions_sample()

    st.subheader('Estado de artefactos del modelo')
    st.write('Archivo de métricas encontrado:', METRICS_PATH.exists())
    st.write('Archivo de configuración/modelo encontrado:', MODEL_INFO_PATH.exists())
    st.write('Archivo de gráfico encontrado:', PLOT_PATH.exists())
    st.write('Archivo de predicciones encontrado:', PREDICTIONS_PATH.exists())
    st.write('Dataset anonimizado encontrado:', DATASET_PATH.exists())

    st.subheader('Descripción del modelo')
    st.write('Modelo base: regresión lineal múltiple para estimar `monto_mensual_ars` a partir de variables operativas y contextuales.')
    st.write('Esta vista integra artefactos generados por el pipeline mejorado y presenta la evidencia analítica de forma más trazable.')

    st.subheader('Configuración del experimento')
    if model_info is None:
        st.warning('No se encontró outputs/model_info.json. Ejecuta primero: python src/train_model_improved.py')
    else:
        st.write('Modelo:', model_info.get('model_name'))
        st.write('Baseline:', model_info.get('baseline_name'))
        st.write('Target:', model_info.get('target'))
        st.write('Muestras totales:', model_info.get('n_total'))
        st.write('Muestras de entrenamiento:', model_info.get('n_train'))
        st.write('Muestras de prueba:', model_info.get('n_test'))
        st.write('Test size:', model_info.get('test_size'))
        st.write('Random state:', model_info.get('random_state'))
        st.write('Agrupación por cliente:', model_info.get('group_column_used'))
        st.write('Variables numéricas:', ', '.join(model_info.get('numeric_features', [])))
        st.write('Variables categóricas:', ', '.join(model_info.get('categorical_features', [])))

    st.subheader('Métricas del modelo')
    if metrics is None:
        st.warning('No se encontró outputs/metrics.json. Ejecuta primero: python src/train_model_improved.py')
    else:
        st.write('MAE:', metrics.get('MAE'))
        st.write('RMSE:', metrics.get('RMSE'))
        st.write('R2:', metrics.get('R2'))

    st.subheader('Comparación con baseline')
    if metrics is None or metrics.get('baseline') is None:
        st.warning('No se encontró baseline dentro de outputs/metrics.json.')
    else:
        baseline = metrics.get('baseline', {})
        st.write('Baseline MAE:', baseline.get('MAE'))
        st.write('Baseline RMSE:', baseline.get('RMSE'))
        st.write('Baseline R2:', baseline.get('R2'))
        st.write('Interpretación: el modelo supera ampliamente al baseline ingenuo en las tres métricas, lo que fortalece la evidencia analítica de la PoC.')

    st.subheader('Gráfico real vs. predicho')
    if PLOT_PATH.exists():
        try:
            img = Image.open(PLOT_PATH)
            st.image(img)
        except Exception as exc:
            st.error(f'No se pudo renderizar el gráfico: {exc}')
    else:
        st.warning('No se encontró outputs/plot.png. Ejecuta el pipeline analítico para generar la visualización.')

    st.subheader('Muestra de predicciones')
    if predictions_df is None:
        st.warning('No se encontró outputs/predictions_sample.csv.')
    else:
        st.dataframe(predictions_df.head(20))

    st.subheader('Interpretación de negocio')
    st.write('La PoC muestra que variables operativas y contextuales explican una proporción sustantiva de la variación del monto mensual. En este conjunto de prueba, el desempeño fue claramente superior al baseline, lo que sugiere utilidad potencial para estimación preliminar, segmentación y planificación.')

    st.subheader('Limitaciones')
    st.write('- El modelo sigue siendo una PoC y no una implementación productiva validada en operación real.')
    st.write('- No se incorporó validación cruzada en esta versión.')
    st.write('- No se documenta tratamiento avanzado de outliers o feature engineering.')
    st.write('- Las métricas deben interpretarse como evidencia exploratoria y reproducible, no como desempeño final garantizado.')

    st.write('Esta página amplía la evidencia del componente analítico y mejora su trazabilidad metodológica dentro del prototipo.')


if __name__ == '__main__':
    main()
