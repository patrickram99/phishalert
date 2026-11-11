# 08 — Informe (Evidencia 4) — PENDIENTE

## Objetivo

Informe de **máximo 4 páginas** con las decisiones tomadas y las limitaciones, que evidencie al menos dos técnicas de NLP.

## Requisitos

- **R1** Archivo `docs/informe.md` exportado a PDF (`docs/informe.pdf`), ≤ 4 páginas A4, fuente 11 pt.
- **R2** Todas las cifras provienen de `reports/metrics.json` (spec 05); ninguna se escribe a mano sin respaldo.
- **R3** Estructura y extensión orientativa:

| # | Sección | Contenido | Extensión |
|---|---|---|---|
| 1 | Problema y objetivo | Qué es el phishing, a quién sirve la app, qué entrega | ¼ pág. |
| 2 | Datos | Fuentes, tamaños por idioma y clase, limpieza, partición, por qué se tradujo | ½ pág. |
| 3 | Técnica 1: clasificación de textos | Por qué DistilBERT multilingüe, configuración de entrenamiento, comparación con baseline TF-IDF | ¾ pág. |
| 4 | Técnica 2: extracción de entidades | Regex vs. NER, lista de marcas, riesgo de enlaces | ½ pág. |
| 5 | Aplicación | Arquitectura (diagrama), flujo de `analyze()`, captura de pantalla | ½ pág. |
| 6 | Resultados | Tabla de métricas global / por idioma, matriz de confusión, latencia, entidades | ¾ pág. |
| 7 | Decisiones y limitaciones | Ver R4 y R5 | ½ pág. |
| 8 | Trabajo futuro y referencias | | ¼ pág. |

- **R4** Decisiones a justificar: transformer en lugar de modelo clásico; modelo multilingüe único en lugar de uno por idioma; traducción automática para obtener español; regex para enlaces/correos y NER solo para organizaciones; Gradio como entregable; léxico + oclusión para explicar.
- **R5** Limitaciones a declarar: español mayormente traducido; spam de SMS como aproximación de smishing; datasets antiguos frente a phishing actual (incluido el generado con IA); sin análisis de cabeceras, adjuntos ni destino real de los enlaces; léxico evadible con ofuscación; posibles falsos positivos en correos bancarios legítimos.
- **R6** Incluir enlace al repositorio y a la demo, e integrantes.

## Criterios de aceptación

- [ ] PDF de ≤ 4 páginas.
- [ ] Cada número del informe se puede rastrear a `reports/`.
- [ ] Las dos técnicas de NLP tienen sección propia.

## Cómo ejecutar esta spec

Requiere las specs 05 y 07 terminadas. Redactar `docs/informe.md` siguiendo R3 y exportar:

```bash
pandoc docs/informe.md -o docs/informe.pdf -V geometry:margin=2cm -V fontsize=11pt
```

## Tareas

Ver `tasks.md` § 08.
