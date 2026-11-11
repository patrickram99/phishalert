# 00 — Visión y reglas del proyecto

## Qué es PhishAlert

Aplicación web que recibe el texto de un correo o mensaje y:

1. lo **clasifica** como `phishing` o `legitimo` con su probabilidad;
2. **extrae entidades**: enlaces, correos electrónicos, teléfonos y organizaciones mencionadas;
3. **resalta expresiones sospechosas**: solicitudes de datos personales, promesas de premios, amenazas de bloqueo de cuenta y urgencia.

Idiomas soportados: español e inglés.

Integrantes: Marycielo Bedoya, María Pinazo, Patrick Ramírez.

## Técnicas de NLP

| Técnica | Implementación |
|---|---|
| Clasificación de textos | `distilbert-base-multilingual-cased` afinado (2 clases) |
| Extracción de entidades | Expresiones regulares (enlaces, correos, teléfonos) + NER de spaCy y lista de marcas (organizaciones) |
| Apoyo: detección de patrones | Léxico bilingüe por categorías para el resaltado |

## Cómo trabajamos (spec-driven)

- Cada funcionalidad tiene una spec en `specs/NN-nombre.md` con: objetivo, requisitos numerados (`R1`, `R2`…), criterios de aceptación verificables, fuera de alcance y tareas.
- No se escribe código sin requisito que lo respalde. Si el código necesita desviarse, primero se actualiza la spec.
- `specs/tasks.md` es la única fuente de verdad del avance.
- Los requisitos se citan en commits y pruebas (`R3 de spec 03`).

## Entregables y alcance

| Evidencia | Fecha | Entregables | Specs |
|---|---|---|---|
| 3 | 12/11 | Repositorio, script de obtención de datos, demo al 50% | 01, 02, 03, 04 |
| 4 | 01/12 (presentación 03/12) | Demo al 100%, métricas, informe ≤4 páginas, pruebas automatizadas | 05, 06, 07, 08 |

### Definición de "demo al 50%" (Evidencia 3)

Flujo completo de extremo a extremo: texto → clasificación + entidades + resaltado en la interfaz Gradio, con un modelo de **entrenamiento corto** (submuestra, 1 época).

### Lo que falta para el 100% (Evidencia 4)

Entrenamiento completo y modelo publicado, evaluación formal por idioma, análisis de riesgo de URLs, explicación basada en el modelo, suite de pruebas con CI e informe.

## Decisiones globales

- **D1** El código vive en `src/phishalert/` y es el mismo que usa la notebook de Colab (la notebook clona el repositorio; no duplica lógica).
- **D2** Los pesos del modelo y los datos generados no se versionan en git (`models/`, `data/`).
- **D3** Etiquetas: `0 = legitimo`, `1 = phishing`.
- **D4** Semilla fija `42` en particiones y entrenamiento.
- **D5** La app debe poder arrancar sin modelo (modo heurístico, señalado en pantalla) para poder probar entidades y resaltado en cualquier máquina.
