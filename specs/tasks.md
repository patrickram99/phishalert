# Tareas

Estado: `[x]` hecho · `[ ]` pendiente. Cada tarea cita su requisito.

## Evidencia 3 — 12/11

### 01 Datos
- [x] T1.1 `data.py`: carga de `phishing-email-dataset` y `sms_spam` (R3, R7)
- [x] T1.2 `data.py`: limpieza y deduplicado (R5)
- [x] T1.3 `data.py`: traducción EN→ES con MarianMT (R4)
- [x] T1.4 `seeds/seed_es.csv`: conjunto semilla en español (R4)
- [x] T1.5 `data.py`: partición estratificada (R6)
- [x] T1.6 `scripts/get_data.py`: CLI y resumen (R1, R8, R9)
- [x] T1.7 Ejecutar en Colab y verificar criterios de aceptación

### 02 Clasificador
- [x] T2.1 `train.py`: afinado con `Trainer` y métricas (R1–R5, R7)
- [x] T2.2 `classifier.py`: `PhishClassifier` (R6)
- [x] T2.3 `scripts/train.py`: CLI (R2, R3)
- [x] T2.4 Entrenamiento corto en Colab y verificación de criterios

### 03 Entidades y resaltado
- [x] T3.1 `entities.py`: URL, EMAIL, TELEFONO (R1–R5, R7)
- [x] T3.2 `entities.py`: ORG con lista de marcas y spaCy opcional (R6)
- [x] T3.3 `highlight.py`: léxico bilingüe y `heuristic_score` (R8–R11)
- [x] T3.4 `pipeline.py`: `analyze` y `segments` (R12, R13)
- [x] T3.5 Pruebas básicas en `tests/`

### 04 App web
- [x] T4.1 `app.py`: interfaz Gradio con ejemplos (R1–R4, R8)
- [x] T4.2 Modo heurístico y texto vacío (R5, R6)
- [x] T4.3 Lanzar desde Colab con enlace público (R7)

### Repositorio
- [x] T0.1 Estructura, `README.md`, `requirements.txt`, `.gitignore`
- [x] T0.2 Publicar en GitHub
- [x] T0.3 Copia de la notebook en `notebooks/PhishAlert.ipynb`

## Evidencia 4 — 01/12

### 05 Evaluación
- [ ] T5.1 `baseline.py`: TF-IDF + Regresión Logística (R4)
- [ ] T5.2 `evaluate.py`: métricas en `test`, por idioma y fuente (R1–R3)
- [ ] T5.3 `seeds/entidades_gold.jsonl` y evaluación de entidades (R5)
- [ ] T5.4 Evaluación del conjunto semilla ES (R6)
- [ ] T5.5 Latencia (R7)
- [ ] T5.6 Análisis de errores (R8)
- [ ] T5.7 Figuras y tabla comparativa (R9)

### 06 Pruebas
- [ ] T6.1 Ampliar pruebas de entidades y resaltado (R2, R3)
- [ ] T6.2 `tests/test_data.py` (R4)
- [ ] T6.3 Prueba por propiedades del pipeline (R5)
- [ ] T6.4 `tests/test_app.py` (R6)
- [ ] T6.5 `tests/test_classifier.py` con modelo diminuto (R7)
- [ ] T6.6 Pruebas de `url_risk` (R8)
- [ ] T6.7 GitHub Actions e insignia (R9)
- [ ] T6.8 Cobertura ≥ 85 % (R10)

### 07 Demo 100 %
- [ ] T7.1 Entrenamiento completo con selección de mejor checkpoint (R1)
- [ ] T7.2 Publicar en Hugging Face Hub con tarjeta de modelo (R2)
- [ ] T7.3 Notebook de demo que carga del Hub (R3)
- [ ] T7.4 `url_risk.py` y tabla de dominios oficiales (R4–R6)
- [ ] T7.5 `explain.py`: importancia por oclusión (R7, R8)
- [ ] T7.6 Ventanas para textos largos (R9)
- [ ] T7.7 Umbral configurable y tres niveles (R10)
- [ ] T7.8 Detección de idioma (R11)

### 08 Informe
- [ ] T8.1 Redactar `docs/informe.md` (R3–R6)
- [ ] T8.2 Insertar cifras y figuras de `reports/` (R2)
- [ ] T8.3 Exportar a PDF ≤ 4 páginas (R1)
