# Fuentes de datos del prototipo

Este documento inventaria las fuentes iniciales previstas para la **capa funcional de integración, trazabilidad y analítica complementaria a FusionWEB**.

> Nota metodológica: este inventario es una **versión inicial de trabajo**. Debe ajustarse cuando se disponga de las exportaciones reales definitivas de FusionWEB y de las planillas complementarias efectivamente utilizadas por Leplag.

## 1. clientes_fusionweb.xlsx
- **Origen:** exportación de FusionWEB
- **Rol en el prototipo:** dimensión maestra de clientes
- **Contenido esperado:** identificación del cliente, razón social o nombre, CUIT/CUIL, dirección, teléfono, zona/localidad
- **Campos esperados:** cliente_id, cliente_nombre, cuit, direccion, telefono, zona
- **Problemas esperados:** duplicados, CUIT faltante, formatos de texto inconsistentes, direcciones incompletas

## 2. servicios_u_ot_fusionweb.xlsx
- **Origen:** exportación de FusionWEB
- **Rol en el prototipo:** hecho principal de trazabilidad operativa
- **Contenido esperado:** órdenes de trabajo / servicios programados, ejecutados, cancelados o reprogramados
- **Campos esperados:** servicio_id, cliente_id, fecha_programada, fecha_ejecucion, estado_servicio, tipo_servicio, tecnico_id, observaciones
- **Problemas esperados:** estados inconsistentes, fechas faltantes, servicios sin técnico asignado, ausencia de clave estable

## 3. cronograma_fusionweb.xlsx
- **Origen:** exportación o captura estructurada de FusionWEB
- **Rol en el prototipo:** complemento temporal para planificación y asignación
- **Contenido esperado:** agenda diaria o semanal por técnico
- **Campos esperados:** evento_id, servicio_id, tecnico_id, fecha_programada, hora_inicio, hora_fin, estado_programacion
- **Problemas esperados:** solapamientos, huecos horarios, diferencias con órdenes de trabajo

## 4. productos_fusionweb.xlsx
- **Origen:** exportación de FusionWEB
- **Rol en el prototipo:** catálogo de insumos / productos
- **Contenido esperado:** producto, principio activo, certificación, precio, proveedor
- **Campos esperados:** producto_id, producto_nombre, principio_activo, certificacion, precio, proveedor
- **Problemas esperados:** nombres no normalizados, unidades inconsistentes, precios faltantes

## 5. tecnicos_complementario.xlsx
- **Origen:** planilla complementaria o exportación disponible
- **Rol en el prototipo:** dimensión de técnicos
- **Contenido esperado:** identificación del técnico, nombre, rol, disponibilidad
- **Campos esperados:** tecnico_id, tecnico_nombre, rol, activo
- **Problemas esperados:** IDs no coincidentes con otras fuentes, nombres duplicados o abreviados

## 6. certificados_complementario.xlsx
- **Origen:** planilla complementaria / registro documental
- **Rol en el prototipo:** control documental de servicios
- **Contenido esperado:** certificado asociado a servicio, fecha, estado documental
- **Campos esperados:** certificado_id, servicio_id, fecha_certificado, estado_certificado, observaciones
- **Problemas esperados:** servicios ejecutados sin certificado, documentos no vinculados por ID, fechas incompletas

## 7. dataset_complementario_regresion_anonimizado-2.csv
- **Origen:** dataset anonimizado del componente analítico del TFG
- **Rol en el prototipo:** prueba de concepto analítica reproducible
- **Contenido esperado:** variables operativas y variable objetivo `monto_mensual_ars`
- **Campos observados en el repositorio actual:** id_cliente_anon, zona, tipo_cliente, mes, tipo_servicio, superficie_m2, distancia_km, tecnico_id, servicios_mes, monto_mensual_ars
- **Problemas esperados:** ausencia de validación cruzada, outliers no tratados explícitamente, generalización acotada

## Recomendaciones de gobierno inicial
1. Mantener una copia inalterada de cada fuente en `data/raw/`.
2. Guardar resultados intermedios limpios en `data/staging/`.
3. Guardar tablas normalizadas e integradas en `data/processed/`.
4. Registrar en cada corrida la fecha de carga y el nombre del archivo fuente.
5. No sobrescribir archivos crudos; versionar por fecha cuando cambien las exportaciones.
