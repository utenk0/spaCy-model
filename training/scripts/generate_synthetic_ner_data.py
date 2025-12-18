import json
import random
from pathlib import Path

INPUT = Path("/Users/liza/uk_fast_geotag/data/processed/locations.jsonl")
OUTPUT = Path("/Users/liza/uk_fast_geotag/data/processed/synthetic_ner.jsonl")

TEMPLATES = {
    "GPE": [
        "У {name} сьогодні сталися важливі події.",
        "Місцева влада повідомила про зміни в {name}.",
        "Ситуація в {name} залишається напруженою.",
        "У районі {name} було зафіксовано обстріли.",
        "ЗСУ просуваються поблизу {name}.",
        "Мешканці {name} повідомляють про вибухи.",
        "У {name} відкрили новий центр гуманітарної допомоги.",
    ],
    "LOC": [
        "У {name} оголошено повітряну тривогу.",
        "Події розгортаються на території {name}.",
        "Ситуація в {name} швидко змінюється.",
        "Військові повідомили про активність у {name}.",
        "На території {name} спостерігається рух техніки.",
        "Жителі {name} чули звуки вибухів.",
        "У {name} працюють служби реагування.",
    ]
}


def load_locations(path):
    locations = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            locations.append(rec)
    return locations


def generate_examples(locations, limit_per_type=5000):
    examples = []

    grouped = {"GPE": [], "LOC": []}
    for loc in locations:
        if loc["label"] in grouped:
            grouped[loc["label"]].append(loc["name"])

    for label in grouped:
        names = grouped[label]
        templates = TEMPLATES[label]

        for i in range(min(limit_per_type, len(names))):
            name = names[i]
            template = random.choice(templates)
            sentence = template.format(name=name)

            start = sentence.index(name)
            end = start + len(name)

            examples.append({
                "text": sentence,
                "entities": [(start, end, label)]
            })

    return examples


def save_examples(examples, path):
    with open(path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


def main():
    locations = load_locations(INPUT)
    print(f"Loaded {len(locations)} locations")

    examples = generate_examples(locations, limit_per_type=7000)
    print(f"Generated {len(examples)} synthetic NER examples")

    save_examples(examples, OUTPUT)
    print(f"Saved to {OUTPUT}")


if __name__ == "__main__":
    main()
