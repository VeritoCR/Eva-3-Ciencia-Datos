"""
Extracción e integración de las dos fuentes de datos del proyecto.

Fuente 1: usuarios_streaming.csv  (archivo plano, datos de consumo)
Fuente 2: perfil_usuarios         (tabla en Postgres, datos de perfil)

Ambas se unen por id_cliente para formar el dataset consolidado.
"""
import pandas as pd
from sqlalchemy import create_engine


def extraer_csv(ruta="data/usuarios_streaming.csv"):
    """Lee la fuente 1: el CSV de consumo de streaming."""
    df = pd.read_csv(ruta)
    print(f"CSV leído: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def extraer_postgres():
    """Lee la fuente 2: la tabla perfil_usuarios desde Postgres."""
    engine = create_engine("postgresql://admin:admin@postgres:5432/streaming_db")
    df = pd.read_sql("SELECT * FROM perfil_usuarios", engine)
    print(f"Postgres leído: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def integrar(df_streaming, df_perfil):
    """Une las dos fuentes por id_cliente."""
    data = df_streaming.merge(df_perfil, on="id_cliente")
    print(f"Datos integrados: {data.shape[0]} filas, {data.shape[1]} columnas")
    return data


if __name__ == "__main__":
    # Flujo de extracción: leer ambas fuentes y unirlas
    streaming = extraer_csv()
    perfil = extraer_postgres()
    data = integrar(streaming, perfil)

    # Guardar el dataset consolidado para que el modelo lo use
    data.to_csv("data/data_consolidada.csv", index=False)
    print("Dataset consolidado guardado en data/data_consolidada.csv")
