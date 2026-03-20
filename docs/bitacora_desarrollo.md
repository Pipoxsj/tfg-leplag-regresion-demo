# Bitácora de desarrollo del prototipo

Este documento registra de forma cronológica las decisiones, avances, bloqueos y evidencias del prototipo del TFG.

## Cómo usar esta bitácora

Registrar cada avance con el siguiente formato:

---
### Fecha:
### Sprint / bloque:
### Objetivo del trabajo realizado:
### Actividades ejecutadas:
- 
- 
- 

### Archivos creados o modificados:
- 
- 

### Resultado obtenido:
### Problemas encontrados:
### Decisiones tomadas:
### Evidencia generada:
- Capturas:
- Dataset:
- Script/notebook:
- Video:

### Relación con el TFG:
- Sección impactada:
- Aporte al problema / objetivo / metodología / resultados:
---

## Registro inicial

### Fecha:
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
- El alcance del prototipo debe seguir cuidándose para no sobreafirmar implementación completa.

### Decisiones tomadas:
- Construir una capa complementaria a FusionWEB, no un reemplazo total.
- Priorizar trazabilidad, calidad de datos, KPIs y módulo analítico reproducible.

### Evidencia generada:
- Estructura del repo
- Documentación inicial en `docs/`

### Relación con el TFG:
- Sección impactada: Metodología, propuesta, planificación, anexos técnicos.
- Aporte: mejora la trazabilidad del proceso de construcción del prototipo.
