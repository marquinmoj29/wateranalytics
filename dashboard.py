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

/* Fondo general */
.stApp{
    background: linear-gradient(135deg,#03101f,#071a33,#0a2747);
    color:white;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#04111f,#08192d);
    border-right:1px solid rgba(255,255,255,0.08);
}

/* Textos */
h1,h2,h3,h4,p,label,span{
    color:white !important;
}

/* Container */
.block-container{
    padding-top:1.2rem;
    max-width: 1400px;
}

/* Selectbox */
div[data-baseweb="select"] > div{
    background:white !important;
    color:black !important;
    border-radius:12px !important;
}

/* Inputs */
input{
    border-radius:12px !important;
}

/* KPI cards visual */
[data-testid="metric-container"]{
    background: rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    padding:18px;
    border-radius:16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

/* Botones */
.stDownloadButton button{
    width:100%;
    border-radius:12px;
    border:none;
    padding:0.65rem 1rem;
    font-weight:700;
    background: linear-gradient(90deg,#0ea5e9,#2563eb);
    color:white;
}

/* Hover */
.stDownloadButton button:hover{
    transform: translateY(-1px);
    transition:0.2s;
}

/* Imagen PCA */
img{
    border-radius:18px;
    box-shadow:0 10px 30px rgba(0,0,0,0.30);
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


UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.sidebar.subheader("📂 Cargar Excel")

archivo = st.sidebar.file_uploader(
    "Sube archivo Excel",
    type=["xlsx", "xls"]
)

if archivo is not None:
    nombre = archivo.name
    ruta_guardado = os.path.join(UPLOAD_DIR, nombre)

    with open(ruta_guardado, "wb") as f:
        f.write(archivo.getbuffer())

# listar históricos
archivos = sorted(os.listdir(UPLOAD_DIR), reverse=True)

seleccion = st.sidebar.selectbox(
    "📅 Historial",
    archivos if archivos else ["Sin archivos"]
)

if archivos:
    ruta = os.path.join(UPLOAD_DIR, seleccion)
else:
    ruta = os.path.join(BASE_DIR, "data", "planilla.xlsx")

df = cargar_excel_nivel_dios(ruta)

df = limpiar_dataframe(df)

df, resumen_ica = calcular_ica(df)

# ----------------------------
# MENU PRINCIPAL
# ----------------------------
modulo = st.sidebar.radio(
    "📚 Módulos",
    [
        "Dashboard Ejecutivo",
        "Limpieza de datos",
        "Descriptiva",
        "Correlación",
        "Inferencial",
        "Outliers",
        "PCA / Clusters",
        "ICA",
        "Reportes",
        "Control de Proceso"
    ]
)

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

if modulo == "Dashboard Ejecutivo":

# ----------------------------
# HEADER
# ----------------------------
st.markdown("# 💧 WaterAnalytics Pro")
st.markdown("### Environmental Intelligence Platform")
st.markdown("---")

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
# DESCARGAS PRO
# ----------------------------
import io

st.subheader("📥 Descargar datos")

buffer = io.BytesIO()
df.to_excel(buffer, index=False, engine="openpyxl")

st.download_button(
    "📄 Descargar Base Procesada",
    data=buffer.getvalue(),
    file_name="wateranalytics_base_procesada.xlsx"
)

buffer2 = io.BytesIO()
resumen_ica.to_excel(buffer2, index=False, engine="openpyxl")

st.download_button(
    "🏆 Descargar Ranking ICA",
    data=buffer2.getvalue(),
    file_name="wateranalytics_ranking_ica.xlsx"
)

# ----------------------------
# PDF EJECUTIVO
# ----------------------------
from modules.reportes import generar_pdf

if st.button("📑 Generar Reporte PDF"):

    generar_pdf(resumen_ica)

    pdf_path = os.path.join(BASE_DIR, "outputs", "reporte_wateranalytics.pdf")

    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Descargar PDF Ejecutivo",
                data=f,
                file_name="WaterAnalytics_Reporte.pdf",
                mime="application/pdf"
            )


elif modulo == "Limpieza de datos":
    st.title("🧼 Limpieza de datos")
    st.dataframe(df.head(100))

elif modulo == "Descriptiva":
    st.title("📈 Estadística Descriptiva")
    st.dataframe(df.describe(include="all"))

elif modulo == "Correlación":
    st.title("📉 Correlación")
    st.dataframe(df.select_dtypes(include="number").corr())

elif modulo == "Inferencial":
    st.title("🧪 Inferencial")
    st.info("Módulo en construcción")

elif modulo == "Outliers":
    st.title("📦 Outliers")
    st.info("Módulo en construcción")

elif modulo == "PCA / Clusters":
    st.title("📐 PCA / Clusters")
    if os.path.exists(img):
        st.image(img, use_container_width=True)

elif modulo == "ICA":
    st.title("💧 ICA")
    st.dataframe(resumen_ica)

elif modulo == "Reportes":
    st.title("📑 Reportes")
    st.info("Excel y PDF disponibles abajo")

elif modulo == "Control de Proceso":
    st.title("⚙️ Control de Proceso")
    st.info("Módulo en construcción")

# ----------------------------
# FOOTER
# ----------------------------
st.caption("© 2026 WaterAnalytics Pro | Powered by Python")