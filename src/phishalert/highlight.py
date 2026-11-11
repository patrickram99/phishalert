"""Resaltado de expresiones sospechosas con un léxico bilingüe (spec 03, R8-R11).

Los patrones se escriben sin tildes y en minúsculas; se buscan sobre una copia del texto
sin tildes y de la misma longitud, de modo que las posiciones valen para el original.
"""

from __future__ import annotations

import re
import unicodedata

CATEGORIES = ("datos_personales", "premio", "amenaza", "urgencia")

_LEXICON: dict[str, list[str]] = {
    "datos_personales": [
        # ES
        r"(?:confirm|verifi|actuali|valid|ingres|proporcion|envi)\w*\s+(?:(?:su|sus|tu|tus|los|el|la)\s+)?"
        r"(?:datos|informacion|cuenta|identidad|clave|contrasena|tarjeta|credenciales)\w*",
        r"(?:numero|nro\.?)\s+de\s+(?:tarjeta|cuenta|dni|documento)",
        r"contrasena",
        r"clave\s+(?:de\s+)?(?:internet|secreta|token|digital|dinamica|web)",
        r"codigo\s+(?:de\s+)?(?:verificacion|seguridad|sms|otp)",
        r"datos\s+(?:personales|bancarios)",
        r"inici\w+\s+sesion",
        r"cvv",
        # EN
        r"(?:confirm|verify|update|validate|provide|enter|submit)\s+(?:your\s+)?"
        r"(?:account|identity|password|information|details|billing|payment|card|credentials|login)\w*"
        r"(?:\s+(?:information|details))?",
        r"password",
        r"social\s+security(?:\s+number)?",
        r"credit\s+card(?:\s+(?:number|details))?",
        r"bank\s+account(?:\s+(?:number|details))?",
        r"login\s+credentials",
        r"personal\s+(?:information|details|data)",
    ],
    "premio": [
        # ES
        r"(?:has|ha)\s+(?:sido\s+)?(?:ganado|seleccionad[oa]|elegid[oa])",
        r"ganador(?:a|es)?",
        r"ganaste",
        r"premio\w*",
        r"sorteo",
        r"loteria",
        r"gratis",
        r"regalo",
        r"felicidades|felicitaciones",
        r"bono\s+(?:de|gratis|exclusivo)",
        r"reclam\w+\s+(?:tu|su|el)\s+(?:premio|regalo|bono|recompensa)",
        r"herencia",
        r"millones\s+de\s+(?:dolares|soles|euros)",
        # EN
        r"you(?:\s+have|['’]ve)?\s+(?:won|been\s+selected|been\s+chosen)",
        r"winner",
        r"prize",
        r"lottery",
        r"free\s+(?:gift|iphone|entry|money|vacation|tickets?)",
        r"congratulations",
        r"claim\s+(?:your|now|it)(?:\s+(?:prize|reward|gift))?",
        r"gift\s+card",
        r"cash\s+(?:prize|reward|bonus)",
        r"inheritance",
        r"million\s+(?:dollars|usd|pounds|euros)",
    ],
    "amenaza": [
        # ES
        r"(?:cuenta|tarjeta|acceso|servicio|linea)\s+(?:ha\s+sido|sera|fue|esta|se\s+encuentra|quedara)\s+"
        r"(?:\w+\s+)?(?:bloquead|suspendid|cancelad|desactivad|restringid|inhabilitad|comprometid)\w*",
        r"(?:bloque|suspen|cancel|desactiv|inhabilit)\w+\s+(?:de\s+)?(?:su|tu|la)\s+(?:cuenta|tarjeta|acceso|servicio)",
        r"actividad\s+(?:sospechosa|inusual|no\s+autorizada)",
        r"acceso\s+no\s+autorizado",
        r"intento\s+de\s+(?:acceso|inicio\s+de\s+sesion)",
        r"de\s+lo\s+contrario|caso\s+contrario",
        r"acciones\s+legales",
        r"perdera\s+(?:el\s+)?acceso",
        r"sera\s+(?:bloquead|suspendid|cancelad|eliminad)\w*",
        # EN
        r"(?:account|card|access|service)\s+(?:has\s+been|will\s+be|is|was)\s+"
        r"(?:\w+\s+)?(?:suspended|blocked|locked|closed|disabled|restricted|deactivated|limited|compromised|terminated)",
        r"(?:suspend|block|lock|close|disable|deactivate|terminate)\w*\s+(?:your|the)\s+(?:account|card|access)",
        r"(?:suspicious|unusual|unauthorized)\s+(?:activity|login|sign-?in|access|transaction)",
        r"security\s+(?:alert|breach|warning)",
        r"legal\s+action",
        r"failure\s+to\s+(?:comply|verify|respond|do\s+so)",
        r"will\s+be\s+(?:suspended|blocked|locked|closed|terminated|deleted)",
    ],
    "urgencia": [
        # ES
        r"urgente(?:mente)?",
        r"inmediat(?:o|a|amente)",
        r"ahora\s+mismo",
        r"hoy\s+mismo",
        r"cuanto\s+antes",
        r"lo\s+antes\s+posible",
        r"ultim[oa]\s+(?:aviso|oportunidad|dia|advertencia)",
        r"(?:en|dentro\s+de)\s+(?:las\s+proximas\s+|los\s+proximos\s+)?\d+\s+(?:horas?|minutos|dias?)",
        r"(?:expira|vence|caduca)\w*\s+(?:hoy|pronto|en\s+\d+)",
        r"tiempo\s+limitado",
        r"hag?a\s+clic\s+(?:aqui|en)",
        r"haz\s+clic",
        r"no\s+ignore\w*",
        # EN
        r"urgent(?:ly)?",
        r"immediate(?:ly)?",
        r"right\s+(?:now|away)",
        r"as\s+soon\s+as\s+possible|asap",
        r"act\s+now",
        r"final\s+(?:notice|warning|reminder)",
        r"last\s+chance",
        r"within\s+\d+\s+(?:hours?|minutes|days?)",
        r"expires?\s+(?:today|soon|in\s+\d+)",
        r"limited\s+time",
        r"click\s+(?:here|below|the\s+link|on\s+the\s+link)",
        r"do\s+not\s+ignore",
        r"today\s+only",
    ],
}

