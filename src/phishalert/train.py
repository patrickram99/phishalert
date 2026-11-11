"""Afinado del clasificador (spec 02, R1-R5, R7)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from . import LABELS

BASE_MODEL = "distilbert-base-multilingual-cased"
SEED = 42


def subsample_train(train: pd.DataFrame, max_train: int) -> pd.DataFrame:
    """Conserva todo el español y completa con inglés (R7)."""
    if not max_train or len(train) <= max_train:
        return train
    es = train[train["lang"] == "es"]
    if len(es) >= max_train:
        return es.sample(max_train, random_state=SEED)
    en = train[train["lang"] != "es"].sample(max_train - len(es), random_state=SEED)
    return pd.concat([es, en]).sample(frac=1.0, random_state=SEED)


def compute_metrics(eval_pred) -> dict:
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support

    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="binary", pos_label=1, zero_division=0
    )
    return {"accuracy": accuracy_score(labels, preds), "precision": precision, "recall": recall, "f1": f1}


def train(
    data_path: str,
    out_dir: str,
    epochs: float = 1.0,
    max_train: int = 6000,
    max_len: int = 256,
    batch_size: int = 16,
    lr: float = 5e-5,
    base_model: str = BASE_MODEL,
) -> dict:
    import torch
    from datasets import Dataset
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        DataCollatorWithPadding,
        Trainer,
        TrainingArguments,
    )

    df = pd.read_csv(data_path)
    train_df = subsample_train(df[df["split"] == "train"], max_train)
    val_df = df[df["split"] == "val"]
    print(f"[entrenamiento] train={len(train_df)}  val={len(val_df)}  base={base_model}")

    tokenizer = AutoTokenizer.from_pretrained(base_model)

    def to_dataset(frame: pd.DataFrame) -> Dataset:
        ds = Dataset.from_pandas(frame[["text", "label"]].reset_index(drop=True))
        return ds.map(
            lambda b: tokenizer(b["text"], truncation=True, max_length=max_len),
            batched=True,
            remove_columns=["text"],
        )

    model = AutoModelForSequenceClassification.from_pretrained(
        base_model, num_labels=2, id2label=LABELS, label2id={v: k for k, v in LABELS.items()}
    )

    args = TrainingArguments(
        output_dir=str(Path(out_dir) / "_checkpoints"),
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size * 4,
        learning_rate=lr,
        weight_decay=0.01,
        logging_steps=50,
        save_strategy="no",
        report_to="none",
        fp16=torch.cuda.is_available(),
        seed=SEED,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=to_dataset(train_df),
        eval_dataset=to_dataset(val_df),
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )
    trainer.train()

    metrics = {k.replace("eval_", ""): float(v) for k, v in trainer.evaluate().items()}
    metrics.update({"train_rows": len(train_df), "val_rows": len(val_df), "epochs": epochs,
                    "max_len": max_len, "base_model": base_model})

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    trainer.save_model(out_dir)
    tokenizer.save_pretrained(out_dir)
    (Path(out_dir) / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("[validación] " + "  ".join(
        f"{k}={metrics[k]:.4f}" for k in ("accuracy", "precision", "recall", "f1")))
    return metrics
