uk_fast_geotag is a lightweight, CPU-optimized spaCy NER model for extracting Ukrainian geographic locations from raw text.
It is inspired by the German fast geotagging model used in the CommonCrawlNewsDataSet project but fully adapted to Ukrainian administrative terminology and news language.

The model runs entirely offline, loads instantly with spaCy, and focuses on high recall for Ukrainian place names.

**Features:**

- Fast CPU inference, no GPU required

- Fully offline after installation

- Model size under ~800 MB

- Optimized for Ukrainian news text

**Two NER labels:**

  GPE — cities, towns, villages, hromadas

  LOC — oblasts, raions, rivers, mountains, general geographic objects

Recognizes current and historical place names (pre-decommunization)

High recall for official names from the Ministry’s administrative-territorial classifier

**Installation:**

After building the wheel/tar.gz package:

pip install uk_fast_geotag-1.0.0.tar.gz

Then:

import spacy
nlp = spacy.load("uk_fast_geotag")

**Usage Example**
import spacy
nlp = spacy.load("uk_fast_geotag")

doc = nlp("Учора в Бахмуті та Авдіївці тривали важкі бої, а в Херсонській області звільнили ще два села.")
print([(ent.text, ent.label_) for ent in doc.ents])


Expected output:
Бахмуті                GPE
Авдіївці               GPE
Херсонській області    LOC


Data Sources Used

Official administrative-territorial classifier (Ministry of Regional Development)

Ukrainian news corpora (CC-NEWS Ukrainian slice, UkrInform archives, etc.)

VIINA dataset (event_info_latest, control_latest)

Additional open-source Ukrainian NER datasets

Model Architecture

Base transformer: youscan/ukr-roberta-base (recommended)

Fine-tuning: LoRA / QLoRA for memory-efficient training

spaCy pipeline: ["tok2vec", "ner"] or transformer-based depending on environment

CPU-optimized configuration for fast inference

**Training Summary**

  All data normalized to current administrative names

  Historical → modern name mapping included (e.g., "Артемівськ" → "Бахмут")

  Synthetic data generation script included

  spaCy .spacy binary data created for training/dev splits
