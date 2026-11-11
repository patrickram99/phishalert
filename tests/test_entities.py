"""Pruebas básicas de entidades (spec 03, R1-R7). La suite completa es la spec 06."""

from phishalert.entities import extract_entities


def by_type(text, kind):
    return [e["text"] for e in extract_entities(text, use_spacy=False) if e["type"] == kind]


def test_url_con_esquema_sin_puntuacion_final():
    assert by_type("Ingrese a http://bcp-seguro.xyz/validar.", "URL") == ["http://bcp-seguro.xyz/validar"]


def test_url_sin_esquema_y_acortador():
    assert by_type("Reclama en bit.ly/premio-peru hoy", "URL") == ["bit.ly/premio-peru"]
    assert by_type("Visit www.example.com now", "URL") == ["www.example.com"]


def test_fin_de_oracion_no_es_url():
    assert by_type("Hola.Me llamo Ana y vivo en Lima.", "URL") == []


def test_email_no_se_duplica_como_url():
    text = "Escriba a soporte@mesa-ayuda.xyz para más información"
    assert by_type(text, "EMAIL") == ["soporte@mesa-ayuda.xyz"]
    assert by_type(text, "URL") == []


def test_telefono():
    assert by_type("Llámenos al +51 987 654 321 hoy", "TELEFONO") == ["+51 987 654 321"]
    assert by_type("Son 3 personas y 25 soles", "TELEFONO") == []


def test_organizacion_sin_distinguir_mayusculas():
    assert by_type("Su cuenta bcp fue bloqueada. Atte. PayPal", "ORG") == ["bcp", "PayPal"]


def test_marca_ambigua_requiere_mayuscula():
    assert by_type("Necesito una visa de trabajo", "ORG") == []
    assert by_type("Su tarjeta Visa fue rechazada", "ORG") == ["Visa"]


def test_posiciones_y_orden():
    text = "BBVA: entre a http://x.xyz o escriba a a@b.com"
    ents = extract_entities(text, use_spacy=False)
    assert [e["type"] for e in ents] == ["ORG", "URL", "EMAIL"]
    assert all(text[e["start"]:e["end"]] == e["text"] for e in ents)


def test_texto_vacio():
    assert extract_entities("") == []
