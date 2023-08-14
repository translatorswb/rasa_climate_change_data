# Installation
```
pip install -r requirements.txt
```
# Convert data from sheets to rasa files:
```
python3 sheet_to_rasa_v3.py
```

This should create following files:
```
.
├── data_core
│   └── stories.yml
├── data_nlu
│   ├── classifier
│   │   └── nlu_data_classifier.yml
│   ├── eng
│   │   └── nlu_data_eng.yml
│   └── hindi
│       └── nlu_data_hindi.yml
├── domains
│   ├── domain_v3_for_classifier.yml
│   └── domain_v3.yml
├── models
│   ├── core_model
│   └── spacy
│       └── hi
├── README.md
├── requirements.txt
├── responses
│   ├── responses_eng.yml
│   └── responses_hindi.yml
└── sheet_to_rasa_v3.py

11 directories, 11 files
```