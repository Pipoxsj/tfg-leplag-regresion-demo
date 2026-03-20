# Relación entre artefactos del repositorio y secciones del TFG

Este documento ayuda a vincular cada artefacto técnico del repositorio con la sección académica correspondiente del TFG.

| Artefacto del repo | Propósito técnico | Sección del TFG donde puede citarse | Tipo de evidencia |
|---|---|---|---|
| `docs/fuentes_datos.md` | Inventario de fuentes | Materiales, instrumentos y fuentes de datos | Documental |
| `docs/diccionario_fuentes.csv` | Normalización de campos | Diseño metodológico / preparación de datos | Técnica |
| `requirements_prototype.txt` | Dependencias del entorno | Herramientas utilizadas | Técnica |
| `docs/bitacora_desarrollo.md` | Registro cronológico del desarrollo | Metodología / planificación / anexos | Proceso |
| `docs/decisiones_arquitectonicas.md` | Justificación técnica de decisiones | Propuesta / arquitectura / discusión | Argumentativa |
| `src/analytics/` | Componente analítico | Aplicación real de CRISP-DM / resultados | Técnica |
| `data/raw/` | Fuentes crudas | Fuentes de datos | Técnica |
| `data/staging/` | Datos intermedios | Preparación y limpieza | Técnica |
| `data/processed/` | Datos normalizados | Resultados del procesamiento | Técnica |
| `tests/` | Casos de prueba | Validación del prototipo | Técnica |
| `outputs/` | Métricas, gráficos, salidas | Resultados / anexos / demo | Visual |

## Recomendación de uso
1. Cada vez que se cree un artefacto nuevo, agregarlo a esta tabla.
2. Mantener consistente el nombre del archivo en repo y el nombre citado en el TFG.
3. Si un artefacto se usa como anexo, registrar también su ubicación final en el manuscrito.
