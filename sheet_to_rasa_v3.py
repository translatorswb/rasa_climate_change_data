#!/usr/bin/env python
# coding: utf-8


import gspread
import os

data = {
    'lang': ['eng', 'hindi'],
    'bot_strings_sheet': 'https://docs.google.com/spreadsheets/d/1xyJ0T0jcxLw-Rhow1_RBtAaYkjjHt96PbllgpKtc5wI/edit?pli=1#gid=1991829780'
    
}

MODEL_SHEET_LINK = data['bot_strings_sheet']
LANGUAGES = data['lang']
IS_MULTILINGUAL = len(LANGUAGES) > 1

VERSION = "3.0"
SESSION_EXPIRATION_TIME = '60'
CARRY_OVER_SLOTS_TO_NEW_SESSION = 'true'

DOMAIN_FOLDER = 'domains'
DOMAIN_FILE = 'domain_v3.yml'
DOMAIN_CLASSIFIER_FILE = 'domain_v3_for_classifier.yml'
STORIES_FILE = 'stories.yml'
STORIES_FOLDER = 'data_core'

#column_ids
COLUMN_DICT = {
    'INTENT' : 'Intent',
    'EXAMPLE_HINDI' : 'Sanitized Question',
    'EXAMPLE_ENG' : 'Sanitized Question Translation in English',
    'RESPONSE_HINDI' : 'Answer Transcription',
    'RESPONSE_ENG' : 'Answer Translation in English '
}

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

create_directory_if_not_exists('models/core_model')
create_directory_if_not_exists('models/spacy/hi')

def list_unique(input_list):
    # Step 1: Convert list to a set to remove duplicates
    unique_set = set(input_list)

    # Step 2: Filter out empty strings using list comprehension
    filtered_list = [item for item in unique_set if item]

    # Step 3: Convert the filtered set back to a list
    unique_list_without_empty = list(filtered_list)
    
    modified_list = [s.replace(' ', '_') for s in unique_list_without_empty]
    
    return modified_list

def get_examples(lang, all_sheet_records):
    examples_dict = {}
    for entry in all_sheet_records:
        intent = entry.get(COLUMN_DICT['INTENT'])
        an_example = entry.get(COLUMN_DICT['EXAMPLE_{language}'.format(language=lang.upper())])
        if intent and an_example:
            if intent not in examples_dict:
                examples_dict[intent] = []

            examples_dict[intent].append(an_example)
    return examples_dict

def get_response(lang, all_sheet_records):
    response_dict = {}
    for entry in all_sheet_records:
        intent = entry.get(COLUMN_DICT['INTENT'])
        a_response = entry.get(COLUMN_DICT['RESPONSE_{language}'.format(language=lang.upper())])
        if intent and a_response:
            if intent not in response_dict:
                response_dict[intent] = []
            
            response_dict[intent].append(a_response)
    return response_dict
def get_all_examples(lang, all_sheet_records):
    list_all = []
    for entry in all_sheet_records:
        intent = entry.get(COLUMN_DICT['INTENT'])
        an_example = entry.get(COLUMN_DICT['EXAMPLE_{language}'.format(language=lang.upper())])
        if intent and an_example:
#             if intent not in examples_dict:
#                 examples_dict[intent] = []

            list_all.append(an_example)
    return list_all

# ### Connect to spreadsheets

gc = gspread.service_account()


#Bot strings
try:
    sheet = gc.open_by_url(MODEL_SHEET_LINK)
#         answers_worksheet = sheet.worksheet("Answers")

except Exception as e:
    print("Cannot access spreadsheet")
    print(e)
#         sys.exit()
        

first_sheet = sheet.worksheet("Climate Change T1")
second_sheet = sheet.worksheet("Climate Change T2")
third_sheet = sheet.worksheet("Climate Change T3")

all_sheet_records = (first_sheet.get_all_records())
all_sheet_records.extend(second_sheet.get_all_records())
all_sheet_records.extend(third_sheet.get_all_records())

for record in all_sheet_records:
    intent = record.get('Intent')
    if intent and not intent.isspace():
        record['Intent'] = intent.replace(' ', '_')


intents = [entry["Intent"] for entry in all_sheet_records]
intents = list_unique(intents)



