# RASA multilingual FAQ bot creator

RASA multilingual FAQ bot creator creates all the necessary files to train a RASA chatbot from a Google Docs spreadsheet. 

To access the source spreadsheet which this repository uses, [click here](https://docs.google.com/spreadsheets/d/1OpTyjwXZjItPugQpprQ86oaV5xU1fUS0A_QELrQMg5U/edit#gid=1991829780). 

In this particular tutorial, we are working with two languages, English and Hindi in three main topics and 25 FAQs in total. 


# Installation

```
pip install -r requirements.txt
```

If you want to connect it to your own spreadsheet, make sure it's publicly accessible and you specify it's link, the languages involved and the column names in these lines of `sheet_to_rasa_v3.py`.

```
data = {
    'lang': ['eng', 'hindi'],
    'bot_strings_sheet': 'https://docs.google.com/spreadsheets/d/1OpTyjwXZjItPugQpprQ86oaV5xU1fUS0A_QELrQMg5U/edit#gid=1133259128'
    
}
...
#column_ids
COLUMN_DICT = {
    'INTENT' : 'Intent',
    'EXAMPLE_HINDI' : 'Sanitized Question',
    'EXAMPLE_ENG' : 'Sanitized Question Translation in English',
    'RESPONSE_HINDI' : 'Answer Transcription',
    'RESPONSE_ENG' : 'Answer Translation in English '
}

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