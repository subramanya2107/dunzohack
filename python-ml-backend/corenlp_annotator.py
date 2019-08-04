import re
import os
import json
import timeit

from corenlp import StanfordCoreNLP
from config import CORENLP_SERVER_URL, path_to_rules_file


import pprint
pp = pprint.PrettyPrinter(indent=4)

###############################################################################
cur_dir = os.path.dirname(os.path.abspath(__file__))
nlp = StanfordCoreNLP(CORENLP_SERVER_URL, port=9000)
props = {'annotators': 'tokenize,ssplit,pos,lemma,ner,tokensregex', 'outputFormat': 'json', 'ner.additional.tokensregex.rules': path_to_rules_file}
###############################################################################


invalid_filter = re.compile("^[-_|*#,\s]+$")
conditional_invalid = (re.compile(r"^[$€£][^0-9]*$"), "MONEY")
replace_filter = (re.compile(r"^(#\s*[0-9][.0-9]*)|([0-9][.0-9]*\s*#)|[0-9]+$"), "NUMBER")
normalized_date_regex = re.compile("^[1-9][0-9]{3}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])(.0)?$")
pronouns = {
"i": ["i", "me", "my", "myself", "mine"],
"we": ["we", "us", "our", "ourselves", "ours"],
"you": ["you", "your", "yours", "yourself", "yourselves"],
"he": ["he", "him", "his", "himself"],
"she": ["she", "her", "hers", "herself"],
"it": ["it", "its", "itself"],
"they": ["they", "them", "their", "theirs", "themselves"]
}
###############################################################################



def get_annotated_text(text):
    #cleaned_text = ""

    ann_res = nlp.annotate(text, properties=props)
    if ann_res is not None and len(text) < 100000:
        try:
            annotated_text = json.loads(ann_res)
        except:
            print("Corenlp server did not return expected result (Number of characters exceeding 100000? Or a timeout probably?).")
            annotated_text = {"sentences": []}
    else:
        annotated_text = {"sentences": []}
    return annotated_text


def tag_entities(annotated_text):
    """
    :param annotated_text: Annotated text from corenlp
    :param doc_date: Date of document
    :param pronoun_resolution: A dictionary of {"pronoun": "replacement"}
    :return: Lists of entities and events
    """
    entities, date_relations = [], {}

    for sentence in annotated_text["sentences"]:
        for entity_mention in sentence["entitymentions"]:
            if invalid_filter.match(entity_mention["text"]):
                continue
            elif replace_filter[0].match(entity_mention["text"]):
                entity_mention["ner"] = replace_filter[1]
            elif conditional_invalid[0].match(entity_mention["text"]) and entity_mention["ner"] == conditional_invalid[1]:
                continue
            entities.append({"type":entity_mention["ner"], "name":entity_mention["text"], "startindex":entity_mention["characterOffsetBegin"], "endindex":entity_mention["characterOffsetEnd"]+1})


    return entities


