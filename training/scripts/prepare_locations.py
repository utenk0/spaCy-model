import pandas as pd
from pathlib import Path
import json

INPUT = Path("/Users/liza/uk_fast_geotag/data/raw/classifier.xlsx")
OUTPUT = Path("/Users/liza/uk_fast_geotag/data/processed/locations.jsonl")

CATEGORY_TO_LABEL = {
    "O": "LOC",   # область
    "P": "LOC",   # район
    "H": "GPE",   # громада
    "M": "GPE",   # місто
    "C": "GPE",   # село
    "X": "GPE",   # селище
}


def main():
    df = pd.read_excel(INPUT, sheet_name="Кодифікатор", header=3)

    print("Correct headers:", df.columns.tolist())

    name_col = "Назва об’єкта"
    cat_col = "Категорія об’єкта"

    print("Унікальні категорії:", df[cat_col].unique())

    locations = []

    for _, row in df.iterrows():
        name = row.get(name_col)
        cat = row.get(cat_col)

        if pd.isna(name) or pd.isna(cat):
            continue

        cat = str(cat).strip()

        if cat in CATEGORY_TO_LABEL:
            label = CATEGORY_TO_LABEL[cat]

            locations.append({
                "name": str(name).strip(),
                "label": label
            })

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for loc in locations:
            f.write(json.dumps(loc, ensure_ascii=False) + "\n")

    print(f"Готово! Витягнуто {len(locations)} локацій.")


if __name__ == "__main__":
    main()
