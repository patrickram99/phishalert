# 01 — Datos (Evidencia 3)

## Objetivo

Un script reproducible que descarga datos públicos, los unifica y produce un único CSV bilingüe listo para entrenar.

## Requisitos

- **R1** `python scripts/get_data.py` genera `data/phishalert.csv` sin intervención manual.
- **R2** Columnas de salida: `text` (str), `label` (0 legítimo / 1 phishing), `lang` (`en`/`es`), `source`, `split` (`train`/`val`/`test`).
- **R3** Fuentes en inglés (Hugging Face Hub):
  - `zefang-liu/phishing-email-dataset` — columnas `Email Text`, `Email Type` (`Safe Email` / `Phishing Email`).
  - `ucirvine/sms_spam` (config `plain_text`) — columnas `sms`, `label` (0 ham / 1 spam). El spam por SMS se usa como aproximación de *smishing*.
- **R4** Español:
  - traducción automática EN→ES de una muestra balanceada (`--translate-n`, por defecto 3000) con `Helsinki-NLP/opus-mt-en-es`;
  - los mensajes traducidos se retiran del conjunto en inglés: cada mensaje queda en un solo idioma, para que no haya fuga entre `train` y `test`;
  - conjunto semilla escrito a mano `seeds/seed_es.csv` (ambas clases), versionado en el repo.
- **R5** Limpieza: normalizar espacios, descartar textos vacíos o de menos de 10 caracteres, recortar a 2000 caracteres, eliminar duplicados exactos.
- **R6** Partición estratificada por `label` y `lang` 80/10/10 con semilla 42.
- **R7** Si una fuente falla al descargar, el script avisa y continúa con las demás; falla solo si no queda ninguna.
- **R8** `--no-translate` omite la traducción (para pruebas rápidas sin GPU); `--max-per-source` limita filas por fuente.
- **R9** Al terminar imprime un resumen: filas por `source`, `lang`, `label` y `split`.

## Criterios de aceptación

- [ ] El CSV existe y tiene las cinco columnas de R2.
- [ ] Hay filas de ambas clases en ambos idiomas.
- [ ] No hay textos duplicados ni vacíos.
- [ ] Dos ejecuciones con los mismos argumentos producen la misma partición.

## Fuera de alcance

- Recolección propia de correos reales (privacidad).
- Balanceo sintético de clases más allá del muestreo.

## Limitaciones conocidas

- El español proviene mayormente de traducción automática: calidad media y estilo poco natural.
- `sms_spam` mezcla publicidad no deseada con phishing real.

## Tareas

Ver `tasks.md` § 01.
