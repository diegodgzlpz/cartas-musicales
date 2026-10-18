"""Exporta el CSV de tarjetas a web/cards.js para la web de juego.

Uso: python web/build_data.py [--csv cards_with_design_columns.csv]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["id", "artist", "title", "year", "month", "spotify_url", "bg_hex", "text_color"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera web/cards.js desde el CSV enriquecido.")
    parser.add_argument("--csv", default=str(ROOT / "cards_with_design_columns.csv"))
    parser.add_argument("--out", default=str(ROOT / "web" / "cards.js"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv, sep=";", dtype=str).fillna("")
    missing = set(FIELDS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {sorted(missing)}")

    # Formato compacto: lista de filas en el orden de FIELDS
    rows = df[FIELDS].values.tolist()
    payload = json.dumps({"fields": FIELDS, "rows": rows}, ensure_ascii=False, separators=(",", ":"))
    Path(args.out).write_text(f"window.CARD_DATA={payload};\n", encoding="utf-8")
    print(f"{len(rows)} tarjetas exportadas a {args.out}")


if __name__ == "__main__":
    main()
