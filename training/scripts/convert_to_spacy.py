import json
from pathlib import Path
import srsly
from spacy.tokens import DocBin
import spacy

INPUT = Path("/Users/liza/uk_fast_geotag/data/processed/synthetic_ner.jsonl")
TRAIN_OUT = Path("/Users/liza/uk_fast_geotag/data/processed/train.spacy")
DEV_OUT = Path("/Users/liza/uk_fast_geotag/data/processed/dev.spacy")

def main():
    nlp = spacy.blank("xx")  # multilingual

    train_db = DocBin()
    dev_db = DocBin()

    with open(INPUT, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Loaded {len(lines)} examples")

    # 90/10 split
    split = int(len(lines) * 0.9)
    train_lines = lines[:split]
    dev_lines = lines[split:]

    for line in train_lines:
        obj = json.loads(line)
        doc = nlp.make_doc(obj["text"])
        ents = []
        for start, end, label in obj["entities"]:
            ents.append(doc.char_span(start, end, label=label))
        doc.ents = ents
        train_db.add(doc)

    for line in dev_lines:
        obj = json.loads(line)
        doc = nlp.make_doc(obj["text"])
        ents = []
        for start, end, label in obj["entities"]:
            ents.append(doc.char_span(start, end, label=label))
        doc.ents = ents
        dev_db.add(doc)

    train_db.to_disk(TRAIN_OUT)
    dev_db.to_disk(DEV_OUT)

    print("Saved:", TRAIN_OUT, DEV_OUT)

if __name__ == "__main__":
    main()
