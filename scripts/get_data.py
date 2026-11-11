"""Descarga, unifica y traduce los datos de PhishAlert (spec 01).

Uso:  python scripts/get_data.py [--out data/phishalert.csv] [--translate-n 3000] [--no-translate]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phishalert.data import build_dataset, summarize  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="data/phishalert.csv")
    parser.add_argument("--translate-n", type=int, default=3000,
                        help="mensajes en inglés a traducir al español")
    parser.add_argument("--no-translate", action="store_true", help="omitir la traducción")
    parser.add_argument("--max-per-source", type=int, default=0, help="límite de filas por fuente (0 = todas)")
    args = parser.parse_args()

    df = build_dataset(
        translate_n=0 if args.no_translate else args.translate_n,
        max_per_source=args.max_per_source,
    )
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"\nGuardado en {out}")
    print(summarize(df))


if __name__ == "__main__":
    main()
