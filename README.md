# API Taller — Predicción de Semanas en Taller

API REST desarrollada con **FastAPI** para predecir el tiempo en semanas que un vehículo siniestrado permanecerá en taller, a partir de un modelo de regresión lineal pre-entrenado.

---

## Descripción general del proyecto

El proyecto integra un flujo completo de MLOps:

1. **Notebook CRISP-DM** — Exploración de datos, reconstrucción de pipelines de preprocesamiento, validación del modelo y exportación de artefactos.
2. **FastAPI App** — API REST que consume los artefactos exportados para realizar predicciones individuales por siniestro.
3. **Docker** — La aplicación se empaqueta en una imagen Docker para garantizar portabilidad y reproducibilidad del entorno.
4. **Artefacto GHCR** — La imagen Docker se publica automáticamente en GitHub Container Registry (GHCR) mediante un workflow de CI/CD con GitHub Actions.
5. **Monitoreo** — Cada consulta a la API queda registrada en un archivo de log `.csv` para seguimiento y evaluación del rendimiento del modelo.
6. **Stress Test** — Se validó el rendimiento del servicio mediante 10 consultas en paralelo con Postman (ver sección Stress Test).

---

## Ejecutar en local

### Requisitos

- Docker instalado ([https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/))

### Pasos

**1 — Descargar la imagen desde GHCR**

```bash
docker pull ghcr.io/themidnightguy/api_taller:latest
```

**2 — Levantar el contenedor**

```bash
docker run -d \
  --name api_taller \
  -p 4000:4000 \
  ghcr.io/themidnightguy/api_taller:latest
```

**3 — Verificar que está corriendo**

```bash
docker ps
```

Output esperado:
```
CONTAINER ID   IMAGE                                      STATUS         PORTS
xxxxxxxxxxxx   ghcr.io/themidnightguy/api_taller:latest  Up X seconds   0.0.0.0:4000->4000/tcp
```

**4 — Acceder a la API**

```
Swagger UI:  http://localhost:4000/docs
Endpoint:    POST http://localhost:4000/predict
Health:      GET  http://localhost:4000/

Puedes probar con http://127.0.0.1:4000/ igualmente
```

**5 — Detener el contenedor**

```bash
docker stop api_taller
```

**6 — Eliminar el contenedor (opcional)**

```bash
docker rm api_taller
```

---

## Documentación de la API

### `GET /`

Verifica que el servicio esté activo.

**Response:**
```json
{
  "mensaje": "Bienvenido! dirigete a /predict para consultar datos sobre siniestros.",
  "status": "ok"
}
```

---

### `POST /predict`

Recibe los datos de un siniestro y retorna la predicción de semanas en taller.

**Request body:**

| Campo | Descripción |
|---|---|
| `claim_id` | ID del siniestro |
| `marca_vehiculo` | Marca del vehículo (`ferd`, `fait`, `chepy`). Si es null se imputa. |
| `antiguedad_vehiculo` | Años desde fabricación hasta el siniestro |
| `tipo_poliza` | Tipo de póliza (1–5). Si es `4` retorna `-1`. |
| `taller` | ID del taller (1–5) |
| `partes_a_reparar` | Número de partes a reparar |
| `partes_a_reemplazar` | Número de partes a reemplazar |

**Ejemplo de request:**
```json
{
  "claim_id": 561205,
  "marca_vehiculo": "ferd",
  "antiguedad_vehiculo": 1,
  "tipo_poliza": 1,
  "taller": 4,
  "partes_a_reparar": 3,
  "partes_a_reemplazar": 2
}
```

**Ejemplo de response:**
```json
{
  "claim_id": 561205,
  "prediccion_semanas": 4.38
}
```

**Regla de negocio — tipo_poliza 4:**
```json
{
  "claim_id": 408550,
  "prediccion_semanas": -1
}
```

**Códigos de respuesta:**

| Código | Descripción |
|---|---|
| `200` | Predicción exitosa |
| `422` | Error de validación en el body |

---

## Log de la API

Cada consulta realizada al endpoint `/predict` queda registrada en `logs/api_requests.log` con el siguiente formato:

```
2025-01-01 12:00:00 | INFO | claim_id=561205 | marca=ferd | tipo_poliza=1 | taller=4 | prediccion=4.38
```

Este archivo permite monitorear el rendimiento del modelo y hacer seguimiento de las predicciones realizadas sobre los registros del dataset `claims_dataset.csv`.

---

## Stress Test

Se realizó un stress test de 10 consultas en paralelo utilizando **Postman Collection Runner**.

**Resultados:**

| Métrica | Valor |
|---|---|
| Total de tests | 40 / 40 ✅ |
| Tests fallidos | 0 |
| Tiempo promedio por request | ~12 seg |
| Tiempo total (10 iteraciones) | ~120 seg |

El tiempo de respuesta (12 segundos) es determinante: corresponde a `time.sleep(2)` en el pipeline de normalización y `time.sleep(10)` en el pipeline de reclamos, definidos en el modelo original entregado por el Data Scientist.

---

## CI/CD — GitHub Actions

El workflow `.github/workflows/docker-publish.yml` se ejecuta en cada push a `main` y realiza automáticamente:

1. Login en GHCR con `GITHUB_TOKEN`
2. Build de la imagen Docker
3. Push de la imagen a `ghcr.io/themidnightguy/api_taller:latest`

---