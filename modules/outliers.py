import pandas as pd

def detectar_outliers(df, salida="outputs/outliers.xlsx"):

    excluir = [
        "observeddate",
        "createddate",
        "latitude",
        "longitude",
        "ica"
    ]

    numericas = [
        c for c in df.select_dtypes(include="number").columns
        if c not in excluir and not c.startswith("s_")
    ]

    hallazgos = []

    for col in numericas:

        serie = df[col].dropna()

        if len(serie) < 5:
            continue

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1

        li = q1 - 1.5 * iqr
        ls = q3 + 1.5 * iqr

        mask = (df[col] < li) | (df[col] > ls)

        temp = df.loc[mask, ["comunidad_final", col]].copy()

        if len(temp) == 0:
            continue

        temp = temp.rename(columns={col: "valor"})
        temp["variable"] = col
        temp["lim_inf"] = li
        temp["lim_sup"] = ls

        hallazgos.append(
            temp[
                [
                    "comunidad_final",
                    "variable",
                    "valor",
                    "lim_inf",
                    "lim_sup"
                ]
            ]
        )

    if hallazgos:
        final = pd.concat(hallazgos, ignore_index=True)
    else:
        final = pd.DataFrame()

    final.to_excel(salida, index=False)

    print("✅ Outliers detectados:", salida)

    return final