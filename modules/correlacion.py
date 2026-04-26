import os
import matplotlib.pyplot as plt
import pandas as pd

def analisis_correlacion(df, carpeta="outputs"):

    vars_ok = [
        "ph",
        "conductividad_eléctrica_uscm",
        "tds",
        "turbidez_ntu",
        "hierro_ppm",
        "plomo_ppm",
        "manganeso_ppm",
        "nitrato_ppm",
        "sulfato",
        "temperatura_°c",
        "cloro_libre_ppm"
    ]

    cols = [c for c in vars_ok if c in df.columns]

    num = df[cols].copy()

    corr = num.corr(method="spearman")

    plt.figure(figsize=(10,7))
    plt.imshow(corr)
    plt.colorbar()

    plt.xticks(range(len(cols)), cols, rotation=45, ha="right")
    plt.yticks(range(len(cols)), cols)

    plt.title("Correlación Ejecutiva")
    plt.tight_layout()

    ruta = os.path.join(carpeta, "heatmap_ejecutivo.png")
    plt.savefig(ruta, dpi=300)
    plt.close()

    print("✅ Heatmap ejecutivo creado")