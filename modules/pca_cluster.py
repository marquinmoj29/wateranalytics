import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def pca_cluster(df, carpeta="outputs"):

    os.makedirs(carpeta, exist_ok=True)

    numericas = df.select_dtypes(include="number")

    # quitar columnas muy vacías
    numericas = numericas.dropna(axis=1, thresh=len(df)*0.5)

    # rellenar faltantes con media
    X = numericas.fillna(numericas.mean())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    comp = pca.fit_transform(X_scaled)

    resultado = pd.DataFrame({
        "PC1": comp[:,0],
        "PC2": comp[:,1],
        "comunidad": df["comunidad_final"].values
    })

    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    resultado["cluster"] = km.fit_predict(comp)

    # exportar excel
    resultado.to_excel(os.path.join(carpeta, "pca_cluster.xlsx"), index=False)

    # gráfico
    plt.figure(figsize=(10,7))

    for c in sorted(resultado["cluster"].unique()):
        sub = resultado[resultado["cluster"] == c]
        plt.scatter(sub["PC1"], sub["PC2"], label=f"Cluster {c}", alpha=0.7)

    for i,row in resultado.iterrows():
        plt.text(row["PC1"], row["PC2"], row["comunidad"], fontsize=7)

    plt.title("PCA + Cluster de Comunidades")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.tight_layout()

    ruta = os.path.join(carpeta, "pca_cluster.png")
    plt.savefig(ruta, dpi=300)
    plt.close()

    print("✅ PCA + Cluster generado")