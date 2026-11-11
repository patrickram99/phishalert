# 05 — Evaluación del desempeño (Evidencia 4) — PENDIENTE

## Objetivo

Medir con rigor qué tan bien funciona PhishAlert y dejar los números listos para el informe.

## Requisitos

- **R1** `python scripts/evaluate.py --data data/phishalert.csv --model models/phishalert --out reports/` evalúa sobre el split `test` (nunca usado en entrenamiento).
- **R2** Métricas de clasificación: accuracy, precision, recall, F1 (clase phishing y macro), ROC-AUC y matriz de confusión.
- **R3** Desglose de R2 por `lang` (`en`, `es`) y por `source`.
- **R4** Baseline: TF-IDF (uni+bigramas) + Regresión Logística entrenado con el mismo `train`; mismas métricas, en la misma tabla.
- **R5** Evaluación de entidades: `seeds/entidades_gold.jsonl` con ~50 mensajes anotados a mano (`text`, `entities: [{type, text}]`); reportar precision, recall y F1 por tipo con coincidencia exacta de texto.
- **R6** Evaluación del conjunto semilla en español natural (`seeds/seed_es.csv`) por separado, para contrastar con el español traducido.
- **R7** Latencia: mediana y p95 de `analyze()` por mensaje, en CPU y en GPU, sobre 200 mensajes de `test`.
- **R8** Análisis de errores: exportar los 20 falsos positivos y 20 falsos negativos de mayor confianza a `reports/errores.csv`.
- **R9** Salidas: `reports/metrics.json`, `reports/confusion_matrix.png`, `reports/roc.png`, `reports/tabla_comparativa.md`.

## Criterios de aceptación

- [ ] `reports/metrics.json` contiene las claves `transformer`, `baseline`, `por_idioma`, `por_fuente`, `entidades`, `latencia`.
- [ ] F1 de phishing en `test` ≥ 0.95 global y ≥ 0.90 en español; si no se alcanza, se documenta la causa en el informe.
- [ ] El script corre de principio a fin en Colab con un solo comando.

## Cómo ejecutar esta spec

```bash
python scripts/get_data.py                      # si data/ no existe
python scripts/train.py --epochs 3 --max-train 0 --out models/phishalert
python scripts/evaluate.py --data data/phishalert.csv --model models/phishalert --out reports/
```

Archivos a crear: `scripts/evaluate.py`, `src/phishalert/evaluate.py`, `src/phishalert/baseline.py`, `seeds/entidades_gold.jsonl`.
Dependencias nuevas: `matplotlib`.

## Fuera de alcance

- Pruebas de robustez adversarial (ofuscación de caracteres, homoglifos): solo se mencionan como limitación.

## Tareas

Ver `tasks.md` § 05.
