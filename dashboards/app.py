"""
Dashboard de segmentación de usuarios de streaming.

Consume la API (api/main.py) vía HTTP — no accede directamente a archivos
del modelo ni de Postgres. Esto mantiene al dashboard como un cliente puro
de la API, respetando la separación entre servicios.
"""
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("Segmentación de Usuarios — Streaming")

# Obtener todo lo necesario desde la API en una sola llamada
respuesta = requests.get("http://api:8000/dashboard-data")
payload = respuesta.json()

data = pd.DataFrame(payload["usuarios"])
metricas = payload["metricas"]
centroides = pd.DataFrame(payload["centroides"])

# --- Métricas del modelo ---
st.subheader("Métricas del modelo")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Silhouette Score", f"{metricas['silhouette_score']:.3f}")
with col2:
    st.metric("Clusters", metricas["n_clusters"])
with col3:
    st.metric("Usuarios", metricas["n_usuarios"])

# --- Tabla de usuarios segmentados ---
st.subheader("Usuarios segmentados")
st.dataframe(data)

# --- Distribución de segmentos ---
st.subheader("Distribución de segmentos")
st.bar_chart(data["cluster"].value_counts())

# --- Perfil de cada segmento (con las variables de streaming) ---
perfil_segmentos = data.groupby("cluster").agg(
    usuarios=("id_cliente", "count"),
    horas_consumo_promedio=("horas_consumo_mensual", "mean"),
    gasto_promedio=("gasto_mensual", "mean"),
    contenidos_vistos_promedio=("cantidad_contenidos_vistos", "mean"),
    antiguedad_promedio=("antiguedad_cliente_meses", "mean"),
    uso_promociones_promedio=("porcentaje_uso_promociones", "mean"),
    dispositivos_promedio=("dispositivos_registrados", "mean"),
).round(2)

st.subheader("Perfil de segmentos")
st.dataframe(perfil_segmentos)

# --- Visualización PCA ---
st.subheader("Visualización PCA de los segmentos")
fig, ax = plt.subplots(figsize=(8, 6))

for cluster in sorted(data["cluster"].unique()):
    subset = data[data["cluster"] == cluster]
    ax.scatter(subset["pc1"], subset["pc2"], label=f"Cluster {cluster}", alpha=0.7)

ax.set_title("Segmentos proyectados con PCA")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.legend()
ax.grid(True)
st.pyplot(fig)
