# Segmentación de Usuarios de Streaming

Proyecto E3 — SCY1101 Programación para la Ciencia de Datos 

Pipeline end-to-end que integra datos de consumo y perfil de usuarios de una
plataforma de streaming, construye un modelo de segmentación con KMeans y
expone los resultados en un dashboard interactivo.

## Integrantes

- Verónica Cereceda
- Diego Torres
- Cristian Urcullú

## Contexto del problema

Ver [`docs/contexto_negocio.md`](docs/contexto_negocio.md) para el detalle completo
del caso de negocio y las fuentes de datos.

En resumen: se busca identificar segmentos de usuarios con comportamientos
similares (consumo, gasto, antigüedad, uso de promociones, etc.) para diseñar
estrategias diferenciadas de retención y recomendación.

## Arquitectura

```
usuarios_streaming.csv ─┐
perfil_usuarios.csv → Postgres ─┼─→ etl/extract.py (extraer + integrar)
                                                     │
                                                     ▼
                                       dataset consolidado de usuarios
                                                     │
                                                     ▼
                              escalamiento → KMeans (k óptimo vía codo + silhouette)
                                                     │
                                                     ▼
                                    dashboard interactivo (Streamlit)
```

Diagrama completo en [`docs/arquitectura.md`](docs/arquitectura.md).

## Estructura del repositorio

```
.
├── etl/            # Pipeline de extracción e integración de fuentes
├── model/          # Entrenamiento de KMeans, selección de k, perfilamiento de clusters
├── api/            # API REST que expone el modelo entrenado (FastAPI)
├── dashboards/     # Dashboard interactivo
├── tests/          # Pruebas automatizadas
├── docker/         # Dockerfiles
├── database/       # init.sql y carga de perfil_usuarios en Postgres
├── docs/           # Documentación técnica y de negocio
└── data/
```

## Cómo correr el proyecto

### Opción A: entorno local

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Luego ver [`docs/guia_despliegue.md`](docs/guia_despliegue.md) para los pasos
de configuración de Postgres y variables de entorno.

### Opción B: Docker (recomendado para la demo)

```bash
docker compose up --build
```

> Nota: la configuración por variables de entorno (`.env`) todavía no está
> implementada — es una mejora pendiente. Por ahora, las credenciales de
> Postgres están definidas directamente en `docker-compose.yml`.

## Flujo de trabajo en Git

Cada integrante trabaja en su propia rama (`feature/<nombre-de-la-parte>`) y
todo cambio llega a `main` mediante Pull Request con revisión de al menos otro
integrante. Ver [`docs/guia_contribucion.md`](docs/guia_contribucion.md).