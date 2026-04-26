import pandas as pd

def estadistica_descriptiva(df, salida="outputs/descriptiva.xlsx"):
    
    numericas = df.select_dtypes(include="number")

    resumen = pd.DataFrame({
        "media": numericas.mean(),
        "mediana": numericas.median(),
        "std": numericas.std(),
        "min": numericas.min(),
        "max": numericas.max(),
        "faltantes": numericas.isna().sum(),
        "cv_%": (numericas.std() / numericas.mean()) * 100
    })

    resumen.to_excel(salida)

    print("✅ Estadística descriptiva exportada:", salida)

    return resumen