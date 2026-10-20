"""Exporta el CSV de tarjetas a web/cards.js para la web de juego.

Añade el estilo y el idioma de categorias.csv (generado con classify_categories.py) para poder
jugar por categorías; las cartas sin clasificar quedan con estos campos vacíos.

Uso: python web/build_data.py [--csv cards_with_design_columns.csv] [--categories categorias.csv]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["id", "artist", "title", "year", "month", "spotify_url", "bg_hex", "text_color"]
CATEGORY_FIELDS = ["genre", "language"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera web/cards.js desde el CSV enriquecido.")
    parser.add_argument("--csv", default=str(ROOT / "cards_with_design_columns.csv"))
    parser.add_argument("--categories", default=str(ROOT / "categorias.csv"))
    parser.add_argument("--out", default=str(ROOT / "web" / "cards.js"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv, sep=";", dtype=str).fillna("")
    missing = set(FIELDS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {sorted(missing)}")

    cat_path = Path(args.categories)
    if cat_path.exists():
        cats = pd.read_csv(cat_path, sep=";", dtype=str, encoding="utf-8-sig").fillna("")
        df = df.merge(cats[["id", *CATEGORY_FIELDS]], on="id", how="left").fillna("")
    else:
        print(f"Aviso: no existe {cat_path}, las cartas van sin estilo ni idioma")
        for f in CATEGORY_FIELDS:
            df[f] = ""

    # Formato compacto: lista de filas en el orden de los campos
    fields = FIELDS + CATEGORY_FIELDS
    rows = df[fields].values.tolist()
    payload = json.dumps({"fields": fields, "rows": rows}, ensure_ascii=False, separators=(",", ":"))
    Path(args.out).write_text(f"window.CARD_DATA={payload};\n", encoding="utf-8")
    print(f"{len(rows)} tarjetas exportadas a {args.out}")


if __name__ == "__main__":
    main()
