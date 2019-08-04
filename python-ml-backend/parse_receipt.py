import pprint
from googlesearch import search
import requests
import io
from google.cloud import vision

from corenlp_annotator import get_annotated_text, tag_entities
from address import find_addresses
from config import POST_URL
from model.table_model import get_table_data

pp = pprint.PrettyPrinter(indent=4)

blacklist = ["nos", "no", "pc", "pcs"]
header_terms = {'qty': 'item_quantity', 'quantity': 'item_quantity', 'price': 'item_price', 'total': 'item_total', 'amount': 'item_total', 'item': 'item_name', 'items': 'item_name'}


def get_date_time(text):
    date, time = None, None
    annotated_text = get_annotated_text(text)
    entities = tag_entities(annotated_text)

    for ent in entities:
        if ent['type'].endswith("DATE"):
            date = ent['name']
        elif ent['type'] == 'TIME':
            time = ent['name']
    return date, time


def isAmount(term):
    return term.replace(".", "", 1).replace(",", "", 1).isdigit()

def get_headers(line):
    headers = []
    terms = [t for t in line.split() if t.lower() != "name"]
    for term in terms:
        term = term.lower()
        if term in header_terms:
            headers.append(header_terms[term])

    return headers

def extract_purchase_info(lines, headers):
    orig_headers = headers.copy()
    purchases = []
    for terms in lines:
        numbers, item_name = [], None
        for t in range(len(terms)-1, -1, -1):
            if terms[t] not in blacklist:
                if isAmount(terms[t]):
                    numbers.append(terms[t].replace(",", "."))
                else:
                    item_name = " ".join(terms[:t+1]).strip().lower()
                    break
        if len(numbers) >= 2 and item_name is not None:
            if len(orig_headers) < 3:
                if len(numbers) == 2: headers = ["item_quantity", "item_total"]
                else: headers = ["item_quantity", "item_price", "item_total"]
            purchase, item_total = {}, None
            for h, n in zip(headers[::-1], numbers):
                if h == "item_total": item_total = float(n)
                else: purchase[h] = float(n)
            purchase["item_name"] = item_name
            purchase['item_category'] = "grocery"
            if 'item_price' not in purchase and 'item_quantity' in purchase and purchase['item_quantity'] > 0.0 and item_total not in [0.0, None]: purchase['item_price'] = item_total/purchase['item_quantity']
            if 'item_price' not in purchase: purchase['item_price'] = 0
            is_food, total = 0, 0
            for url in search(item_name, stop=10):
                if "www.youtube." in url: continue
                total += 1
                if "recipe" in url or "restaurant" in url or "swiggy" in url or "zomato" in url:
                    is_food += 1
            if total > 0:
                if is_food/total > 0.45:
                    purchase['item_category'] = "food"
                else: purchase['item_category'] = "others"

            purchases.append(purchase)

    return purchases


def parse_items(file_path):
    purchase_results = []
    for table in get_table_data(file_path):
        purchase_results.extend(extract_purchase_info(table, []))
    return purchase_results


def parse_items2(text):
    lines = text.split("\n")
    for l in range(len(lines)):
        if lines[l].strip().lower().startswith("item"):
            if l + 1 < len(lines):
                headers = get_headers(lines[l])
                return extract_purchase_info(lines[l + 1:], headers)

    return []

def get_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if len(texts): return texts[0].description
    else: return ""


def extract_info(file_path):
    text = get_text(file_path)
    text = text.replace("—", "-")

    purchases = parse_items(file_path)
    if not len(purchases):
        purchases = parse_items2(text)
    address = find_addresses(text)
    #date, time = get_date_time(text)

    address["items"] = purchases

    print("SAVING DATA:", address)

    resp = requests.post(POST_URL, json=address)
    if resp.status_code != 200:
        print("Something went wrong while saving the data.")
        print(resp.json())

    return resp.status_code


