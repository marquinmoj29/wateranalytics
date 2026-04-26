import pandas as pd
import numpy as np

def score_inverso(valor, ideal, maximo, peso=1):
    if pd.isna(valor):
        return np.nan

    if valor <= ideal:
        return 100

    if valor >= maximo:
        return 0

    score = 100 * (1 - (valor - ideal) / (maximo - ideal))
    return score * peso


def score_rango(valor, minimo, maximo, peso=1):
    if pd.isna(valor):
        return np.nan

    if minimo <= valor <= maximo:
        return 100 * peso

    dist = min(abs(valor - minimo), abs(valor - maximo))
    penal = min(dist * 20, 100)

    return (100 - penal) * peso


def calcular_ica(df, salida="outputs/ica.xlsx"):

    d = df.copy()

    d["s_ph"] = d["ph"].apply(lambda x: score_rango(x, 6.5, 8.5, 1.2)) if "ph" in d.columns else np.nan

    d["s_turbidez"] = d["turbidez_ntu"].apply(
        lambda x: score_inverso(x, 1, 10, 1.3)
    ) if "turbidez_ntu" in d.columns else np.nan

    d["s_tds"] = d["tds"].apply(
        lambda x: score_inverso(x, 300, 1000, 1.0)
    ) if "tds" in d.columns else np.nan

    d["s_hierro"] = d["hierro_ppm"].apply(
        lambda x: score_inverso(x, 0.3, 1.5, 1.4)
    ) if "hierro_ppm" in d.columns else np.nan

    d["s_plomo"] = d["plomo_ppm"].apply(
        lambda x: score_inverso(x, 0.01, 0.05, 2.0)
    ) if "plomo_ppm" in d.columns else np.nan

    d["s_manganeso"] = d["manganeso_ppm"].apply(
        lambda x: score_inverso(x, 0.1, 0.5, 1.5)
    ) if "manganeso_ppm" in d.columns else np.nan

    d["s_cloro"] = d["cloro_libre_ppm"].apply(
        lambda x: score_rango(x, 0.2, 1.0, 1.2)
    ) if "cloro_libre_ppm" in d.columns else np.nan

    scores = [c for c in d.columns if c.startswith("s_")]

    d["ICA"] = d[scores].mean(axis=1)

    def clasif(x):
        if pd.isna(x): return "Sin dato"
        if x >= 90: return "Excelente"
        if x >= 75: return "Buena"
        if x >= 60: return "Regular"
        if x >= 40: return "Mala"
        return "Crítica"

    d["categoria_ica"] = d["ICA"].apply(clasif)

    resumen = (
        d.groupby("comunidad_final")
        .agg(
            ICA_promedio=("ICA", "mean"),
            categoria=("categoria_ica", lambda x: x.mode().iloc[0] if len(x.mode()) else "NA")
        )
        .reset_index()
        .sort_values("ICA_promedio", ascending=False)
    )

    resumen.to_excel(salida, index=False)

    print("✅ ICA calculado:", salida)

    return d, resumen