import pandas as pd
from scipy.stats import shapiro

def pruebas_normalidad(df, salida="outputs/normalidad.xlsx"):

    excluir = [
        "observeddate",
        "createddate",
        "latitude",
        "longitude",
        "ica",
        "s_ph",
        "s_turbidez",
        "s_tds",
        "s_hierro",
        "s_plomo",
        "s_manganeso",
        "s_cloro"
    ]

    numericas = df.select_dtypes(include="number").columns

    resultados = []

    for col in numericas:

        if col in excluir:
            continue

        serie = df[col].dropna()

        if len(serie) < 3:
            continue

        muestra = serie.sample(min(len(serie), 5000), random_state=42)

        try:
            stat, p = shapiro(muestra)

            resultados.append({
                "variable": col,
                "n": len(serie),
                "W": stat,
                "p_value": p,
                "distribucion": "Normal" if p > 0.05 else "No normal",
                "recomendada": "ANOVA" if p > 0.05 else "Kruskal"
            })

        except:
            pass

    final = pd.DataFrame(resultados)
    final.to_excel(salida, index=False)

    print("✅ Normalidad evaluada:", salida)

    return final