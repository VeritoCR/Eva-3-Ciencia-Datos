"""
Entrenamiento del modelo de segmentación KMeans.

Lee el dataset consolidado (producido por etl/extract.py), escala las
variables, determina el número óptimo de clusters con el método del codo
(KneeLocator) confirmado con Silhouette, entrena el modelo final y guarda:
  - el modelo, el scaler y el PCA (para que la API los use)
  - el dataset con clusters asignados (para el dashboard)
  - las métricas y los centroides
"""
import pandas as pd
import json
import pickle
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from kneed import KneeLocator
from sklearn.decomposition import PCA

os.makedirs("models", exist_ok=True)

# 1. Leer el dataset consolidado que dejó el ETL
data = pd.read_csv("data/data_consolidada.csv")

# 2. Preparar las variables del modelo (quitar el identificador)
X = data.drop(columns=["id_cliente"])

# 3. Escalamiento
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Probar k de 2 a 10, guardando inercia y silhouette de cada uno
inertias = []
silhouettes = []
for k in range(2, 11):
    modelo = KMeans(n_clusters=k, random_state=29, n_init=10)
    modelo.fit(X_scaled)
    inertias.append(modelo.inertia_)
    silhouettes.append(silhouette_score(X_scaled, modelo.labels_))

# 5. Elegir el k óptimo con el método del codo (automático)
kl = KneeLocator(range(2, 11), inertias, curve="convex", direction="decreasing")
k_optimo = kl.elbow

# 6. Entrenar el modelo final con el k óptimo
kmeans = KMeans(n_clusters=k_optimo, random_state=29, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
data["cluster"] = clusters
print(f"Modelo entrenado con k={k_optimo}")

# 7. PCA a 2 componentes, solo para visualización
pca = PCA(n_components=2)
componentes = pca.fit_transform(X_scaled)
data["pc1"] = componentes[:, 0]
data["pc2"] = componentes[:, 1]

# 8. Guardar el dataset con clusters (lo usa el dashboard)
data.to_csv("data/usuarios_segmentados.csv", index=False)

# 9. Guardar métricas
metricas = {
    "k_optimo": int(k_optimo),
    "silhouette_score": float(silhouette_score(X_scaled, data["cluster"])),
    "n_usuarios": int(len(data)),
    "n_clusters": int(k_optimo),
    "varianza_pca": float(pca.explained_variance_ratio_.sum()),
}
with open("models/metricas.json", "w") as f:
    json.dump(metricas, f, indent=4)

# 10. Guardar centroides en la escala original (interpretables)
centroides_original = scaler.inverse_transform(kmeans.cluster_centers_)
centroides_df = pd.DataFrame(centroides_original, columns=X.columns)
centroides_df.to_csv("data/centroides.csv", index=False)

# 11. Guardar modelo, scaler y PCA (los usa la API)
pickle.dump(kmeans, open("models/modelo_kmeans.pkl", "wb"))
pickle.dump(scaler, open("models/scaler.pkl", "wb"))
pickle.dump(pca, open("models/pca.pkl", "wb"))

print("Modelo, métricas y centroides guardados")
