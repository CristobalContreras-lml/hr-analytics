"""
Módulo 4: Modelo predictivo de rotación (Attrition).

Objetivo: construir un modelo de clasificación simple que prediga si un
empleado tiene alta probabilidad de dejar la empresa, respondiendo al
requisito de Sodexo: "construir escenarios predictivos de los principales
KPI de RRHH" e "Inteligencia Artificial (IA) aplicada al análisis y
optimización de procesos".

Usa Regresión Logística (modelo simple e interpretable, ideal para RRHH,
donde explicar el "por qué" de una predicción es tan importante como la
predicción misma).
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

DATA_PATH = "data/HR-Employee-Attrition-clean.csv"
RANDOM_STATE = 42


def load_clean_data(path: str = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def preparar_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepara variables predictoras (X) y variable objetivo (y).

    - Elimina columnas de texto redundantes con AttritionFlag.
    - Convierte variables categóricas a variables numéricas (One-Hot Encoding).
    """
    df = df.copy()

    y = df["AttritionFlag"]

    # Quitamos las columnas de texto que ya están representadas numéricamente
    # o que no aportan como predictoras (Attrition es la misma info que y).
    X = df.drop(columns=["Attrition", "AttritionFlag"])

    # One-Hot Encoding: convierte columnas de texto (ej. Department: "Sales",
    # "R&D", "HR") en varias columnas binarias (0/1), una por categoría.
    # Los modelos matemáticos no entienden texto, solo números.
    X = pd.get_dummies(X, drop_first=True)

    return X, y


def entrenar_modelo(X_train, y_train) -> tuple[LogisticRegression, StandardScaler]:
    """Escala las variables numéricas y entrena la Regresión Logística."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    modelo = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight="balanced")
    modelo.fit(X_train_scaled, y_train)

    return modelo, scaler


def evaluar_modelo(modelo, scaler, X_test, y_test) -> None:
    """Imprime métricas de desempeño del modelo sobre el set de prueba."""
    X_test_scaled = scaler.transform(X_test)
    y_pred = modelo.predict(X_test_scaled)

    print("=" * 60)
    print("MÉTRICAS DE DESEMPEÑO (sobre datos de prueba, nunca vistos)")
    print("=" * 60)
    print(f"Accuracy  (exactitud general):     {accuracy_score(y_test, y_pred):.3f}")
    print(f"Precision (de los que predije rotan, cuántos rotan realmente): {precision_score(y_test, y_pred):.3f}")
    print(f"Recall    (de los que rotan realmente, cuántos detecté):       {recall_score(y_test, y_pred):.3f}")
    print(f"F1-score  (balance entre precision y recall):                 {f1_score(y_test, y_pred):.3f}")

    print("\n" + "=" * 60)
    print("MATRIZ DE CONFUSIÓN")
    print("=" * 60)
    cm = confusion_matrix(y_test, y_pred)
    print(f"                  Predijo: No se va   Predijo: Se va")
    print(f"Realidad: No se va       {cm[0][0]:>10}         {cm[0][1]:>10}")
    print(f"Realidad: Se va          {cm[1][0]:>10}         {cm[1][1]:>10}")

    print("\n" + "=" * 60)
    print("REPORTE DE CLASIFICACIÓN COMPLETO")
    print("=" * 60)
    print(classification_report(y_test, y_pred, target_names=["No rota", "Rota"]))


def variables_mas_influyentes(modelo, X: pd.DataFrame, top_n: int = 10) -> None:
    """Muestra las variables con mayor peso (coeficiente) en la predicción."""
    coeficientes = pd.Series(modelo.coef_[0], index=X.columns)
    top = coeficientes.reindex(coeficientes.abs().sort_values(ascending=False).index).head(top_n)

    print("=" * 60)
    print(f"TOP {top_n} VARIABLES QUE MÁS INFLUYEN EN LA PREDICCIÓN")
    print("=" * 60)
    print("(Positivo = aumenta probabilidad de rotar | Negativo = la reduce)\n")
    print(top.round(3))


if __name__ == "__main__":
    df = load_clean_data()
    X, y = preparar_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    modelo, scaler = entrenar_modelo(X_train, y_train)

    evaluar_modelo(modelo, scaler, X_test, y_test)
    print()
    variables_mas_influyentes(modelo, X)