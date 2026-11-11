"""Afina DistilBERT multilingüe para detectar phishing (spec 02).

Uso:  python scripts/train.py --data data/phishalert.csv --out models/phishalert
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phishalert.train import BASE_MODEL, train  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="data/phishalert.csv")
    parser.add_argument("--out", default="models/phishalert")
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--max-train", type=int, default=6000, help="0 = todo el split de entrenamiento")
    parser.add_argument("--max-len", type=int, default=256)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=5e-5)
    parser.add_argument("--base-model", default=BASE_MODEL)
    args = parser.parse_args()

    train(args.data, args.out, epochs=args.epochs, max_train=args.max_train, max_len=args.max_len,
          batch_size=args.batch_size, lr=args.lr, base_model=args.base_model)


if __name__ == "__main__":
    main()
