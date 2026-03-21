# TFG Leplag Fumigaciones - MVP de integración, trazabilidad y analítica

Repositorio de trabajo del TFG de Ricardo Landa sobre transformación digital orientada a datos en Leplag Fumigaciones.

Este proyecto implementa un MVP funcional complementario a FusionWEB para integrar datos operativos, construir trazabilidad de servicios, evaluar calidad de datos y exponer una prueba de concepto analítica reproducible.

## Qué incluye

- ingesta de fuentes sanitizadas de clientes, servicios y técnicos
- base local DuckDB para consulta y análisis
- vistas de trazabilidad operativa
- normalización de tipos de servicio
- reglas de calidad de datos
- dashboard y páginas de consulta en Streamlit
- componente analítico con una PoC de regresión múltiple

## Componentes principales

### Datos e integración
- `src/ingest/loaders.py`
- `src/ingest/run_ingest.py`

### Base y trazabilidad
- `src/db/build_db.py`
- `src/db/build_db_normalized.py`

### Calidad de datos
- `src/quality/rules.py`
- `src/quality/run_quality.py`

### Normalización
- `src/transform/normalize.py`

### App Streamlit
- `app_legacy.py`
- `pages/01_Trazabilidad.py`
- `pages/02_Dashboard.py`
- `pages/03_Calidad.py`
- `pages/04_Analitica.py`
- `pages/05_Analitica_Mejorada.py`

### Analítica
- `src/train_model.py`
- `src/train_model_improved.py`

## Ejecución local

```bash
git clone https://github.com/Pipoxsj/tfg-leplag-regresion-demo.git
cd tfg-leplag-regresion-demo
git checkout feature/capa-integracion-trazabilidad
python -m venv venv
venv\Scripts\activate
pip install pandas duckdb streamlit scikit-learn matplotlib pillow joblib
```

### Construcción de la base del prototipo

```bash
python -m src.ingest.run_ingest
python -m src.db.build_db_normalized
python -m src.quality.run_quality
```

### Ejecución del pipeline analítico mejorado

```bash
python src/train_model_improved.py
```

### Ejecución de la app

```bash
python -m streamlit run app_legacy.py
```

## Qué muestra el prototipo

La aplicación incluye cinco vistas principales:

- **Inicio**: resumen general del prototipo
- **Trazabilidad**: consulta detallada de servicios
- **Dashboard**: indicadores operativos básicos
- **Calidad**: hallazgos e inconsistencias detectadas
- **Analítica**: métricas y artefactos del modelo predictivo

## Componente analítico

El pipeline analítico reproduce una prueba de concepto de regresión lineal múltiple para estimar `monto_mensual_ars` a partir de variables operativas y contextuales.

### Artefactos generados

- `outputs/metrics.json`
- `outputs/model_info.json`
- `outputs/plot.png`
- `outputs/predictions_sample.csv`
- `outputs/model.joblib`

### Estructura de datos

El dataset `data/dataset_complementario_regresion_anonimizado-2.csv` contiene, entre otras, las siguientes variables:

- `id_cliente_anon`
- `zona`
- `tipo_cliente`
- `mes`
- `tipo_servicio`
- `superficie_m2`
- `distancia_km`
- `tecnico_id`
- `servicios_mes`
- `monto_mensual_ars`

En la versión mejorada del pipeline:
- `tecnico_id` se trata como variable categórica
- se incorpora imputación explícita
- se utiliza split agrupado por cliente cuando la columna está disponible
- se compara el modelo contra un baseline simple

## Video demo

El video de demostración del prototipo está disponible en el siguiente enlace:

👉 [Ver video demo](https://docs.google.com/videos/d/1nBcodtw41iR3uLrHqs6swiHNwT7i_c-rtLHMSomg0Bo/edit?usp=sharing)

## Troubleshooting

### Error: `ModuleNotFoundError`
Instala las dependencias necesarias en el entorno virtual:

```bash
pip install pandas duckdb streamlit scikit-learn matplotlib pillow joblib
```

### Error: `FileNotFoundError`
Asegúrate de ejecutar los comandos desde la raíz del repositorio:

```bash
cd tfg-leplag-regresion-demo
```

### La app no abre o localhost no responde
Verifica que Streamlit esté corriendo:

```bash
python -m streamlit run app_legacy.py
```

### No aparecen métricas o gráfico en la página Analítica
Ejecuta primero el pipeline analítico mejorado:

```bash
python src/train_model_improved.py
```

## Alcance y limitaciones

Este MVP se valida en entorno local y no representa un despliegue productivo. Las fuentes utilizadas están sanitizadas y recortadas para fines de demostración. El componente analítico corresponde a una prueba de concepto y no a un servicio operativo en producción.

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Ver archivo `LICENSE` para más detalles.

## Autor

**Ricardo Landa**  
Trabajo Final de Grado  
Universidad Siglo 21

## Agradecimientos

- Instituto Data Science Argentina
- Leplag Fumigaciones
- Comunidad de Python y scikit-learn
