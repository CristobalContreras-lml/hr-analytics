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


  ## Conclusiones y Recomendaciones

### Hallazgos clave

El análisis exploratorio y el modelo predictivo coinciden en señalar a **OverTime** como la variable con mayor impacto en la rotación: los empleados que hacen horas extra rotan a una tasa cercana al triple que quienes no lo hacen. Esto se confirma tanto en el análisis de KPIs (Módulo 3) como en el modelo predictivo, donde `OverTime_Yes` es el segundo coeficiente más alto (0.771).

Por área, **Sales** (~20%) y **Human Resources** (~19%) presentan las tasas de rotación más altas, mientras que **Research & Development** es la más estable (~14%). El modelo refuerza esto: `Department_Sales` y `JobRole_Sales Representative` aparecen entre las variables más predictivas.

Otras variables con peso relevante:
- **TotalWorkingYears** (coeficiente -0.660): a menor experiencia laboral total, mayor probabilidad de rotar — sugiere que el riesgo se concentra en etapas tempranas de carrera.
- **YearsSinceLastPromotion** (0.499): empleados sin ascensos recientes muestran más propensión a irse.
- **BusinessTravel_Travel_Frequently** (0.723): los viajes frecuentes se asocian a mayor rotación.
- **JobRole_Laboratory Technician** (0.810): el rol individual con mayor coeficiente positivo del modelo.

### Desempeño del modelo

El modelo de regresión logística alcanzó un **accuracy de 75.2%**, pero ese número por sí solo es engañoso dado el desbalance de clases (247 "No rota" vs. 47 "Rota" en el set de prueba). Lo relevante para el negocio es el **recall de la clase "Rota" (0.62)**: el modelo detecta 6 de cada 10 empleados que efectivamente van a renunciar, lo cual es útil como sistema de alerta temprana — aunque con una precisión moderada (0.35), es decir, de cada 10 personas que el modelo marca como "en riesgo", ~3-4 realmente rotan. En un contexto de retención, ese trade-off es razonable: es preferible revisar algunos falsos positivos de más que dejar pasar a alguien que sí se va a ir.

### Recomendaciones para RRHH

1. **Revisar la política de horas extra** en Sales y HR, priorizando estos departamentos dado que OverTime es el driver individual más fuerte y más accionable (a diferencia de variables como antigüedad, que no se puede "corregir" directamente).
2. **Fortalecer la conversación de desarrollo de carrera** en roles con baja frecuencia de ascensos (`YearsSinceLastPromotion` alto), especialmente en los primeros años de permanencia.
3. **Programa de retención focalizado** para roles de mayor riesgo identificados por el modelo (Laboratory Technician, Sales Representative), en vez de una política genérica para toda la organización.
4. **Usar el modelo como filtro de priorización**, no como decisión automática: dado el balance actual precision/recall, su mejor uso es generar una lista corta de personas para que un HRBP revise cualitativamente, no para actuar sobre la predicción de forma aislada.

### Próximos pasos

Con más tiempo, el modelo se beneficiaría de: balanceo de clases (SMOTE u oversampling), ajuste del umbral de decisión según el costo real de un falso negativo vs. falso positivo para el negocio, y variables adicionales como resultados de encuestas de clima o motivos declarados en entrevistas de salida.