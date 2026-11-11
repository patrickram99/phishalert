# 06 — Pruebas automatizadas (Evidencia 4) — PENDIENTE

## Objetivo

Una suite que se ejecute con un comando, sin GPU ni descarga de modelos, y que corra en cada push.

## Estado de partida (Ev3)

Ya existen `tests/test_entities.py`, `tests/test_highlight.py` y `tests/test_pipeline.py` con casos básicos. Esta spec los amplía.

## Requisitos

- **R1** `pytest` corre toda la suite en menos de 30 s en CPU, sin red.
- **R2** Entidades (spec 03 R1–R7): por cada tipo, casos positivos y negativos en ES y EN; URL con puntuación final, correo que no se duplica como URL, teléfono con prefijo `+51`, marca en minúsculas, texto sin entidades, texto vacío.
- **R3** Resaltado (spec 03 R8–R11): al menos 3 frases por categoría e idioma; variantes sin tilde; ausencia de falsos positivos en 5 mensajes legítimos fijos.
- **R4** Datos (spec 01 R5–R6): `clean_text`, deduplicado y partición probados con un DataFrame sintético; partición determinista y estratificada.
- **R5** Pipeline (spec 03 R12–R13): con un clasificador simulado (`FakeClassifier`), verificar contrato de salida y que `segments` reconstruye el texto; prueba basada en propiedades con textos aleatorios (`hypothesis`).
- **R6** App (spec 04): `build_demo(None)` construye sin lanzar servidor; la función de análisis devuelve 4 salidas con texto vacío, ejemplo de phishing y ejemplo legítimo.
- **R7** Clasificador (spec 02 R6): prueba marcada `@pytest.mark.slow` que carga un modelo diminuto (`hf-internal-testing/tiny-random-DistilBertForSequenceClassification`) y verifica el formato de `predict`; excluida por defecto.
- **R8** Heurísticas de URL de la spec 07, cuando existan.
- **R9** CI: `.github/workflows/tests.yml` ejecuta `pytest` en Python 3.11 en cada push y pull request.
- **R10** Cobertura de `entities.py`, `highlight.py` y `pipeline.py` ≥ 85 % (`pytest --cov`).

## Criterios de aceptación

- [ ] `pytest` en verde local y en GitHub Actions.
- [ ] Insignia de CI en el README.
- [ ] Reporte de cobertura cumple R10.

## Cómo ejecutar esta spec

```bash
pip install -r requirements-dev.txt
pytest --cov=phishalert --cov-report=term-missing
pytest -m slow            # opcional, requiere red
```

Archivos a crear o ampliar: `tests/test_data.py`, `tests/test_app.py`, `tests/test_classifier.py`, `tests/conftest.py`, `.github/workflows/tests.yml`.
Dependencias nuevas (dev): `pytest-cov`, `hypothesis`.

## Tareas

Ver `tasks.md` § 06.
