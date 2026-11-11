# 🛡️ PhishAlert

Detección de mensajes de phishing mediante procesamiento de lenguaje natural.

Aplicación web que analiza el texto de un correo o mensaje (español o inglés), lo clasifica como **phishing** o **legítimo** y muestra por qué: resalta solicitudes de datos personales, promesas de premios, amenazas de bloqueo y urgencia, y extrae los enlaces, correos, teléfonos y organizaciones mencionadas.

**Integrantes:** Marycielo Bedoya · María Pinazo · Patrick Ramírez

## Técnicas de NLP

| Técnica | Cómo |
|---|---|
| Clasificación de textos | `distilbert-base-multilingual-cased` afinado para 2 clases |
| Extracción de entidades | Expresiones regulares (enlaces, correos, teléfonos) + NER de spaCy y lista de marcas (organizaciones) |

## Estado

| Entrega | Fecha | Contenido | Estado |
|---|---|---|---|
| Evidencia 3 | 12/11 | Repositorio, script de datos, demo al 50 % | ✅ |
| Evidencia 4 | 01/12 | Demo al 100 %, métricas, informe, pruebas automatizadas | Especificado en `specs/05`–`08` |

El proyecto se desarrolla guiado por especificaciones: ver [`specs/`](specs/) y el avance en [`specs/tasks.md`](specs/tasks.md).

### Resultados de la Evidencia 3 (corrida en Colab, GPU T4, 11/11)

| | |
|---|---|
| Datos | 22 609 mensajes: 19 582 en inglés y 3 027 en español; 7 132 phishing y 15 477 legítimos |
| Entrenamiento | 6 000 mensajes, 1 época, 47 s |
| Validación (2 261 mensajes) | accuracy 0.943 · precision 0.973 · recall 0.844 · F1 0.904 |
| Pruebas | 30 de 30 |

Son métricas de referencia sobre validación con el modelo corto; la evaluación formal sobre `test` es la spec 05.

## Ejecutar en Google Colab (recomendado)

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/patrickram99/phishalert/blob/main/notebooks/PhishAlert.ipynb)

Abrir [`notebooks/PhishAlert.ipynb`](notebooks/PhishAlert.ipynb) en Colab con GPU (Entorno de ejecución → Cambiar tipo → T4) y ejecutar todas las celdas. La notebook clona este repositorio, descarga los datos, afina el modelo y lanza la app con un enlace público.

## Ejecutar por comandos

```bash
pip install -r requirements.txt
python -m spacy download xx_ent_wiki_sm

python scripts/get_data.py                 # genera data/phishalert.csv
python scripts/train.py                    # genera models/phishalert
python app.py --model models/phishalert    # abre la app
pytest                                     # pruebas
```

Sin modelo entrenado, `python app.py` arranca en modo heurístico (solo reglas), útil para probar entidades y resaltado.

## Datos

`scripts/get_data.py` descarga y unifica:

- [`zefang-liu/phishing-email-dataset`](https://huggingface.co/datasets/zefang-liu/phishing-email-dataset) — correos en inglés;
- [`ucirvine/sms_spam`](https://huggingface.co/datasets/ucirvine/sms_spam) — SMS en inglés;
- una muestra traducida al español con `Helsinki-NLP/opus-mt-en-es`;
- `seeds/seed_es.csv` — 40 mensajes en español escritos a mano.

## Estructura

```
specs/            especificaciones y tareas
src/phishalert/   data · train · classifier · entities · highlight · pipeline
scripts/          get_data.py · train.py
app.py            interfaz Gradio
seeds/            datos semilla versionados
tests/            pruebas (pytest)
notebooks/        notebook de Colab
```

## Limitaciones actuales

- El modelo de la Evidencia 3 es de entrenamiento corto (submuestra, 1 época).
- El español de entrenamiento proviene mayormente de traducción automática.
- No se analiza el destino real de los enlaces, cabeceras ni adjuntos.
