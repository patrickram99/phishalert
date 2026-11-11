"""Extracción de entidades: enlaces, correos, teléfonos y organizaciones (spec 03, R1-R7)."""

from __future__ import annotations

import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")

_TLDS = (
    "com|net|org|pe|info|xyz|top|ly|co|io|me|app|site|online|click|link|gob|gov|edu|biz|"
    "es|mx|ar|cl|us|uk|ru|cn|tk|ml|shop|live|club|gl|gd|cc"
)
_URL_CHARS = r"[^\s<>\"'()\[\]{}]"
URL_RE = re.compile(
    # Con esquema o www. (sin distinguir mayúsculas)
    rf"(?i:https?://|www\.){_URL_CHARS}+"
    # Dominio sin esquema: solo minúsculas, para no confundir "Hola.Me" con un dominio
    rf"|(?<![\w@.-])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:{_TLDS})\b(?:/{_URL_CHARS}*)?"
)

PHONE_RE = re.compile(r"(?<![\w/.-])\+?\(?\d[\d ().-]{6,18}\d(?!\w)")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}[.-]\d{1,2}[.-]\d{2,4}")

# Marcas y entidades frecuentemente suplantadas. Sin distinguir mayúsculas.
BRANDS = [
    "Banco de Crédito del Perú", "Banco de Credito del Peru", "Banco de Crédito",
    "Banco de Credito", "BCP", "BBVA", "Interbank", "Scotiabank", "Banco de la Nación",
    "Banco de la Nacion", "BanBif", "Banco Pichincha", "Caja Arequipa", "Caja Huancayo",
    "Yape", "SUNAT", "RENIEC", "EsSalud", "Indecopi", "Serpost", "Movistar", "Bitel",
    "PayPal", "Mastercard", "American Express", "Western Union", "Microsoft", "Outlook",
    "Office 365", "OneDrive", "Google", "Gmail", "iCloud", "Amazon", "Netflix", "Spotify",
    "Facebook", "Instagram", "WhatsApp", "Telegram", "LinkedIn", "Dropbox", "DocuSign",
    "eBay", "DHL", "FedEx", "USPS", "Mercado Libre", "MercadoLibre", "Mercado Pago",
    "Binance", "Coinbase", "Wells Fargo", "Bank of America", "Citibank", "HSBC",
    "Santander",
]
# Nombres que también son palabras comunes: solo con su capitalización exacta.
BRANDS_CASE_SENSITIVE = ["Visa", "Apple", "Chase", "UPS", "IRS", "Plin", "Entel", "Olva"]


def _alternation(words: list[str]) -> str:
    return "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True))


BRAND_RE = re.compile(
    rf"(?<!\w)(?:(?i:{_alternation(BRANDS)})|{_alternation(BRANDS_CASE_SENSITIVE)})(?!\w)"
)

_TRAILING = ".,;:!?…"

_nlp = None
_nlp_tried = False


def _get_nlp():
    """Carga perezosa del modelo multilingüe de spaCy; None si no está instalado."""
    global _nlp, _nlp_tried
    if not _nlp_tried:
        _nlp_tried = True
        try:
            import spacy

            _nlp = spacy.load("xx_ent_wiki_sm", disable=["parser"])
        except Exception:
            _nlp = None
    return _nlp


def _ent(kind: str, text: str, start: int, end: int) -> dict:
    return {"type": kind, "text": text[start:end], "start": start, "end": end}


def resolve_overlaps(spans: list[dict]) -> list[dict]:
    """Gana el span que empieza antes; a igual inicio, el más largo (R7)."""
    out: list[dict] = []
    last_end = -1
    for s in sorted(spans, key=lambda s: (s["start"], -(s["end"] - s["start"]))):
        if s["start"] >= last_end:
            out.append(s)
            last_end = s["end"]
    return out


def extract_entities(text: str, use_spacy: bool = True) -> list[dict]:
    """Devuelve [{"type", "text", "start", "end"}] ordenado por posición."""
    if not text:
        return []
    found: list[dict] = []

    emails = [_ent("EMAIL", text, m.start(), m.end()) for m in EMAIL_RE.finditer(text)]
    found.extend(emails)

    for m in URL_RE.finditer(text):
        start, end = m.start(), m.end()
        while end > start and text[end - 1] in _TRAILING:
            end -= 1
        if end - start < 4:
            continue
        if any(start < e["end"] and e["start"] < end for e in emails):
            continue
        found.append(_ent("URL", text, start, end))

    for m in PHONE_RE.finditer(text):
        chunk = m.group()
        digits = sum(c.isdigit() for c in chunk)
        if not 9 <= digits <= 15 or _DATE_RE.match(chunk):
            continue
        found.append(_ent("TELEFONO", text, m.start(), m.end()))

    found.extend(_ent("ORG", text, m.start(), m.end()) for m in BRAND_RE.finditer(text))

    if use_spacy:
        nlp = _get_nlp()
        if nlp is not None:
            for ent in nlp(text[:5000]).ents:
                if ent.label_ == "ORG" and len(ent.text.strip()) > 1:
                    found.append(_ent("ORG", text, ent.start_char, ent.end_char))

    return resolve_overlaps(found)
