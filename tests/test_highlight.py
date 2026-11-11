"""Pruebas básicas del resaltado (spec 03, R8-R11)."""

import pytest

from phishalert.highlight import find_suspicious, heuristic_score


def cats(text):
    return {h["category"] for h in find_suspicious(text)}


@pytest.mark.parametrize("text,category", [
    ("Verifique sus datos ahora", "datos_personales"),
    ("Ingrese su contrasena", "datos_personales"),
    ("Please verify your account", "datos_personales"),
    ("Has sido seleccionado ganador", "premio"),
    ("You have won a free gift", "premio"),
    ("Su cuenta ha sido bloqueada", "amenaza"),
    ("Your account will be suspended", "amenaza"),
    ("Responda de inmediato", "urgencia"),
    ("Act now, offer expires today", "urgencia"),
])
def test_categorias(text, category):
    assert category in cats(text)


def test_tolera_tildes_y_mayusculas():
    assert "datos_personales" in cats("INGRESE SU CONTRASEÑA")
    assert "datos_personales" in cats("codigo de verificacion")
    assert "datos_personales" in cats("código de verificación")


@pytest.mark.parametrize("text", [
    "Hola Ana, la reunión del proyecto será el jueves a las 10 am en la sala 3.",
    "Hi Mark, thanks for sending the draft. Let's go over it at tomorrow's meeting.",
    "Mamá, ya llegué a la universidad. Salgo a las 6.",
])
def test_legitimo_sin_resaltados(text):
    assert find_suspicious(text) == []


def test_spans_validos_y_sin_solapes():
    text = "URGENTE: su cuenta ha sido bloqueada. Verifique sus datos y reclame su premio."
    spans = find_suspicious(text)
    assert all(text[s["start"]:s["end"]] == s["text"] for s in spans)
    assert all(a["end"] <= b["start"] for a, b in zip(spans, spans[1:]))


def test_heuristic_score():
    assert heuristic_score([], has_url=False) == 0.0
    alto = heuristic_score(find_suspicious("Su cuenta ha sido bloqueada, verifique sus datos urgente"), True)
    assert 0.5 < alto <= 1.0
