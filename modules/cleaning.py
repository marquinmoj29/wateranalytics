import pandas as pd

COLUMNAS_TECNICAS = [
    "observeddate",
    "createddate",
    "latitude",
    "longitude",
    "datasheetname"
]

def limpiar_columnas(df):
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )

    # eliminar columnas duplicadas conservando la primera
    df = df.loc[:, ~df.columns.duplicated()]

    return df

def convertir_fechas(df):
    for col in ["observeddate", "createddate"]:
        if col in df.columns:
            s = pd.to_numeric(df[col], errors="coerce")
            df[col] = pd.to_datetime(s, unit="us", errors="coerce")
    return df


def convertir_numericas(df):
    excluir = {
        "comunidad_final",
        "nombre",
        "fuente_de_agua"
    }

    for col in df.columns:
        if col in excluir:
            continue

        conv = pd.to_numeric(df[col], errors="coerce")

        if conv.notna().sum() > 0:
            df[col] = conv

    return df


def eliminar_muy_vacias(df, umbral=0.80):
    ratio = df.isna().mean()
    borrar = ratio[ratio > umbral].index.tolist()

    if borrar:
        df = df.drop(columns=borrar)

    print("🧹 Eliminadas vacías:", borrar)

    return df


def limpiar_dataframe(df):
    df = limpiar_columnas(df)
    df = convertir_fechas(df)
    df = convertir_numericas(df)
    df = eliminar_muy_vacias(df)

    return df