create_directory_if_not_exists(DOMAIN_FOLDER)
with open(DOMAIN_FOLDER+'/'+DOMAIN_FILE, 'w') as f:
    
    #version: "3.0"
    f.write('version: \"{VERSION}\"\n'.format(VERSION=VERSION))
    
    #write intents
    f.write('\nintents:\n\n')
    
    for an_intent in sorted(intents):
        f.write('  - {an_intent}\n'.format(an_intent=an_intent))
    
    f.write('\nactions:\n\n')
    
    actions_from_intents = []
    
    for an_intent in sorted(intents):
        f.write('  - utter_answer_{an_intent}\n'.format(an_intent=an_intent))
        actions_from_intents.append('utter_answer_{an_intent}'.format(an_intent=an_intent))

                                    #Write tracker session configuration
    f.write('\nsession_config:\n')
    f.write('  session_expiration_time: %s\n'%SESSION_EXPIRATION_TIME)
    f.write('  carry_over_slots_to_new_session: %s\n'%CARRY_OVER_SLOTS_TO_NEW_SESSION)


with open(DOMAIN_FOLDER+'/'+DOMAIN_CLASSIFIER_FILE, 'w') as f:
    
    #version: "3.0"
    f.write('version: \"{VERSION}\"\n'.format(VERSION=VERSION))
    
    #write intents
    f.write('\nintents:\n\n')
    
    for a_lang in sorted(LANGUAGES):
        f.write('  - lang_{a_lang}\n'.format(a_lang=a_lang))

                                    #Write tracker session configuration
    f.write('\nsession_config:\n')
    f.write('  session_expiration_time: %s\n'%SESSION_EXPIRATION_TIME)
    f.write('  carry_over_slots_to_new_session: %s\n'%CARRY_OVER_SLOTS_TO_NEW_SESSION)

create_directory_if_not_exists(STORIES_FOLDER)
with open(STORIES_FOLDER+'/'+STORIES_FILE, 'w') as f:
    
    #version: "3.0"
    f.write('version: \"{VERSION}\"\n\n'.format(VERSION=VERSION))
    
    f.write('stories: \n\n')
    
    for an_intent in sorted(intents):
        f.write('- story: {an_intent}\n'.format(an_intent=an_intent))
        f.write('  steps:\n')
        f.write('  - intent: {an_intent}\n'.format(an_intent=an_intent))
        f.write('  - action: utter_answer_{an_intent}\n'.format(an_intent=an_intent))
  

for lang in LANGUAGES:
    path_lang = 'data_nlu/{lang}'.format(lang=lang)
    create_directory_if_not_exists(path_lang)

    with open('{path_lang}/nlu_data_{lang}.yml'.format(path_lang=path_lang, lang=lang), 'w', encoding='utf-8') as f:
         #version: "3.0"
        f.write('version: \"{VERSION}\"\n\n'.format(VERSION=VERSION))
        f.write('nlu:\n')
        intent_examples_dict = get_examples(lang, all_sheet_records)
        for intent, examples in intent_examples_dict.items():
            f.write('- intent: {intent}\n'.format(intent=intent))
            f.write('  examples: |\n')
            for an_example in examples:
                f.write('    - {an_example}\n'.format(an_example=an_example))     


    # for lang in LANGUAGES:
    path_lang = 'data_nlu/classifier'
    create_directory_if_not_exists(path_lang)

    with open('{path_lang}/nlu_data_classifier.yml'.format(path_lang=path_lang), 'w', encoding='utf-8') as f:
         #version: "3.0"
        f.write('version: \"{VERSION}\"\n\n'.format(VERSION=VERSION))
        f.write('nlu:\n')
#         intent_examples_dict = get_examples(lang, all_sheet_records)
#         for intent, examples in intent_examples_dict.items():
        for lang in LANGUAGES:
            all_list = get_all_examples(lang, all_sheet_records)
            f.write('- intent: lang_{lang}\n'.format(lang=lang))
            f.write('  examples: |\n')
            for an_example in all_list:
                f.write('    - {an_example}\n'.format(an_example=an_example))     

import yaml

# ...

for lang in LANGUAGES:
    path_lang = 'responses'
    create_directory_if_not_exists(path_lang)

    with open(f'{path_lang}/responses_{lang}.yml', 'w', encoding='utf-8') as f:
        f.write('responses:\n')
        intent_response_dict = get_response(lang, all_sheet_records)
        for intent, responses in intent_response_dict.items():
            f.write(f'  utter_answer_{intent}:\n')  # Add two spaces before the key
            for a_response in responses:
                indented_response = " " * 8 + f"- text: |-\n" + "\n".join(" " * 12 + line for line in a_response.splitlines()) + "\n"
                f.write(indented_response)  # Write the indented response with '- text:' prefix

