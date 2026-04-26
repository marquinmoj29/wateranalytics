import streamlit as st
import pandas as pd
import plotly.express as px
import os

from modules.loader import cargar_excel_nivel_dios
from modules.cleaning import limpiar_dataframe
from modules.ica import calcular_ica

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(
    page_title="WaterAnalytics Pro",
    page_icon="💧",
    layout="wide"
)

# ----------------------------
# CSS PREMIUM
# ----------------------------
st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#07111f,#0d1f38);
    color:white;
}

[data-testid="stSidebar"]{
    background:#0b1728;
}

h1,h2,h3,label,p,span{
    color:white !important;
}

.block-container{
    padding-top:1.5rem;
}

div[data-baseweb="select"] *{
    color:black !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# RUTAS BASE
# ----------------------------
BASE_DIR = os.path.dirname(__file__)

# ----------------------------
# DATA
# ----------------------------
ruta = os.path.join(BASE_DIR, "data", "planilla.xlsx")

df = cargar_excel_nivel_dios(ruta)
df = limpiar_dataframe(df)

df, resumen_ica = calcular_ica(df)

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("⚙️ Filtros")

comunidades = sorted(df["comunidad_final"].dropna().unique())

com = st.sidebar.selectbox(
    "Comunidad",
    ["Todas"] + comunidades
)

if com != "Todas":
    df = df[df["comunidad_final"] == com]

# ----------------------------
# HEADER
# ----------------------------
st.title("💧 WaterAnalytics Pro")
st.caption("Environmental Intelligence Platform")

# ----------------------------
# KPIs
# ----------------------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("Muestras", len(df))
k2.metric("Comunidades", df["comunidad_final"].nunique())
k3.metric("Variables", df.shape[1])
k4.metric("ICA Promedio", round(df["ICA"].mean(), 1))

# ----------------------------
# VARIABLES
# ----------------------------
excluir = [
    "observeddate",
    "createddate",
    "latitude",
    "longitude",
    "ICA"
]

num_cols = [
    c for c in df.select_dtypes(include="number").columns
    if c not in excluir and not c.startswith("s_")
]

var = st.selectbox("Parámetro", num_cols)

# ----------------------------
# GRAFICOS
# ----------------------------
c1, c2 = st.columns(2)

with c1:
    fig = px.box(
        df,
        x="comunidad_final",
        y=var,
        color="comunidad_final",
        title=f"{var} por comunidad"
    )

    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig2 = px.histogram(
        df,
        x=var,
        nbins=25,
        title=f"Distribución de {var}"
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# ICA RANKING
# ----------------------------
st.subheader("🏆 Ranking ICA")

fig3 = px.bar(
    resumen_ica,
    x="ICA_promedio",
    y="comunidad_final",
    orientation="h",
    color="ICA_promedio",
    text="categoria"
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# PCA IMAGE
# ----------------------------
img = os.path.join(BASE_DIR, "outputs", "pca_cluster.png")

if os.path.exists(img):
    st.subheader("🧠 Segmentación Inteligente")
    st.image(img, use_container_width=True)

# ----------------------------
# FOOTER
# ----------------------------
st.caption("© 2026 WaterAnalytics Pro | Powered by Python")