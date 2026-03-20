# Registro de decisiones arquitectónicas

Este documento resume decisiones técnicas y de alcance del prototipo, con el objetivo de reutilizarlas en el TFG.

## DA-001 — El prototipo no reemplaza FusionWEB
- **Fecha:**
- **Decisión:** el prototipo se define como una capa complementaria a FusionWEB.
- **Motivo:** el caso real muestra uso parcial del sistema vigente; el problema principal es la integración incompleta, la trazabilidad y la explotación analítica limitada.
- **Consecuencia:** se evita modelar el prototipo como ERP/sistema total.

## DA-002 — Ingesta basada en archivos exportados
- **Fecha:**
- **Decisión:** la integración inicial se realizará mediante archivos CSV/XLSX exportados desde FusionWEB y planillas complementarias.
- **Motivo:** no existe evidencia técnica consolidada de API utilizable para el TFG.
- **Consecuencia:** el pipeline será reproducible y controlable en entorno de prueba.

## DA-003 — Repositorio analítico local
- **Fecha:**
- **Decisión:** usar DuckDB o SQLite como base local del prototipo.
- **Motivo:** simplicidad de despliegue, reproducibilidad y bajo costo.
- **Consecuencia:** se facilita la construcción de vistas de trazabilidad y KPIs.

## DA-004 — Interfaz liviana para demostración
- **Fecha:**
- **Decisión:** usar Streamlit como interfaz del prototipo.
- **Motivo:** velocidad de construcción, bajo esfuerzo de mantenimiento y buena capacidad demostrativa para TFG.
- **Consecuencia:** el foco queda en trazabilidad y analítica, no en front-end complejo.

## DA-005 — El componente analítico es una PoC integrada
- **Fecha:**
- **Decisión:** mantener la regresión múltiple como prueba de concepto analítica reproducible integrada al prototipo.
- **Motivo:** ya existe evidencia técnica ejecutable en el repositorio.
- **Consecuencia:** el módulo analítico no debe presentarse como sistema de IA productivo, sino como evidencia de factibilidad.
