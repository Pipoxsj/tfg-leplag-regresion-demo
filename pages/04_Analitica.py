from pathlib import Path
import json

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = PROJECT_ROOT / 'outputs' / 'metrics.json'
PLOT_PATH = PROJECT_ROOT / 'outputs' / 'plot.png'
DATASET_PATH = PROJECT_ROOT / 'data' / 'dataset_complementario_regresion_anonimizado-2.csv'


def load_metrics():
    if not METRICS_PATH.exists():
        return None
    with open(METRICS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    st.title('Analítica predictiva')
    st.write('Prueba de concepto analítica integrada al prototipo Leplag.')

    st.subheader('Descripción del modelo')
    st.write('Modelo base: regresión lineal múltiple para estimar `monto_mensual_ars` a partir de variables operativas.')
    st.write('Variables consideradas en la PoC: zona, tipo_cliente, mes, tipo_servicio, superficie_m2, distancia_km, tecnico_id y servicios_mes.')
    st.write('La finalidad de esta página es mostrar evidencia reproducible del componente analítico, no una validación productiva definitiva.')

    metrics = load_metrics()

    st.subheader('Estado de artefactos del modelo')
    st.write('Archivo de métricas encontrado:', METRICS_PATH.exists())
    st.write('Archivo de gráfico encontrado:', PLOT_PATH.exists())
    st.write('Dataset anonimizado encontrado:', DATASET_PATH.exists())

    st.subheader('Métricas del modelo')
    if metrics is None:
        st.warning('No se encontró outputs/metrics.json. Para generar resultados, ejecutar primero el pipeline analítico del repositorio.')
    else:
        st.write('MAE:', metrics.get('MAE'))
        st.write('RMSE:', metrics.get('RMSE'))
        st.write('R2:', metrics.get('R2'))

    st.subheader('Gráfico real vs. predicho')
    if PLOT_PATH.exists():
        st.image(str(PLOT_PATH))
    else:
        st.warning('No se encontró outputs/plot.png. Ejecuta el pipeline analítico para generar la visualización.')

    st.subheader('Interpretación de negocio')
    st.write('La PoC permite explorar si variables operativas y contextuales explican parte de la variación del monto mensual. Esto puede servir como apoyo preliminar para estimación, segmentación y planificación.')

    st.subheader('Limitaciones')
    st.write('- El modelo es una PoC y no una implementación productiva validada en operación real.')
    st.write('- No se incorporó validación cruzada en esta versión.')
    st.write('- No se documenta tratamiento avanzado de outliers o feature engineering.')
    st.write('- Las métricas deben interpretarse como evidencia exploratoria y reproducible, no como desempeño final garantizado.')

    st.write('Esta página permite integrar el componente analítico al prototipo y mostrar su relación con la transformación digital orientada a datos.')


if __name__ == '__main__':
    main()
