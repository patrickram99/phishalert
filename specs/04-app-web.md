# 04 — Aplicación web (Evidencia 3)

## Objetivo

Interfaz web donde se pega un mensaje y se ve la clasificación, las expresiones sospechosas resaltadas y las entidades extraídas.

## Requisitos

- **R1** Gradio (`gr.Blocks`). `build_demo(model_dir)` construye la interfaz; `python app.py --model models/phishalert [--share]` la lanza.
- **R2** Entrada: cuadro de texto multilínea y botón **Analizar**.
- **R3** Salidas:
  - veredicto con probabilidades de `phishing` y `legitimo` (`gr.Label`);
  - texto con resaltado por categoría y entidad (`gr.HighlightedText`) con leyenda;
  - tabla de entidades (tipo, texto);
  - resumen en una línea de las señales encontradas.
- **R4** Al menos 4 ejemplos precargados: phishing ES, phishing EN, legítimo ES, legítimo EN.
- **R5** Si `model_dir` no existe, la app arranca en modo heurístico y lo indica de forma visible.
- **R6** Texto vacío: mensaje pidiendo ingresar texto, sin error.
- **R7** Desde Colab se lanza con `share=True` y devuelve un enlace público temporal.
- **R8** Textos de la interfaz en español.

## Criterios de aceptación

- [ ] Con los 4 ejemplos, la app responde sin errores en menos de 3 s por mensaje (GPU o CPU).
- [ ] El ejemplo de phishing en español muestra al menos un resaltado y un enlace en la tabla.
- [ ] La app arranca localmente sin modelo (R5).

## Fuera de alcance (pasa a Ev4)

- Despliegue permanente, historial de análisis, carga de archivos `.eml`.

## Tareas

Ver `tasks.md` § 04.
