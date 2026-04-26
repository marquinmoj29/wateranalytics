import os
import matplotlib.pyplot as plt
import pandas as pd

def control_proceso(df, variable="ph", carpeta="outputs"):

    if variable not in df.columns:
        print("❌ Variable no encontrada")
        return

    serie = df[variable].dropna().reset_index(drop=True)

    if len(serie) < 5:
        print("❌ Pocos datos")
        return

    media = serie.mean()
    std = serie.std()

    ucl = media + 3 * std
    lcl = media - 3 * std

    plt.figure(figsize=(12,6))

    plt.plot(serie.index, serie.values, marker="o")
    plt.axhline(media, linestyle="--", label="Media")
    plt.axhline(ucl, linestyle="--", label="UCL (+3σ)")
    plt.axhline(lcl, linestyle="--", label="LCL (-3σ)")

    plt.title(f"Control de Proceso - {variable}")
    plt.xlabel("Muestra")
    plt.ylabel(variable)
    plt.legend()
    plt.tight_layout()

    ruta = os.path.join(carpeta, f"control_{variable}.png")
    plt.savefig(ruta, dpi=300)
    plt.close()

    print("✅ Control chart generado:", ruta)