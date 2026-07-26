# HR Analytics Dashboard — People Analytics Project

Proyecto de aprendizaje orientado a **People Analytics**: exploración, limpieza,
cálculo de KPIs de RRHH, visualización y modelo predictivo de rotación (attrition),
usando el dataset público *IBM HR Analytics Employee Attrition & Performance*.

Este proyecto nace como preparación práctica para una entrevista técnica en el
área de People Analytics, con foco en las herramientas y conceptos solicitados:
Business Intelligence, visualización de datos, IA aplicada al análisis de RRHH
y automatización de reportes.

## Estructura del proyecto

- `data/` — datasets crudos y procesados
- `src/` — scripts de procesamiento, análisis y modelado
- `notebooks/` — exploración interactiva
- `reports/` — reportes y gráficos generados

## Roadmap (por módulos)

1. **Exploración y limpieza de datos** ✅
2. Cálculo de KPIs y correlaciones
3. Visualización de KPIs
4. Modelo predictivo de rotación (attrition)
5. Automatización de reportes

## Dataset

**IBM HR Analytics Employee Attrition & Performance** (1470 empleados, 35 variables).

- **Origen:** dataset ficticio creado por científicos de datos de IBM para la
  plataforma Watson Analytics, con el fin de demostrar el análisis de factores
  de rotación de personal. No corresponde a datos reales de empleados.
- **Registro con DOI (archivo permanente, citable):**
  https://zenodo.org/records/4088439
- **Distribución conocida también en:** Kaggle
  (pavansubhasht/ibm-hr-analytics-attrition-dataset) y como dataset `attrition`
  en el paquete R `modeldata` (tidymodels/Posit).
- **Verificación de integridad:** el archivo usado en este proyecto fue
  verificado mediante hash MD5 (`ad8207459e5732574372cf8ff619883f`), coincidente
  con el registrado en Zenodo, confirmando que es una copia íntegra y sin
  alteraciones del dataset original.