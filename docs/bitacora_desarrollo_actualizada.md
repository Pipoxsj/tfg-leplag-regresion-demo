# Bitácora de desarrollo del prototipo

Este documento registra de forma cronológica las decisiones, avances, bloqueos y evidencias del prototipo del TFG.

---
### Fecha: 2026-03-20
### Sprint / bloque: Preparación del prototipo
### Objetivo del trabajo realizado:
Dejar preparada la rama de desarrollo y la estructura base del prototipo complementario a FusionWEB.

### Actividades ejecutadas:
- Creación de la rama `feature/capa-integracion-trazabilidad`.
- Incorporación de carpetas base para `app`, `data`, `src`, `tests` y `docs`.
- Creación de `requirements_prototype.txt`.
- Creación de inventario inicial de fuentes de datos.
- Creación de diccionario canónico inicial de campos.

### Archivos creados o modificados:
- `requirements_prototype.txt`
- `docs/fuentes_datos.md`
- `docs/diccionario_fuentes.csv`
- estructura base del repositorio

### Resultado obtenido:
Quedó preparada la base documental y técnica para avanzar con los loaders y la normalización de datos.

### Problemas encontrados:
- Aún no se incorporaron las exportaciones reales/anónimas definitivas.
- El alcance del prototipo debía cuidarse para no sobreafirmar implementación completa.

### Decisiones tomadas:
- Construir una capa complementaria a FusionWEB, no un reemplazo total.
- Priorizar trazabilidad, calidad de datos, KPIs y módulo analítico reproducible.

### Evidencia generada:
- Estructura del repo
- Documentación inicial en `docs/`

### Relación con el TFG:
- Sección impactada: Metodología, propuesta, planificación, anexos técnicos.
- Aporte: mejora la trazabilidad del proceso de construcción del prototipo.
---

---
### Fecha: 2026-03-20
### Sprint / bloque: Ingesta inicial y sanitización
### Objetivo del trabajo realizado:
Definir fuentes mínimas del prototipo, sanitizar muestras y construir la ingesta reproducible.

### Actividades ejecutadas:
- Selección de las tres fuentes mínimas del MVP: clientes, servicios/órdenes de trabajo y técnicos.
- Sanitización de la exportación de órdenes de trabajo para eliminar identificadores sensibles.
- Creación de archivos `clientes_fusionweb.csv`, `clientes_fusionweb_compatible.csv`, `servicios_u_ot_fusionweb.csv` y `tecnicos_complementario.csv`.
- Desarrollo de `src/ingest/loaders.py` y `src/ingest/run_ingest.py`.
- Ejecución de la carga inicial y corrección de inconsistencias entre IDs de clientes y servicios.

### Archivos creados o modificados:
- `data/raw/clientes_fusionweb.csv`
- `data/raw/clientes_fusionweb_compatible.csv`
- `data/raw/servicios_u_ot_fusionweb.csv`
- `data/raw/tecnicos_complementario.csv`
- `src/ingest/loaders.py`
- `src/ingest/run_ingest.py`

### Resultado obtenido:
Se logró cargar correctamente las tres fuentes mínimas del prototipo con validación básica de columnas y consistencia cruzada de IDs.

### Problemas encontrados:
- La exportación real contenía datos sensibles y debió anonimizarse.
- El archivo inicial de clientes no coincidía con los IDs del archivo de servicios.

### Decisiones tomadas:
- Trabajar con una muestra sanitizada y compatible para garantizar reproducibilidad y resguardo de datos.
- Priorizar el archivo `clientes_fusionweb_compatible.csv` como fuente principal del MVP.

### Evidencia generada:
- CSV sanitizados en `data/raw/`
- Script de carga reproducible
- Salida exitosa de `python -m src.ingest.run_ingest`

### Relación con el TFG:
- Sección impactada: Materiales, instrumentos y fuentes de datos; diseño metodológico.
- Aporte: demuestra cómo se obtuvieron, adaptaron y cargaron las fuentes para el entorno de prueba.
---

---
### Fecha: 2026-03-20
### Sprint / bloque: Base integrada y trazabilidad
### Objetivo del trabajo realizado:
Construir una base local reproducible y vistas iniciales de trazabilidad sobre las fuentes integradas.

### Actividades ejecutadas:
- Desarrollo de `src/db/build_db.py`.
- Construcción de `data/processed/leplag.duckdb`.
- Creación de tablas `clientes`, `servicios` y `tecnicos`.
- Creación de la vista `vw_trazabilidad_servicios`.
- Verificación de cantidades y consistencia básica de la base.

