"""Inferencia con el modelo afinado (spec 02, R6)."""

from __future__ import annotations


class PhishClassifier:
    def __init__(self, model_dir: str, device: str | None = None, max_len: int = 256):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self._torch = torch
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_len = max_len
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.model.to(self.device).eval()

    def predict_batch(self, texts: list[str], batch_size: int = 32) -> list[dict]:
        torch = self._torch
        results: list[dict] = []
        for i in range(0, len(texts), batch_size):
            batch = [t or "" for t in texts[i:i + batch_size]]
            enc = self.tokenizer(
                batch, truncation=True, max_length=self.max_len, padding=True, return_tensors="pt"
            ).to(self.device)
            with torch.no_grad():
                probs = torch.softmax(self.model(**enc).logits.float(), dim=-1)[:, 1]
            for p in probs.tolist():
                results.append({"label": "phishing" if p >= 0.5 else "legitimo", "prob_phishing": p})
        return results

    def predict(self, text: str) -> dict:
        return self.predict_batch([text])[0]
