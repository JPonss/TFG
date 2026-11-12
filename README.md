# TFG
Programación Genética para el descubrimiento de estrategias de inversión rentables en opciones sobre índices financieros
Calendario 2026-27:

Envío de propuestas hasta el: 18 de septiembre.
Inicio de solicitud de propuestas: 14 de septiembre.
Fin de solicitud de propuestas: 23 de septiembre.
Publicación de asignaciones de TFG: 28 de septiembre.
Entrega del plan de trabajo: 9 de octubre.
Entrega de la memoria de seguimiento: 13 de noviembre
Entrega de la memoria final: 11 de enero
Defensas de TFG: 26, 27 y 29 de enero


Título del trabajo: 10295 — Programación Genética para el descubrimiento de estrategias de inversión rentables en opciones sobre índices financieros

Resumen general del trabajo:
El proyecto se apoya en los principios de la Programación Genética (https://www.genetic-programming.org/) para representar estrategias de trading mediante estructuras de árboles sintácticos. Se requiere construir un entorno de simulación (backtesting) donde se introduzca la información histórica de un índice financiero determinado para que el algoritmo evolutivo descubra de forma autónoma la combinación óptima de reglas. Se pide al alumno que aplique una metodología formal de Ingeniería del Software para diseñar, construir y validar un entorno integral. El lenguaje de programación, las herramientas y las librerías a utilizar quedan a libre elección del estudiante. La solución deberá:

Ingestar y estructurar datos históricos de un índice financiero y su mercado de opciones asociado.

Generar e iterar estrategias de inversión mediante un motor evolutivo de Programación Genética.

Implementar una función de evaluación (fitness) centrada en maximizar la rentabilidad y gestionar el riesgo a lo largo de una ventana temporal especificada.

Simular y validar la efectividad de las estrategias resultantes frente a datos fuera de muestra (out-of-sample)

Lista de objetivos concretos:

Diseñar la arquitectura modular del sistema utilizando metodologías y patrones de diseño propios de la Ingeniería del Software.

Implementar un módulo de datos capaz de procesar e integrar las series temporales del índice elegido y sus correspondientes opciones para la ventana temporal de estudio.

Desarrollar el motor de Programación Genética (definición de nodos terminales, funciones, operadores de cruce, mutación y selección natural) adaptado al problema de trading.
Desarrollar el motor de simulación (backtesting) y la función de fitness orientada a identificar estrategias maximizadoras de rentabilidad y control del riesgo en el periodo evaluado.

Empaquetar la solución dotándol
a de una interfaz (CLI o gráfica) y un sistema de configuración que permita parametrizar las ejecuciones y ventanas temporales de forma sencilla.

Evaluar la rentabilidad y robustez de las estrategias encontradas comparándolas con estrategias base de referencia (baselines) en la ventana de tiempo seleccionada.

Desglose de la dedicación total del trabajo en horas (297 horas en los Grados):
Fase 1: Inicio y Requisitos — 30 horas
Fase 2: Desarrollo Técnico (Núcleo de Ingeniería) — 180 horas
Fase 3: Despliegue, Pruebas y Validación — 47 horas
Fase 4: Documentación y Memoria — 40 horas
TOTAL : 297 horas

Conocimientos previos recomendados para hacer el trabajo:
Programación orientada a objetos en el lenguaje seleccionado por el alumno
Principios e ingeniería del software (patrones de diseño, UML, arquitecturas modulares)
Algoritmos evolutivos y programación genética
Fundamentos de derivados financieros (opciones call/put y métricas de rendimiento)
Control de versiones con Git
Manejo de estructuras de datos y cálculo paralelo/multiprocesamiento

Tutor 1: FRANCISCO JAVIER SEGOVIA PÉREZ - fsegovia@fi.upm.es

1ªtarea: plan de trabajo

Al finalizar la tercera semana de docencia el alumno ha de entregar su Plan de Trabajo.

Esta primera tarea del alumno será documentar la descripción del trabajo a realizar con las indicaciones que le haya dado el tutor durante las primeras sesiones de trabajo. En ellas se fijarán, más concretamente, los objetivos que debe cumplir cada alumno y la planificación previa de su trabajo. El documento no debe ocupar más de cuatro páginas y deberá estructurarse en cuatro apartados:

Descripción general del trabajo, con una lista de objetivos
Lista de tareas
Diagrama de Gantt
Copia de la propuesta de trabajo escrito por el tutor.







Borrador estructura del proyecto: 

TFG/
├── data/
│   ├── raw/                 # spy_options.csv y descargas en bruto
│   └── processed/           # dataset maestro consolidado (CSV o Parquet)
├── config/
│   └── data_config.yaml     # Fechas, rutas, tickers y parámetros configurables
├── src/
│   ├── __init__.py
│   ├── data/                # <-- MÓDULO DE INGESTA Y PROCESAMIENTO
│   │   ├── __init__.py
│   │   ├── base.py          # Interfaces abstractas (Contratos)
│   │   ├── yfinance_source.py # Adaptador para SPX y VIX
│   │   ├── dolt_source.py   # Adaptador y procesador para spy_options.csv
│   │   └── pipeline.py      # Orquestador/Builder del dataset unificado
│   ├── genetic/             # Motor de Programación Genética (Fase posterior)
│   ├── backtest/            # Simulador y función de Fitness (Fase posterior)
│   └── utils/               # Logging y métricas auxiliares
├── tests/
│   └── test_data_ingestion.py # Tests unitarios con pytest
├── main.py                  # Punto de entrada / CLI
├── requirements.txt
└── README.md
