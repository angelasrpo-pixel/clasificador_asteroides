
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
    r = requests.get(url, params=params, timeout=60)
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

st.sidebar.header("Filtros")

clases = ["Todas"] + sorted(df["class"].dropna().unique().tolist())
clase_sel = st.sidebar.selectbox("Clase orbital", clases)

solo_pha = st.sidebar.checkbox("Solo PHAs")

h_min, h_max = st.sidebar.slider(
    "Rango de magnitud H",
    min_value=df["H"].min(),
    max_value=df["H"].max(),
    value=(float(df["H"].min()), 25.0)
)

df_filtrado = df.copy()

if clase_sel != "Todas":
    df = df[df["class"] == clase_sel]

if solo_pha:
    df = df[df["pha"] == "Y"]

df_filtrado = df_filtrado[(df_filtrado["H"] >= h_min) & (df_filtrado["H"] <= h_max)]

st.sidebar.markdown(f"**{len(df_filtrado):,} asteroides** con estos filtros")

tab1, tab2, tab3 = st.tabs(["📋 Catálogo", "🗺️ Mapas", "🔍 Ficha"])

with tab1:
    st.subheader("Catálogo de Asteroides NEA")
    columnas = ["nombre", "H", "albedo", "diameter", "moid", "class", "pha"]
    st.dataframe(
        df_filtrado[columnas].rename(columns={
            "nombre"   : "Nombre",
            "H"        : "Mag. H",
            "albedo"   : "Albedo",
            "diameter" : "Diámetro (km)",
            "moid"     : "MOID (UA)",
            "class"    : "Clase",
            "pha"      : "PHA"
        }),
        use_container_width = True,
        height              = 500
    )

