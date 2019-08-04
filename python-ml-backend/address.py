import re
from stanfordcorenlp import StanfordCoreNLP

from config import CORENLP_SERVER_URL

nlp = StanfordCoreNLP(CORENLP_SERVER_URL, port=9000)
props = {'annotators': 'tokenize,ssplit,pos,ner', 'outputFormat': 'json'}

ORG_SUFFIX_PAT = re.compile("llc|ltd|inc", re.IGNORECASE)

invalid_filter = re.compile("^[-_|]+$")
replace_filter = (re.compile("^#[\s0-9]*$"), "NUMBER")

address_threshold = {"STATE_OR_PROVINCE": 1, "LOCATION": 1, "CITY": 1}
address_desirable = {"NUMBER": 0.5, "ORGANIZATION": 1, "COUNTRY": 1}
postal_code_regex = re.compile(r"[^0-9][0-9]{6}[^0-9]")  # ("[0-9]{5}(-[0-9]{4})?")
ph_regex = re.compile(r"[0-9]+[—-][0-9]+")
number_regex = re.compile(r"[0-9]+")

not_address = tuple(["tin ", "cash", "invoice", "date", "sale", "serial", "takeaway"])


def classify_information_type(text):
    """
        :param text: The block text to be identified
        :return: dictionary indicating scores for different classes for this block of text {class: score}
    """
    entities = tag_entities(text)
    address_score = address(text, entities)

    return {"address": address_score}


def clean_entities(entities):
    cleaned_entities = []

    for ent in entities:
        if invalid_filter.search(ent[0]):
            continue
        elif replace_filter[0].search(ent[0]):
            cleaned_entities.append([ent[0], replace_filter[1]])
        elif ent[1] != 'O':
            cleaned_entities.append([ent[0], ent[1]])

    return cleaned_entities


def tag_entities(text):
    entity_mentions = nlp.ner(text)
    entities = clean_entities(entity_mentions)

    return entities


def get_clean_text_lines(text):
    lines = text.split("\n")
    l = 0
    for l in range(len(lines)):
        if lines[l].strip() != "":
            lines[l] = lines[l] + ","
            break

    lines = [line for line in lines[l:] if not line.strip().lower().startswith(not_address)]
    return lines


def find_addresses(ocr_text):
    cur_score, first = 0, True
    blocks = ocr_text.split("\n\n")
    if len(blocks) < 2:
        blocks = ["\n".join(ocr_text.split("\n")[:7])]
    address_json = {}
    for line in blocks:
        if line.strip():

            text = ORG_SUFFIX_PAT.sub(lambda m: m.group(0).capitalize(), line)
            # words = ner.nlp.word_tokenize(text)
            # print(words)
            # n_words = len(words)
            text_lines = get_clean_text_lines(text)
            proper_text = "\n".join(text_lines)
            text = "\n".join([x + " ." for x in text_lines])
            # temp = extract_information(0, 1, 1, [line])
            address_score = classify_information_type(text).get("address", 0)
            if address_score > cur_score or first:
                first = False
                zip_code = None
                numbers = number_regex.findall(line)
                phones = [ph for ph in ph_regex.findall(line) if len(ph) in [11, 12]]
                for n in numbers:
                    if len(n) == 6:
                        zip_code = n
                    elif len(n) == 10:
                        phones.append(n)
                    address_json = {"store_name": text.split("\n")[0][:-3].strip().lower(),"store_address": proper_text.strip().lower(), "store_info": {"phones": phones},
                                     "store_pincode": zip_code}

    return address_json


def address(text, entities):
    if len(entities) <= 1: return 0
    # print(entities)
    # if n_tokens >= 2*len(entities): return 0
    score, perfect_score = 0, 6
    entity_types = [ent[1] for ent in entities]
    x1 = [address_threshold[ent] for ent in address_threshold if ent in entity_types]
    score = sum(x1)

    if score > 0:
        x2 = [address_desirable[ent] for ent in address_desirable if ent in entity_types]
        score += sum(x2)
        ner_ratio = float(score / len(entity_types))

        if postal_code_regex.search(text):
            score += 0.5

        score = score / perfect_score + ner_ratio

    return score
