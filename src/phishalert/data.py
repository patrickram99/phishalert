"""Obtención y preparación de datos (spec 01)."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

SEED = 42
MIN_CHARS = 10
MAX_CHARS = 2000
TRANSLATE_MAX_CHARS = 500
SEED_ES_PATH = Path(__file__).resolve().parents[2] / "seeds" / "seed_es.csv"
COLUMNS = ["text", "label", "lang", "source"]


def clean_text(text) -> str:
    """Normaliza espacios y recorta (R5)."""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    return re.sub(r"\s+", " ", str(text)).strip()[:MAX_CHARS]


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["text"] = df["text"].map(clean_text)
    df = df[df["text"].str.len() >= MIN_CHARS]
    df = df.drop_duplicates(subset="text").reset_index(drop=True)
    df["label"] = df["label"].astype(int)
    return df[COLUMNS]


def _load_phishing_emails() -> pd.DataFrame:
    from datasets import load_dataset

    raw = load_dataset("zefang-liu/phishing-email-dataset", split="train").to_pandas()
    return pd.DataFrame({
        "text": raw["Email Text"],
        "label": (raw["Email Type"].astype(str).str.strip() == "Phishing Email").astype(int),
        "lang": "en",
        "source": "phishing_email",
    })


def _load_sms_spam() -> pd.DataFrame:
    from datasets import load_dataset

    raw = load_dataset("ucirvine/sms_spam", split="train").to_pandas()
    return pd.DataFrame({"text": raw["sms"], "label": raw["label"], "lang": "en", "source": "sms_spam"})


def load_english(max_per_source: int = 0) -> pd.DataFrame:
    """Descarga las fuentes en inglés; una fuente caída no detiene el proceso (R7)."""
    frames = []
    for name, loader in [("phishing_email", _load_phishing_emails), ("sms_spam", _load_sms_spam)]:
        try:
            df = clean_frame(loader())
        except Exception as exc:  # noqa: BLE001
            print(f"[aviso] no se pudo cargar '{name}': {exc}")
            continue
        if max_per_source and len(df) > max_per_source:
            df = df.sample(max_per_source, random_state=SEED)
        print(f"[datos] {name}: {len(df)} filas")
        frames.append(df)
    if not frames:
        raise RuntimeError("No se pudo descargar ninguna fuente de datos.")
    return pd.concat(frames, ignore_index=True)


def load_seed_es(path: Path = SEED_ES_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["lang"] = "es"
    df["source"] = "semilla_es"
    return clean_frame(df)


def pick_for_translation(df_en: pd.DataFrame, n: int) -> pd.DataFrame:
    """Muestra balanceada por clase, prefiriendo textos cortos (R4)."""
    short = df_en[df_en["text"].str.len() <= TRANSLATE_MAX_CHARS]
    picked = []
    for label in (0, 1):
        pool = short[short["label"] == label]
        picked.append(pool.sample(min(n // 2, len(pool)), random_state=SEED))
    return pd.concat(picked)


def translate_en_es(texts: list[str], batch_size: int = 32) -> list[str]:
    """Traduce EN→ES con MarianMT. Usa GPU si hay."""
    import torch
    from tqdm.auto import tqdm
    from transformers import MarianMTModel, MarianTokenizer

    name = "Helsinki-NLP/opus-mt-en-es"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = MarianTokenizer.from_pretrained(name)
    model = MarianMTModel.from_pretrained(name).to(device).eval()

    order = sorted(range(len(texts)), key=lambda i: len(texts[i]))
    out = [""] * len(texts)
    for i in tqdm(range(0, len(order), batch_size), desc="Traduciendo EN→ES"):
        idx = order[i:i + batch_size]
        enc = tokenizer(
            [texts[j] for j in idx], return_tensors="pt", padding=True, truncation=True, max_length=256
        ).to(device)
        with torch.no_grad():
            gen = model.generate(**enc, num_beams=1, max_length=256)
        for j, t in zip(idx, tokenizer.batch_decode(gen, skip_special_tokens=True)):
            out[j] = t
    return out


def add_splits(df: pd.DataFrame) -> pd.DataFrame:
    """Partición estratificada por clase e idioma 80/10/10 (R6)."""
    from sklearn.model_selection import train_test_split

    df = df.reset_index(drop=True)
    strata = df["label"].astype(str) + "_" + df["lang"]
    train_idx, rest_idx = train_test_split(df.index, test_size=0.2, random_state=SEED, stratify=strata)
    val_idx, test_idx = train_test_split(
        rest_idx, test_size=0.5, random_state=SEED, stratify=strata.loc[rest_idx]
    )
    df["split"] = "train"
    df.loc[val_idx, "split"] = "val"
    df.loc[test_idx, "split"] = "test"
    return df


def build_dataset(translate_n: int = 3000, max_per_source: int = 0) -> pd.DataFrame:
    en = load_english(max_per_source)
    frames = []

    if translate_n > 0:
        chosen = pick_for_translation(en, translate_n)
        es = chosen.copy()
        es["text"] = translate_en_es(chosen["text"].tolist())
        es["lang"] = "es"
        es["source"] = es["source"] + "_traducido"
        frames.append(es)
        # Cada mensaje queda en un solo idioma: evita fuga entre train y test.
        en = en.drop(index=chosen.index)

    frames = [en, *frames, load_seed_es()]
    return add_splits(clean_frame(pd.concat(frames, ignore_index=True)))


def summarize(df: pd.DataFrame) -> str:
    lines = [f"Total: {len(df)} filas"]
    for col in ("source", "lang", "label", "split"):
        counts = ", ".join(f"{k}={v}" for k, v in df[col].value_counts().sort_index().items())
        lines.append(f"  {col}: {counts}")
    lines.append("  label x lang:")
    for (lang, label), v in df.groupby(["lang", "label"]).size().items():
        lines.append(f"    {lang} / {label}: {v}")
    return "\n".join(lines)
