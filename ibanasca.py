
# Importar librerias
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests

# Configuramos la pantalla de la app
st.set_page_config(
    page_title="Ibanasca - Defensa Planetaria de Dr.Z Academy",
    page_icon="🪨",
    layout="wide"
)

#Cargamos los datos
@st.cache_data  # Para guardar el resultado en la memoria
def cargar_datos():
    url = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
    campos = "full_name,H,albedo,diameter,moid,e,a,i,class,neo,pha"
    params = {
        "fields"   : campos,
        "sb-kind" : "a",
        "sb-group": "neo",

    }
    r = request.get(url, params=params, timeout=60)
    df = pd.DataFrame(r.json()["data"], columns=r.json()["fields"])

    for col in ["H", "albedo", "diameter", "moid", "e", "a", "i"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["nombre"] = df["full_name"].str.strip()

    return df

# st.spinner muestra un mensaje mientras espera la descarga
with st.spinner("Descargando catálogo del JPL..."):
    df = cargar_datos()

st.title("Ibanasca - Defensa planetaria de Dr.Z Academy")
st.caption(f"Catálogo JPL - {len(df):,} asteroides NEA")
