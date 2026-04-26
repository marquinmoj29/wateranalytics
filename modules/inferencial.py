import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def anova_tukey(df, grupo="comunidad_final", salida="outputs/anova_tukey.xlsx"):

    if grupo not in df.columns:
        print(f"❌ No existe columna grupo: {grupo}")
        return

    # Forzar columna simple
    grupo_col = df[grupo].astype(str)

    numericas = df.select_dtypes(include="number").columns.tolist()

    resultados = []

    writer = pd.ExcelWriter(salida, engine="openpyxl")

    for col in numericas:

        try:
            temp = pd.DataFrame({
                grupo: grupo_col,
                col: df[col]
            }).dropna()

            if temp.empty:
                continue

            n_grupos = temp[grupo].nunique()

            if n_grupos < 2:
                continue

            grupos = [g[col].values for _, g in temp.groupby(grupo)]

            if len(grupos) < 2:
                continue

            stat, p = f_oneway(*grupos)

            resultados.append({
                "variable": col,
                "F": stat,
                "p_value": p
            })

            if p < 0.05:

                tukey = pairwise_tukeyhsd(
                    endog=temp[col],
                    groups=temp[grupo],
                    alpha=0.05
                )

                tukey_df = pd.DataFrame(
                    tukey.summary().data[1:],
                    columns=tukey.summary().data[0]
                )

                hoja = col[:30]
                tukey_df.to_excel(writer, sheet_name=hoja, index=False)

        except Exception as e:
            print(f"⚠️ Error en {col}: {e}")

    pd.DataFrame(resultados).to_excel(writer, sheet_name="ANOVA", index=False)

    writer.close()

    print("✅ ANOVA + Tukey exportado:", salida)