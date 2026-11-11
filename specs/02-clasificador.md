# 02 — Clasificador (Evidencia 3)

## Objetivo

Afinar un transformer multilingüe que distinga phishing de mensajes legítimos y exponerlo con una interfaz de inferencia simple.

## Requisitos

- **R1** Modelo base `distilbert-base-multilingual-cased`, cabeza de clasificación de 2 clases (`id2label = {0: legitimo, 1: phishing}`).
- **R2** `python scripts/train.py --data data/phishalert.csv --out models/phishalert` entrena con el split `train`, evalúa en `val` y guarda modelo, tokenizador y `metrics.json` en `--out`.
- **R3** Hiperparámetros por argumento: `--epochs` (1), `--max-train` (6000; 0 = todo), `--max-len` (256), `--batch-size` (16), `--lr` (5e-5). Semilla 42.
- **R4** Usa GPU con precisión mixta si está disponible; funciona en CPU (lento).
- **R5** Métricas de validación reportadas: accuracy, precision, recall y F1 de la clase phishing.
- **R6** `PhishClassifier(model_dir).predict(texto)` devuelve `{"label": "phishing"|"legitimo", "prob_phishing": float}`; `predict_batch(lista)` devuelve una lista equivalente.
- **R7** La submuestra de entrenamiento (`--max-train`) conserva todas las filas en español y completa con inglés, para no perder el idioma minoritario.

## Criterios de aceptación (Ev3 — entrenamiento corto)

- [ ] El entrenamiento termina en Colab con GPU T4 en menos de 10 minutos.
- [ ] F1 de validación ≥ 0.90 (referencia; la evaluación formal es la spec 05).
- [ ] `predict` clasifica correctamente al menos 3 de 4 mensajes de humo (phishing ES/EN, legítimo ES/EN).

## Fuera de alcance (pasa a Ev4)

- Entrenamiento completo, búsqueda de hiperparámetros, evaluación en `test`, comparación con baseline, publicación del modelo.

## Tareas

Ver `tasks.md` § 02.
