"""Interfaz web de PhishAlert (spec 04).

Uso:  python app.py --model models/phishalert [--share]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import gradio as gr  # noqa: E402

from phishalert.pipeline import analyze  # noqa: E402

ETIQUETAS = {
    "datos_personales": "Solicitud de datos",
    "premio": "Premio",
    "amenaza": "Amenaza",
    "urgencia": "Urgencia",
    "URL": "Enlace",
    "EMAIL": "Correo",
    "TELEFONO": "Teléfono",
    "ORG": "Organización",
}
COLORES = {
    "Solicitud de datos": "#f97316",
    "Premio": "#eab308",
    "Amenaza": "#ef4444",
    "Urgencia": "#ec4899",
    "Enlace": "#3b82f6",
    "Correo": "#06b6d4",
    "Teléfono": "#8b5cf6",
    "Organización": "#22c55e",
}
EJEMPLOS = [
    ["Estimado cliente: su cuenta BCP ha sido bloqueada por actividad sospechosa. Verifique sus datos "
     "y su clave de internet en las próximas 24 horas ingresando a http://bcp-seguridad-clientes.xyz/validar "
     "o de lo contrario será suspendida definitivamente."],
    ["Congratulations! You have been selected as the winner of a $1,000 Amazon gift card. Click here "
     "to claim your prize now: http://bit.ly/claim-reward-now. Offer expires today."],
    ["Hola equipo, les comparto el acta de la reunión del lunes. Quedamos en revisar el avance del "
     "proyecto el jueves a las 3 pm en la sala 2. Cualquier comentario me avisan. Saludos, Carla."],
    ["Hi Mark, thanks for sending the draft. I added a few comments on section 3 and attached the "
     "updated figures. Let's go over them at tomorrow's meeting. Best, Julia"],
]


def build_demo(model_dir: str | None = None) -> gr.Blocks:
    classifier = None
    if model_dir and Path(model_dir).exists():
        try:
            from phishalert.classifier import PhishClassifier

            classifier = PhishClassifier(model_dir)
        except Exception as exc:  # noqa: BLE001
            print(f"[aviso] no se pudo cargar el modelo '{model_dir}': {exc}")

    def run(text: str):
        if not text or not text.strip():
            return None, [], [], "Ingresa el texto de un correo o mensaje para analizarlo."
        result = analyze(text, classifier)
        prob = result["prob_phishing"]
        segments = [(frag, ETIQUETAS.get(lab) if lab else None) for frag, lab in result["segments"]]
        table = [[ETIQUETAS[e["type"]], e["text"]] for e in result["entities"]]
        categorias = sorted({ETIQUETAS[h["category"]] for h in result["highlights"]})
        resumen = (
            f"**Veredicto: {'⚠️ Posible phishing' if result['label'] == 'phishing' else '✅ Parece legítimo'}** "
            f"({prob:.0%} de probabilidad de phishing). "
            f"Señales: {', '.join(categorias) if categorias else 'ninguna'}. "
            f"Entidades encontradas: {len(result['entities'])}."
        )
        if result["mode"] == "heuristico":
            resumen += "\n\n_Modo heurístico: no hay modelo cargado; el puntaje sale solo de las reglas._"
        return {"phishing": prob, "legitimo": 1 - prob}, segments, table, resumen

    with gr.Blocks(title="PhishAlert") as demo:
        gr.Markdown(
            "# 🛡️ PhishAlert\n"
            "Detección de mensajes de phishing con procesamiento de lenguaje natural. "
            "Pega el texto de un correo o mensaje (español o inglés)."
        )
        if classifier is None:
            gr.Markdown("> **Sin modelo cargado:** la app funciona en modo heurístico (solo reglas).")
        with gr.Row():
            with gr.Column(scale=1):
                entrada = gr.Textbox(label="Mensaje", lines=10, placeholder="Pega aquí el correo o mensaje…")
                boton = gr.Button("Analizar", variant="primary")
                gr.Examples(examples=EJEMPLOS, inputs=entrada, label="Ejemplos")
            with gr.Column(scale=1):
                veredicto = gr.Label(label="Clasificación", num_top_classes=2)
                resumen = gr.Markdown()
                resaltado = gr.HighlightedText(
                    label="Expresiones sospechosas y entidades", color_map=COLORES, show_legend=True
                )
                entidades = gr.Dataframe(headers=["Tipo", "Texto"], label="Entidades extraídas", wrap=True)
        boton.click(run, inputs=entrada, outputs=[veredicto, resaltado, entidades, resumen])
        entrada.submit(run, inputs=entrada, outputs=[veredicto, resaltado, entidades, resumen])
    return demo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="models/phishalert")
    parser.add_argument("--share", action="store_true", help="crear enlace público temporal")
    cli = parser.parse_args()
    build_demo(cli.model).launch(share=cli.share)