### Archivos creados o modificados:
- `src/db/build_db.py`
- `data/processed/leplag.duckdb`

### Resultado obtenido:
Se obtuvo una base DuckDB local con persistencia de tablas y una vista inicial de trazabilidad operativa.

### Problemas encontrados:
- La copia local del repositorio no tenía inicialmente el archivo `build_db.py` actualizado y fue necesario sincronizar la branch.

### Decisiones tomadas:
- Usar DuckDB como repositorio analítico local por simplicidad, reproducibilidad y bajo costo de despliegue.

### Evidencia generada:
- Ejecución exitosa de `python -m src.db.build_db`
- Base `leplag.duckdb`
- Conteos verificados de tablas y vista de trazabilidad

### Relación con el TFG:
- Sección impactada: Propuesta, arquitectura, resultados técnicos.
- Aporte: demuestra la consolidación del circuito mínimo de integración y consulta.
---

---
### Fecha: 2026-03-20
### Sprint / bloque: Calidad de datos y normalización
### Objetivo del trabajo realizado:
Agregar reglas de validación de calidad y resolver el problema del campo compuesto `servicios`.

### Actividades ejecutadas:
- Desarrollo de `src/quality/rules.py` y `src/quality/run_quality.py`.
- Definición de reglas para servicios sin cliente, sin técnico, estados inválidos, horarios faltantes, duplicados potenciales y servicios con múltiples tipos.
- Ejecución de la validación de calidad.
- Desarrollo de `src/transform/normalize.py`.
- Construcción de `src/db/build_db_normalized.py`.
- Creación de la tabla `servicios_tipos` y de la vista `vw_trazabilidad_servicios_tipos`.

### Archivos creados o modificados:
- `src/quality/rules.py`
- `src/quality/run_quality.py`
- `src/transform/normalize.py`
- `src/db/build_db_normalized.py`

### Resultado obtenido:
Se detectaron 4 hallazgos de baja severidad asociados a servicios con múltiples tipos, y se normalizó el campo `servicios` en una estructura relacional apta para análisis.

### Problemas encontrados:
- El campo `servicios` mezclaba más de un tipo en una misma celda.

### Decisiones tomadas:
- Mantener la detección del problema como evidencia de calidad de datos.
- Crear una tabla derivada `servicios_tipos` en lugar de dejar el campo compuesto como estaba.

### Evidencia generada:
- Ejecución exitosa de `python -m src.quality.run_quality`
- Ejecución exitosa de `python -m src.db.build_db_normalized`
- Hallazgo `servicio_multi_tipo`
- Resumen de tipos normalizados (`DESINSECTACION`, `DESRATIZACION`)

### Relación con el TFG:
- Sección impactada: Diseño metodológico, preparación de datos, resultados y discusión.
- Aporte: muestra capacidad de detección de inconsistencias y mejora estructural de los datos fuente.
---

---
### Fecha: 2026-03-20
### Sprint / bloque: Construcción de interfaz demostrativa
### Objetivo del trabajo realizado:
Exponer el MVP mediante una interfaz simple que permita consultar trazabilidad, indicadores, calidad y analítica.

### Actividades ejecutadas:
- Desarrollo de `app.py`, `app_compat.py` y `app_legacy.py` para resolver compatibilidades con distintas versiones de Streamlit.
- Desarrollo de páginas `01_Trazabilidad`, `02_Dashboard`, `03_Calidad`, `04_Analitica` y `05_Analitica_Mejorada`.
- Pruebas de ejecución local en Windows con entorno virtual.
- Ajustes de compatibilidad por errores de `st.cache_data`, `use_container_width` y renderizado.

### Archivos creados o modificados:
- `app.py`
- `app_compat.py`
- `app_legacy.py`
- `pages/01_Trazabilidad.py`
- `pages/02_Dashboard.py`
- `pages/03_Calidad.py`
- `pages/04_Analitica.py`
- `pages/05_Analitica_Mejorada.py`

### Resultado obtenido:
Se logró una app Streamlit funcional con menú lateral y cinco vistas orientadas al problema del TFG.

### Problemas encontrados:
- Incompatibilidades con una versión antigua de Streamlit en el entorno local.
- Algunas páginas no aparecían inicialmente por ubicación incorrecta de la carpeta `pages`.
- Errores de renderizado del gráfico analítico y de parámetros no soportados.

