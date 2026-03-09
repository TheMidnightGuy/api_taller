# Notebook — Desarrollo CRISP-DM

Documentación del proceso de análisis y preparación de datos realizado en el notebook `DESAFIO_FINAL.ipynb`, siguiendo el estándar **CRISP-DM** *(Cross-Industry Standard Process for Data Mining)*.

---

## Fase 1 — Business Understanding

### Contexto del problema

El objetivo del proyecto es predecir el **tiempo en semanas** que un vehículo siniestrado permanecerá en taller para su reparación. Esta predicción permite a la organización planificar recursos, gestionar tiempos de entrega y dar visibilidad al proceso de siniestros.

### Archivos entregados

- **`claims_dataset.csv`** — Dataset de inferencia con 10 registros de siniestros de pérdida parcial.
- **6 archivos `.pkl`** — Pipelines de preprocesamiento serializados, creados por el Data Scientist.
- **`linnear_regression.pkl`** — Modelo de regresión lineal pre-entrenado.
- **`documentacion.md`** — Instructivo con descripción de variables, interdependencias entre pipelines y requisitos del modelo.

### Variables del dataset

| Variable | Descripción |
|---|---|
| `claim_id` | Identificador del siniestro |
| `marca_vehiculo` | Marca del vehículo (`ferd`, `fait`, `chepy`) |
| `antiguedad_vehiculo` | Años desde fabricación hasta el siniestro |
| `tipo_poliza` | Tipo de póliza asociada |
| `taller` | Identificador del taller (1–5) |
| `partes_a_reparar` | Número de partes a reparar |
| `partes_a_reemplazar` | Número de partes a reemplazar |

### Condición especial

El cliente estableció que cuando `tipo_poliza == 4`, el modelo debe retornar `-1`, ya que estas pólizas se gestionan de forma especial y no requieren predicción.

---

## Fase 2 — Data Understanding

### Carga del dataset

El dataset se carga con separador `|` y se le agrega la columna `valor_vehiculo` inicializada en `NaN`, ya que su valor será calculado posteriormente por los pipelines de preprocesamiento.

### Hallazgos iniciales

- **10 registros** en total.
- **3 valores nulos** en la columna `marca_vehiculo`.
- **0 duplicados**.
- Los nulos no se eliminan en esta etapa — el pipeline de imputación los gestiona más adelante.

### Interdependencias entre pipelines

Los 6 pipelines no son independientes entre sí. Su ejecución debe seguir un orden específico:

| Pipeline | Dependencia |
|---|---|
| `pipeline_1` | Independiente |
| `pipeline_2` | Depende de `pipeline_1` |
| `pipeline_3` | Independiente |
| `pipeline_4` | Depende de `pipeline_2` y `pipeline_3` |
| `pipeline_5` | Depende de `pipeline_3` |
| `pipeline_6` | Independiente (imputación final) |

---

## Fase 3 — Data Preparation

### Problema con los pipelines originales

Los archivos `.pkl` entregados no podían ser leídos ni procesados directamente. Fueron creados con `scikit-learn 1.3.0` y el entorno de trabajo utiliza `1.6.1`, lo que generaba incompatibilidades al deserializarlos.

**Solución:** Se reconstruyeron los pipelines manualmente a partir del análisis de su contenido binario con un editor hexadecimal (HxD), extrayendo la lógica real de cada transformación.

### Pipelines reconstruidos

Cada pipeline fue reconstruido como un `sklearn.pipeline.Pipeline` con un `FunctionTransformer`.

**Pipeline 1 — Suma de piezas totales**

Crea la columna `total_piezas` sumando `partes_a_reparar` y `partes_a_reemplazar`.

**Pipeline 3 — Codificación de marca**

Convierte `marca_vehiculo` (texto) a `marca_vehiculo_encoded` (numérico) usando el diccionario:
```
chepy → 1 | fait → 2 | ferd → 3
```

**Pipeline 2 — Normalización logarítmica**

Aplica `np.log` sobre `total_piezas` para crear `log_total_piezas`. Incluye un `time.sleep(2)` definido en el modelo original.

**Pipeline 4 — Valor de vehículo y valor por pieza**

Crea `valor_vehiculo` y `valor_por_pieza` mediante mapeo por diccionarios según marca y taller:
```
Valor vehículo:  chepy=1500 | fait=2950 | ferd=8540
Valor por pieza: taller1=50 | taller2=100 | taller3=200 | taller4=300 | taller5=400
```

**Pipeline 5 — Reclamos por marca y taller**

Crea `reclamos_por_marca` y `reclamos_por_taller` desde diccionarios históricos. Incluye un `time.sleep(10)` definido en el modelo original.

**Pipeline 6 — Imputación de valores nulos**

Aplica `fillna` con el siguiente diccionario de imputación:
```
log_total_piezas=1.4545 | marca_vehiculo_encoded=0 | valor_vehiculo=3560
valor_por_pieza=150 | antiguedad_vehiculo=1 | tipo_poliza=1 | taller=1
partes_a_reparar=3 | partes_a_reemplazar=1
```

### Orden de ejecución

```
pipeline_1 → pipeline_3 → pipeline_2 → pipeline_4 → pipeline_5 → pipeline_6
```

Este orden garantiza que cada columna exista antes de ser utilizada por el pipeline siguiente.

### Exportación de artefactos

Los 6 pipelines se encapsulan en un único `pipeline_completo` para simplificar su consumo desde la API. Tanto el pipeline como el modelo se exportan con **dill**, que serializa el código de las funciones internamente, eliminando la dependencia de un archivo externo `functions.py` al momento de deserializar.

```
pipeline_completo.pkl
modelo_RL.pkl
```

---

## Fase 4 — Modeling

### Modelo

Se utiliza el modelo de regresión lineal pre-entrenado `linnear_regression.pkl`, entrenado con datos históricos de siniestros.

### Features requeridas por el modelo

| Feature | Tipo |
|---|---|
| `log_total_piezas` | float64 |
| `marca_vehiculo_encoded` | int64 |
| `valor_vehiculo` | int64 |
| `valor_por_pieza` | int64 |
| `antiguedad_vehiculo` | int64 |

### Predicción

El modelo recibe el dataframe procesado con las 5 features y retorna el número de semanas estimado. Tras la predicción se aplica la condición de negocio: si `tipo_poliza == 4`, el resultado se reemplaza por `-1`.

### Casos validados

| claim_id | tipo_poliza | prediccion_semanas |
|---|---|---|
| 561205 | 1 | 4.38 |
| 408550 | 4 | -1 (regla de negocio) |
| 208451 | 2 (marca=null) | 6.17 (imputado) |

---

## Fase 5 — Evaluation

El modelo fue validado funcionalmente sobre los 10 registros del dataset de inferencia. La evaluación de métricas estadísticas (RMSE, R²) no aplica en este contexto ya que el modelo es pre-entrenado y se entrega como insumo — el foco del desafío es el despliegue correcto del servicio.

---

## Fase 6 — Deployment

El despliegue completo se documenta en el `README.md` principal del repositorio e incluye:

- API REST con FastAPI consumiendo los artefactos exportados.
- Imagen Docker publicada en GHCR mediante CI/CD con GitHub Actions.
- Log de predicciones para monitoreo del modelo en producción.
- Stress test de 10 consultas en paralelo validado con Postman (40/40 tests passed).