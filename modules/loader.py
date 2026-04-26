import pandas as pd

def cargar_excel_nivel_dios(ruta):

    hojas = pd.read_excel(ruta, sheet_name=None)

    print("📂 Hojas detectadas:")
    print(list(hojas.keys()))

    frames = []

    hojas_excluir = [
        "TODOS_LOS_DATOS",
        "RESUMEN",
        "DASHBOARD",
        "GRAFICOS"
    ]

    for nombre_hoja, df in hojas.items():

        if df.empty:
            continue

        if nombre_hoja.upper() in [x.upper() for x in hojas_excluir]:
            continue

        # limpiar columnas vacías
        df = df.dropna(axis=1, how="all")

        # ignorar hojas pequeñas
        if len(df) < 2:
            continue

        # Detectar comunidad real dentro del archivo
if "Comunidad" in df.columns:
    df["comunidad_final"] = df["Comunidad"]

elif "comunidad" in df.columns:
    df["comunidad_final"] = df["comunidad"]

elif "locationName" in df.columns:
    df["comunidad_final"] = df["locationName"]

else:
    df["comunidad_final"] = nombre_hoja.strip()

        frames.append(df)

        print(f"✅ Hoja cargada: {nombre_hoja} ({df.shape[0]} filas)")

    if len(frames) == 0:
        raise ValueError("❌ No se encontraron hojas válidas.")

    final = pd.concat(frames, ignore_index=True, sort=False)

    print("🔥 Base unificada creada")

    return final