### Decisiones tomadas:
- Mantener `app_legacy.py` como entry point principal del prototipo por compatibilidad.
- Ubicar las páginas en la carpeta raíz `pages/` para asegurar su detección por Streamlit.

### Evidencia generada:
- Capturas funcionales de Inicio, Trazabilidad, Dashboard, Calidad y Analítica.
- Ejecución exitosa de `python -m streamlit run app_legacy.py`.

### Relación con el TFG:
- Sección impactada: Prototipo, validación, resultados, demo.
- Aporte: demuestra implementación funcional del MVP en entorno de prueba.
---

---
### Fecha: 2026-03-21
### Sprint / bloque: Fortalecimiento metodológico del componente analítico
### Objetivo del trabajo realizado:
Mejorar el pipeline analítico para que la PoC tenga mejor sustento metodológico y más artefactos reutilizables en el TFG.

### Actividades ejecutadas:
- Revisión crítica del pipeline inicial de regresión.
- Desarrollo de `src/utils_improved.py` y `src/train_model_improved.py`.
- Tratamiento de `tecnico_id` como variable categórica.
- Incorporación de imputación para variables numéricas y categóricas.
- Implementación de split agrupado por cliente.
- Comparación contra `DummyRegressor` como baseline.
- Guardado de `metrics.json`, `model_info.json`, `plot.png`, `predictions_sample.csv` y `model.joblib`.
- Integración de estos artefactos en la página `05_Analitica_Mejorada.py`.

### Archivos creados o modificados:
- `src/utils_improved.py`
- `src/train_model_improved.py`
- `outputs/metrics.json`
- `outputs/model_info.json`
- `outputs/plot.png`
- `outputs/predictions_sample.csv`
- `outputs/model.joblib`
- `pages/05_Analitica_Mejorada.py`

### Resultado obtenido:
Se obtuvo una PoC analítica más sólida, con métricas reales de desempeño (`MAE`, `RMSE`, `R2`), comparación contra baseline y artefactos reproducibles listos para anexos y demo.

### Problemas encontrados:
- Faltaban dependencias como `joblib`, `matplotlib` y `scikit-learn` en el entorno virtual.
- La página analítica inicial mostraba artefactos de manera incompleta.

### Decisiones tomadas:
- Mantener el componente analítico como PoC integrada, no como módulo productivo.
- Exponer baseline, configuración del experimento y muestra de predicciones para reforzar la trazabilidad metodológica.

### Evidencia generada:
- Ejecución exitosa de `python src/train_model_improved.py`
- Métricas del modelo y baseline
- Gráfico real vs. predicho
- Página `Analitica Mejorada` funcionando

### Relación con el TFG:
- Sección impactada: Aplicación de CRISP-DM, resultados analíticos, discusión y limitaciones.
- Aporte: fortalece el sustento metodológico y la evidencia cuantitativa del prototipo.
---

---
### Fecha: 2026-03-21
### Sprint / bloque: Organización de evidencia y control de versiones
### Objetivo del trabajo realizado:
Ordenar el repositorio como evidencia técnica del TFG y dejar un hito claro del MVP.

### Actividades ejecutadas:
- Actualización del `README.md` para reflejar el MVP de integración, trazabilidad y analítica.
- Creación de documentos auxiliares: relación repo-TFG y decisiones arquitectónicas.
- Apertura del Pull Request `#2` para registrar la versión hito del MVP.
- Definición de capturas sugeridas y lineamientos de evidencia para el manuscrito.

### Archivos creados o modificados:
- `README.md`
- `docs/relacion_repo_tfg.md`
- `docs/decisiones_arquitectonicas.md`
- Pull Request #2 en GitHub

### Resultado obtenido:
Quedó consolidada una versión hito del prototipo con trazabilidad de cambios, documentación auxiliar y evidencia organizada para uso en el TFG.

### Problemas encontrados:
- `main` seguía mostrando la versión anterior mientras el PR permanecía sin merge.
- Fue necesario ajustar la portada del repositorio para que no describiera solo la demo de regresión.

### Decisiones tomadas:
- Mantener la branch de desarrollo como fuente principal del MVP hasta consolidar la documentación final.
- Usar el PR como evidencia de evolución técnica y control de versiones.

### Evidencia generada:
- Pull Request #2 abierto
- README alineado al MVP
- Matriz preliminar de evidencia útil para el TFG

### Relación con el TFG:
- Sección impactada: Anexos, metodología, validación y evidencia del prototipo.
- Aporte: facilita la articulación entre desarrollo técnico y presentación académica.
---
