# TFG Leplag Fumigaciones - Demo Regresión Múltiple

Repositorio demo del **Trabajo Final de Grado** de Ricardo Landa: _Transformación digital orientada a datos en Leplag Fumigaciones_.

Este repositorio reproduce el pipeline de regresión lineal múltiple para predecir `monto_mensual_ars` a partir de variables operativas (superficie, distancia, mes, tipo de cliente, etc.).

---

## 📋 Características

- **Pipeline completo**: carga de datos, preprocesamiento con `ColumnTransformer`, entrenamiento con `LinearRegression` de scikit-learn.
- **Métricas**: MAE, RMSE, R².
- **Visualización**: gráfico scatter de valores reales vs. predichos.
- **Reproducibilidad**: `random_state=42` fijado en train/test split.
- **Ejecutable en**:
  - **Google Colab** (1-click).
  - **Entorno local** (Python 3.8+).

---

## 🚀 Ejecución en Google Colab (Recomendado)

1. Abre el notebook directamente en Colab haciendo clic aquí:  
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Pipoxsj/tfg-leplag-regresion-demo/blob/main/notebooks/demo_regresion_leplag.ipynb)

2. El notebook descargará automáticamente el dataset desde el repo (o puedes subirlo manualmente).

3. Ejecuta todas las celdas (`Runtime > Run all`).

4. Los resultados (métricas y gráfico) se generarán en las últimas celdas.

---

## 💻 Ejecución local

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes)

### Pasos

1. **Clonar el repositorio**:

```bash
git clone https://github.com/Pipoxsj/tfg-leplag-regresion-demo.git
cd tfg-leplag-regresion-demo
```

2. **Crear entorno virtual** (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```

4. **Ejecutar el script de entrenamiento**:

```bash
python src/train_model.py
```

5. **Resultados**:
   - Métricas impresas en consola.
   - Gráfico guardado en `outputs/plot.png`.
   - Métricas JSON en `outputs/metrics.json`.

---

## 📊 Outputs esperados

Al ejecutar el pipeline, se generan:

| Archivo                | Descripción                                                       |
|------------------------|-------------------------------------------------------------------|
| `outputs/metrics.json` | Métricas del modelo: MAE, RMSE, R² en formato JSON               |
| `outputs/plot.png`     | Gráfico scatter: valores reales vs. predichos                     |

**Ejemplo de métricas**:

```json
{
  "MAE": 5432.18,
  "RMSE": 7821.34,
  "R2": 0.6789
}
```

---

## 🗂️ Estructura de datos

El dataset (`data/dataset_complementario_regresion_anonimizado-2.csv`) contiene las siguientes columnas:

| Columna                | Tipo         | Descripción                                      |
|------------------------|--------------|--------------------------------------------------|
| `id_cliente_anon`      | int          | ID anónimo del cliente                           |
| `zona`                 | categórica   | Zona geográfica (RAWSON, DESCONOCIDA, etc.)      |
| `tipo_cliente`         | categórica   | Residencial o Comercial/Industrial               |
| `mes`                  | int          | Mes del año (1-12)                               |
| `tipo_servicio`        | categórica   | Fumigación, Desinfección o Desratización         |
| `superficie_m2`        | float        | Superficie tratada en m²                         |
| `distancia_km`         | float        | Distancia al lugar del servicio (km)             |
| `tecnico_id`           | int          | ID del técnico asignado                          |
| `servicios_mes`        | int          | Cantidad de servicios prestados ese mes          |
| `monto_mensual_ars`    | float        | **Variable objetivo**: monto facturado (ARS)     |

---
## 🎥 Video demo 

El video de demostración (3–5 minutos) del prototipo está disponible en el siguiente enlace:

👉 [Ver video demo](https://docs.google.com/videos/d/1nBcodtw41iR3uLrHqs6swiHNwT7i_c-rtLHMSomg0Bo/edit?usp=sharing)

---

## 🔧 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'sklearn'`

**Solución**: Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

### Error: `FileNotFoundError: data/dataset_complementario_regresion_anonimizado-2.csv`

**Solución**: Asegúrate de estar ejecutando el script desde la raíz del repositorio:

```bash
cd tfg-leplag-regresion-demo
python src/train_model.py
```

---

### El gráfico no se muestra en entorno local

**Solución**: El gráfico se guarda automáticamente en `outputs/plot.png`. Si quieres visualizarlo interactivamente, ejecuta el notebook en Jupyter:

```bash
jupyter notebook notebooks/demo_regresion_leplag.ipynb
```

---

## ⚠️ Limitaciones

- **Modelo simple**: se utiliza regresión lineal múltiple sin feature engineering avanzado ni ajuste de hiperparámetros.
- **Validación**: no se implementa validación cruzada (k-fold CV).
- **Outliers**: no se aplica tratamiento explícito de outliers (se mantiene dataset original).
- **Variables descartadas**: `id_cliente_anon` no se usa como feature (es identificador, no predictora).
- **Generalización**: las métricas corresponden a un test set del 20% con split aleatorio (random_state=42).

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Ver archivo `LICENSE` para más detalles.

---

## 👤 Autor

**Ricardo Landa**  
Trabajo Final de Grado - Diplomatura en Ciencia de Datos  
Universidad Siglo 21 - 2025

---

## 📧 Contacto

Para consultas sobre el TFG o el repositorio, contactar vía GitHub Issues.

---

## 🙏 Agradecimientos

- Instituto Data Science Argentina
- Leplag Fumigaciones (empresa caso de estudio)
- Comunidad de scikit-learn y Python
