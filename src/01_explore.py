"""
Módulo 1 - Parte A: Exploración inicial del dataset de RRHH.

Objetivo: entender la estructura, tipos de datos, valores nulos y
distribución general del dataset antes de limpiarlo.
"""

import pandas as pd

DATA_PATH = "data/HR-Employee-Attrition.csv"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Carga el dataset crudo de RRHH."""
    df = pd.read_csv(path)
    return df


def explore(df: pd.DataFrame) -> None:
    """Imprime un resumen exploratorio del dataset."""
    print("=" * 60)
    print("DIMENSIONES DEL DATASET")
    print("=" * 60)
    print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}\n")

    print("=" * 60)
    print("TIPOS DE DATOS")
    print("=" * 60)
    print(df.dtypes.value_counts(), "\n")

    print("=" * 60)
    print("VALORES NULOS POR COLUMNA")
    print("=" * 60)
    nulls = df.isnull().sum()
    print(nulls[nulls > 0] if nulls.sum() > 0 else "Sin valores nulos.\n")

    print("=" * 60)
    print("COLUMNAS CONSTANTES (candidatas a eliminar)")
    print("=" * 60)
    constantes = [col for col in df.columns if df[col].nunique() == 1]
    print(constantes if constantes else "No hay columnas constantes.")

    print("\n" + "=" * 60)
    print("COLUMNAS TIPO ID (candidatas a eliminar)")
    print("=" * 60)
    posibles_ids = [col for col in df.columns if df[col].nunique() == df.shape[0]]
    print(posibles_ids if posibles_ids else "No se detectaron columnas tipo ID.")
    
    
    print("\n" + "=" * 60)
    print("TASA DE ROTACIÓN (ATTRITION) GENERAL")
    print("=" * 60)
    tasa = df["Attrition"].value_counts(normalize=True) * 100
    print(tasa.round(2))


if __name__ == "__main__":
    df = load_data()
    explore(df)