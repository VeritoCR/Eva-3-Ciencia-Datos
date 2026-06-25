"""
API REST que expone los resultados del modelo de segmentación.

No es una fuente de datos: sirve los resultados ya calculados por
model/train.py (clusters, centroides, métricas) para que el dashboard
(u otro cliente) los consuma vía HTTP.
"""
import pandas as pd
import json
import pickle

from fastapi import FastAPI

app = FastAPI(title="API de Segmentación de Usuarios — Streaming")

# Cargar al iniciar: los resultados que dejó el entrenamiento
modelo = pickle.load(open("models/modelo_kmeans.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

with open("models/metricas.json") as f:
    metricas = json.load(f)


@app.get("/")
def inicio():
    """Endpoint raíz: confirma que el servicio está corriendo."""
    return {"mensaje": "API de segmentación de usuarios funcionando"}


@app.get("/dashboard-data")
def dashboard_data():
    """Devuelve todo lo que el dashboard necesita para graficar:
    usuarios con su cluster asignado, centroides y métricas del modelo."""
    usuarios = pd.read_csv("data/usuarios_segmentados.csv")
    centroides = pd.read_csv("data/centroides.csv")

    return {
        "usuarios": usuarios.to_dict(orient="records"),
        "centroides": centroides.to_dict(orient="records"),
        "metricas": metricas,
    }


@app.post("/predict")
def predict(datos: dict):
    """Clasifica un usuario nuevo: recibe sus variables y devuelve
    a qué cluster pertenece, según el modelo ya entrenado."""
    fila = pd.DataFrame([datos])
    X = scaler.transform(fila)
    cluster = modelo.predict(X)

    return {"cluster": int(cluster[0])}