_COMPILED = {
    cat: re.compile(r"(?<!\w)(?:" + "|".join(pats) + r")(?!\w)", re.IGNORECASE)
    for cat, pats in _LEXICON.items()
}

_WEIGHTS = {"datos_personales": 0.30, "amenaza": 0.30, "premio": 0.25, "urgencia": 0.15}
_URL_WEIGHT = 0.15


def strip_accents(text: str) -> str:
    """Quita tildes carácter a carácter, conservando la longitud del texto."""
    out = []
    for ch in text:
        base = unicodedata.normalize("NFD", ch)
        out.append(base[0] if len(base) > 1 and not unicodedata.combining(base[0]) else ch)
    return "".join(out)


def find_suspicious(text: str) -> list[dict]:
    """Devuelve [{"category", "text", "start", "end"}] sin solapes, ordenado por posición."""
    if not text:
        return []
    plain = strip_accents(text)
    spans = [
        {"category": cat, "text": text[m.start():m.end()], "start": m.start(), "end": m.end()}
        for cat, rx in _COMPILED.items()
        for m in rx.finditer(plain)
    ]
    out: list[dict] = []
    last_end = -1
    for s in sorted(spans, key=lambda s: (s["start"], -(s["end"] - s["start"]))):
        if s["start"] >= last_end:
            out.append(s)
            last_end = s["end"]
    return out


def heuristic_score(highlights: list[dict], has_url: bool = False) -> float:
    """Puntaje en [0, 1] para el modo sin modelo (R11). No reemplaza al clasificador."""
    remaining = 1.0
    for cat in {h["category"] for h in highlights}:
        remaining *= 1.0 - _WEIGHTS.get(cat, 0.0)
    if has_url:
        remaining *= 1.0 - _URL_WEIGHT
    return round(1.0 - remaining, 4)
