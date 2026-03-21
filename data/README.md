# Organización de la carpeta `data`

Esta carpeta reúne tanto los artefactos del componente analítico original como las nuevas estructuras de datos incorporadas para el MVP de integración, trazabilidad y analítica.

## Estructura actual

### `data/dataset_complementario_regresion_anonimizado-2.csv`
Dataset anonimizado del componente analítico del TFG.

- **Rol:** prueba de concepto de regresión múltiple.
- **Estado:** se conserva en la raíz de `data/` por compatibilidad con `src/train_model.py` y `src/train_model_improved.py`.
- **Observación:** corresponde al componente analítico legado/integrado, no a las fuentes operativas mínimas del MVP.

### `data/raw/`
Fuentes sanitizadas utilizadas por el MVP operativo.

Archivos previstos o presentes:
- `clientes_fusionweb.csv`
- `clientes_fusionweb_compatible.csv`
- `servicios_u_ot_fusionweb.csv`
- `tecnicos_complementario.csv`

**Rol:** insumo de la capa de integración y trazabilidad.

### `data/staging/`
Espacio reservado para resultados intermedios de limpieza, conciliación o transformación.

**Rol:** capa opcional de preparación antes de persistir los datos integrados.

### `data/processed/`
Resultados persistidos y estructuras derivadas del prototipo.

Archivos previstos o presentes:
- `leplag.duckdb`

**Rol:** base integrada y normalizada utilizada por la app Streamlit.

## Criterio de uso

- El archivo `dataset_complementario_regresion_anonimizado-2.csv` se mantiene porque sigue siendo necesario para la PoC analítica.
- Las fuentes del MVP operativo deben mantenerse en `data/raw/`.
- Los resultados intermedios pueden guardarse en `data/staging/`.
- Los artefactos persistidos del prototipo deben guardarse en `data/processed/`.

## Nota metodológica

La coexistencia de estos elementos dentro de `data/` refleja que el repositorio evolucionó desde una demo analítica hacia un MVP más amplio. En el TFG conviene explicitar esta transición para diferenciar:

1. el componente analítico original;
2. la capa de integración y trazabilidad desarrollada posteriormente;
3. la articulación final de ambos dentro del prototipo.
