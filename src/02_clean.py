"""
Módulo 1 - Parte B: Limpieza y preparación del dataset de RRHH.

Objetivo: dejar un dataset "processed" listo para el cálculo de KPIs
(Módulo 2), eliminando columnas sin valor analítico y normalizando
nombres/tipos.
"""

import pandas as pd

RAW_PATH = "data/HR-Employee-Attrition.csv"
PROCESSED_PATH = "data/HR-Employee-Attrition-clean.csv"

# Columnas constantes o sin valor analítico (detectadas en 01_explore.py)
COLUMNS_TO_DROP = ["EmployeeCount", "Over18", "StandardHours", "EmployeeNumber"]


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia el dataset: elimina columnas irrelevantes y normaliza tipos."""
    df = df.drop(columns=[c for c in COLUMNS_TO_DROP if c in df.columns])

    # Normalizar Attrition a booleano explícito (además de mantener texto)
    df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)

    # Verificación de duplicados
    duplicados = df.duplicated().sum()
    if duplicados > 0:
        df = df.drop_duplicates()

    return df


def save(df: pd.DataFrame, path: str = PROCESSED_PATH) -> None:
    df.to_csv(path, index=False)


if __name__ == "__main__":
    df_raw = load_raw()
    df_clean = clean(df_raw)
    save(df_clean)

    print(f"Dataset original: {df_raw.shape[1]} columnas")
    print(f"Dataset limpio:   {df_clean.shape[1]} columnas")
    print(f"Columnas eliminadas: {COLUMNS_TO_DROP}")
    print(f"Guardado en: {PROCESSED_PATH}")