"""
Módulo 2: Cálculo de KPIs de RRHH y correlaciones.

Objetivo: identificar patrones y tendencias en los datos de personas
"identificar patrones, tendencias y correlaciones en los datos de personas
para generar diagnósticos relevantes".

Trabaja sobre el dataset ya limpio (data/HR-Employee-Attrition-clean.csv).
"""

import pandas as pd

DATA_PATH = "data/HR-Employee-Attrition-clean.csv"


def load_clean_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Carga el dataset ya limpio (salida del Módulo 1)."""
    return pd.read_csv(path)


def rotacion_por_departamento(df: pd.DataFrame) -> pd.Series:
    """Tasa de rotación (%) agrupada por departamento."""
    return (
        df.groupby("Department")["AttritionFlag"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )


def rotacion_por_rol(df: pd.DataFrame) -> pd.Series:
    """Tasa de rotación (%) agrupada por rol/cargo."""
    return (
        df.groupby("JobRole")["AttritionFlag"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )


def rotacion_por_overtime(df: pd.DataFrame) -> pd.Series:
    """Tasa de rotación (%) según si el empleado hace horas extra."""
    return (
        df.groupby("OverTime")["AttritionFlag"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )


def brecha_salarial_genero(df: pd.DataFrame) -> pd.Series:
    """Ingreso mensual promedio por género."""
    return df.groupby("Gender")["MonthlyIncome"].mean().round(0)


def brecha_salarial_nivel(df: pd.DataFrame) -> pd.DataFrame:
    """Ingreso mensual promedio por nivel de puesto (JobLevel) y género."""
    return (
        df.groupby(["JobLevel", "Gender"])["MonthlyIncome"]
        .mean()
        .round(0)
        .unstack()
    )


def satisfaccion_vs_rotacion(df: pd.DataFrame) -> pd.Series:
    """Tasa de rotación (%) según nivel de satisfacción laboral (1=Baja, 4=Muy alta)."""
    return (
        df.groupby("JobSatisfaction")["AttritionFlag"]
        .mean()
        .mul(100)
        .round(2)
    )


def correlaciones_con_rotacion(df: pd.DataFrame, top_n: int = 8) -> pd.Series:
    """Variables numéricas más correlacionadas (en valor absoluto) con la rotación."""
    numericas = df.select_dtypes(include="number")
    corr = numericas.corr()["AttritionFlag"].drop("AttritionFlag")
    return corr.reindex(corr.abs().sort_values(ascending=False).index).head(top_n).round(3)


def resumen(df: pd.DataFrame) -> None:
    print("=" * 60)
    print("1. TASA DE ROTACIÓN POR DEPARTAMENTO (%)")
    print("=" * 60)
    print(rotacion_por_departamento(df), "\n")

    print("=" * 60)
    print("2. TASA DE ROTACIÓN POR ROL (%)")
    print("=" * 60)
    print(rotacion_por_rol(df), "\n")

    print("=" * 60)
    print("3. TASA DE ROTACIÓN SEGÚN HORAS EXTRA (OverTime) (%)")
    print("=" * 60)
    print(rotacion_por_overtime(df), "\n")

    print("=" * 60)
    print("4. INGRESO MENSUAL PROMEDIO POR GÉNERO")
    print("=" * 60)
    print(brecha_salarial_genero(df), "\n")

    print("=" * 60)
    print("5. INGRESO MENSUAL PROMEDIO POR NIVEL DE PUESTO Y GÉNERO")
    print("=" * 60)
    print(brecha_salarial_nivel(df), "\n")

    print("=" * 60)
    print("6. TASA DE ROTACIÓN SEGÚN SATISFACCIÓN LABORAL (%)")
    print("=" * 60)
    print(satisfaccion_vs_rotacion(df), "\n")

    print("=" * 60)
    print("7. TOP VARIABLES CORRELACIONADAS CON LA ROTACIÓN")
    print("=" * 60)
    print(correlaciones_con_rotacion(df))


if __name__ == "__main__":
    df = load_clean_data()
    resumen(df)