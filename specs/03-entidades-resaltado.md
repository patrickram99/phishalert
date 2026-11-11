# 03 — Extracción de entidades y resaltado (Evidencia 3)

## Objetivo

Mostrarle al usuario **por qué** un mensaje es sospechoso: qué enlaces, correos y organizaciones contiene, y qué frases siguen patrones típicos de phishing.

## Requisitos — entidades (`entities.py`)

- **R1** `extract_entities(texto)` devuelve una lista de `{"type", "text", "start", "end"}` ordenada por posición, con `texto[start:end] == text`.
- **R2** Tipos: `URL`, `EMAIL`, `TELEFONO`, `ORG`.
- **R3** `URL`: con esquema (`http://`, `https://`), con `www.` y dominios sin esquema con TLD conocido (`bit.ly/abc`, `banco-seguro.com/login`). No incluye la puntuación final de la frase.
- **R4** `EMAIL`: direcciones completas; un correo no se reporta además como URL.
- **R5** `TELEFONO`: secuencias con 9 a 15 dígitos, con `+`, espacios, guiones o paréntesis opcionales.
- **R6** `ORG`: (a) lista de marcas frecuentemente suplantadas (bancos peruanos, servicios de pago, tecnológicas, courier, entidades del Estado), sin distinguir mayúsculas; (b) entidades `ORG` del modelo spaCy `xx_ent_wiki_sm` si está instalado. Sin spaCy el módulo sigue funcionando solo con (a).
- **R7** Las entidades no se solapan entre sí; ante conflicto gana la que empieza antes y, a igual inicio, la más larga.

## Requisitos — resaltado (`highlight.py`)

- **R8** `find_suspicious(texto)` devuelve `{"category", "text", "start", "end"}` sin solapes.
- **R9** Categorías: `datos_personales`, `premio`, `amenaza`, `urgencia`.
- **R10** Léxico en español e inglés, insensible a mayúsculas y tolerante a tildes omitidas (`contraseña`/`contrasena`, `verificación`/`verificacion`).
- **R11** `heuristic_score(texto)` devuelve un puntaje en [0, 1] a partir de las categorías presentes y de la existencia de enlaces; se usa solo cuando no hay modelo (D5 de la visión).

## Requisitos — integración (`pipeline.py`)

- **R12** `analyze(texto, classifier=None)` devuelve `label`, `prob_phishing`, `mode` (`modelo`/`heuristico`), `entities`, `highlights` y `segments`.
- **R13** `segments` es una lista de `(fragmento, etiqueta | None)` que reconstruye el texto completo al concatenarse; combina resaltados y entidades.

## Criterios de aceptación

- [ ] `pytest tests/` pasa (casos ES y EN de cada tipo y categoría).
- [ ] Un mensaje legítimo sin patrones devuelve cero resaltados.
- [ ] `"".join(f for f, _ in segments) == texto` para cualquier entrada.

## Fuera de alcance (pasa a Ev4)

- Riesgo de URL (IP, acortadores, dominio que no coincide con la organización).
- Resaltado por atribución del modelo.

## Tareas

Ver `tasks.md` § 03.
