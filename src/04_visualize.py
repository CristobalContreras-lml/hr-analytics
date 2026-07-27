"""
Módulo 3: Visualización de KPIs de RRHH.

Objetivo: convertir los KPIs calculados en el Módulo 2 en gráficos claros,
respondiendo al requisito de la publicación de Sodexo sobre "Business
Intelligence (BI) y visualización de datos".

Genera imágenes .png en la carpeta reports/, listas para incluir en una
presentación o dashboard.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/HR-Employee-Attrition-clean.csv"
REPORTS_DIR = "reports"

sns.set_theme(style="whitegrid")


def load_clean_data(path: str = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def grafico_rotacion_por_departamento(df: pd.DataFrame) -> None:
    """Gráfico de barras: tasa de rotación por departamento."""
    tasa = (
        df.groupby("Department")["AttritionFlag"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=tasa.values, y=tasa.index, hue=tasa.index, palette="Reds_r", legend=False)
    ax.set_xlabel("Tasa de rotación (%)")
    ax.set_ylabel("Departamento")
    ax.set_title("Tasa de rotación por departamento")
    for i, v in enumerate(tasa.values):
        ax.text(v + 0.3, i, f"{v}%", va="center")
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/01_rotacion_por_departamento.png", dpi=150)
    plt.close()


def grafico_rotacion_por_overtime(df: pd.DataFrame) -> None:
    """Gráfico de barras: rotación según horas extra."""
    tasa = (
        df.groupby("OverTime")["AttritionFlag"]
        .mean()
        .mul(100)
        .round(2)
    )

    plt.figure(figsize=(6, 5))
    ax = sns.barplot(x=tasa.index, y=tasa.values, hue=tasa.index, palette="Oranges", legend=False)
    ax.set_xlabel("¿Hace horas extra?")
    ax.set_ylabel("Tasa de rotación (%)")
    ax.set_title("Rotación según horas extra (OverTime)")
    for i, v in enumerate(tasa.values):
        ax.text(i, v + 0.5, f"{v}%", ha="center")
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/02_rotacion_por_overtime.png", dpi=150)
    plt.close()


def grafico_satisfaccion_vs_rotacion(df: pd.DataFrame) -> None:
    """Gráfico de línea: rotación según nivel de satisfacción laboral."""
    tasa = (
        df.groupby("JobSatisfaction")["AttritionFlag"]
        .mean()
        .mul(100)
        .round(2)
    )

    plt.figure(figsize=(7, 5))
    ax = sns.lineplot(x=tasa.index, y=tasa.values, marker="o", linewidth=2.5)
    ax.set_xlabel("Nivel de satisfacción laboral (1=Baja, 4=Muy alta)")
    ax.set_ylabel("Tasa de rotación (%)")
    ax.set_title("Rotación según satisfacción laboral")
    ax.set_xticks(tasa.index)
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/03_satisfaccion_vs_rotacion.png", dpi=150)
    plt.close()


def grafico_correlaciones(df: pd.DataFrame, top_n: int = 8) -> None:
    """Gráfico de barras horizontales: variables más correlacionadas con la rotación."""
    numericas = df.select_dtypes(include="number")
    corr = numericas.corr()["AttritionFlag"].drop("AttritionFlag")
    corr_top = corr.reindex(corr.abs().sort_values(ascending=False).index).head(top_n).round(3)

    colores = ["#d62728" if v < 0 else "#2ca02c" for v in corr_top.values]

    plt.figure(figsize=(8, 5))
    plt.barh(corr_top.index[::-1], corr_top.values[::-1], color=colores[::-1])
    plt.xlabel("Coeficiente de correlación con AttritionFlag")
    plt.title(f"Top {top_n} variables correlacionadas con la rotación")
    plt.axvline(0, color="black", linewidth=0.8)
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/04_correlaciones_rotacion.png", dpi=150)
    plt.close()


def grafico_distribucion_edad_por_attrition(df: pd.DataFrame) -> None:
    """Histograma comparativo: distribución de edad según si rotó o no."""
    plt.figure(figsize=(8, 5))
    ax = sns.histplot(
        data=df, x="Age", hue="Attrition", multiple="stack",
        palette={"Yes": "#d62728", "No": "#1f77b4"}, bins=20
    )
    ax.set_xlabel("Edad")
    ax.set_ylabel("Cantidad de empleados")
    ax.set_title("Distribución de edad según rotación")
    plt.tight_layout()
    plt.savefig(f"{REPORTS_DIR}/05_distribucion_edad_attrition.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    df = load_clean_data()

    grafico_rotacion_por_departamento(df)
    grafico_rotacion_por_overtime(df)
    grafico_satisfaccion_vs_rotacion(df)
    grafico_correlaciones(df)
    grafico_distribucion_edad_por_attrition(df)

    print("Gráficos generados en la carpeta 'reports/':")
    print("  01_rotacion_por_departamento.png")
    print("  02_rotacion_por_overtime.png")
    print("  03_satisfaccion_vs_rotacion.png")
    print("  04_correlaciones_rotacion.png")
    print("  05_distribucion_edad_attrition.png")