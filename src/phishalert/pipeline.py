"""Integra clasificación, entidades y resaltado (spec 03, R12-R13)."""

from __future__ import annotations

from .entities import extract_entities, resolve_overlaps
from .highlight import find_suspicious, heuristic_score


def build_segments(text: str, highlights: list[dict], entities: list[dict]) -> list[tuple]:
    """Lista de (fragmento, etiqueta | None) que reconstruye el texto completo."""
    spans = [{"start": h["start"], "end": h["end"], "label": h["category"]} for h in highlights]
    spans += [{"start": e["start"], "end": e["end"], "label": e["type"]} for e in entities]
    segments: list[tuple] = []
    pos = 0
    for s in resolve_overlaps(spans):
        if s["start"] > pos:
            segments.append((text[pos:s["start"]], None))
        segments.append((text[s["start"]:s["end"]], s["label"]))
        pos = s["end"]
    if pos < len(text):
        segments.append((text[pos:], None))
    return segments


def analyze(text: str, classifier=None, use_spacy: bool = True) -> dict:
    """Analiza un mensaje. Sin clasificador usa el puntaje heurístico (modo de respaldo)."""
    text = text or ""
    entities = extract_entities(text, use_spacy=use_spacy)
    highlights = find_suspicious(text)

    if classifier is not None and text.strip():
        prob = float(classifier.predict(text)["prob_phishing"])
        mode = "modelo"
    else:
        prob = heuristic_score(highlights, has_url=any(e["type"] == "URL" for e in entities))
        mode = "heuristico"

    return {
        "label": "phishing" if prob >= 0.5 else "legitimo",
        "prob_phishing": prob,
        "mode": mode,
        "entities": entities,
        "highlights": highlights,
        "segments": build_segments(text, highlights, entities),
    }
