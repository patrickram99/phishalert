"""Pruebas básicas del pipeline (spec 03, R12-R13)."""

import pytest

from phishalert.pipeline import analyze


class FakeClassifier:
    def __init__(self, prob):
        self.prob = prob

    def predict(self, text):
        return {"label": "phishing" if self.prob >= 0.5 else "legitimo", "prob_phishing": self.prob}


TEXTS = [
    "",
    "Hola, nos vemos mañana.",
    "Su cuenta BCP ha sido bloqueada. Verifique sus datos en http://bcp-seguro.xyz/validar de inmediato.",
    "You have won! Click here: bit.ly/x or write to win@prize.top, call +1 (555) 123-4567.",
]


@pytest.mark.parametrize("text", TEXTS)
def test_segments_reconstruyen_el_texto(text):
    result = analyze(text, use_spacy=False)
    assert "".join(frag for frag, _ in result["segments"]) == text


def test_contrato_con_modelo():
    result = analyze(TEXTS[2], FakeClassifier(0.93), use_spacy=False)
    assert result["mode"] == "modelo"
    assert result["label"] == "phishing"
    assert result["prob_phishing"] == pytest.approx(0.93)
    assert {"entities", "highlights", "segments"} <= result.keys()
    assert any(e["type"] == "URL" for e in result["entities"])


def test_modo_heuristico_sin_modelo():
    assert analyze(TEXTS[2], use_spacy=False)["mode"] == "heuristico"
    assert analyze(TEXTS[1], use_spacy=False)["label"] == "legitimo"
