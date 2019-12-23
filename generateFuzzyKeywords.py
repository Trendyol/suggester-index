import json
import re
import os

import pandas as pd
from elasticsearch import Elasticsearch

es = Elasticsearch([os.getenv('SOURCE_ES_URL')])


def get_product_names_from_elastic():
    print("Getting data from elasticsearch index...")
    content_names = []
    res2 = es.search(index=os.getenv('SOURCE_INDEX'))
    total_count = int(res2["hits"]["total"])

    for i in range(0, int(total_count / 1000)):
        res = es.search(
            index=os.getenv('SOURCE_INDEX'),
            body={
                "_source": "name",
                "from": i * 1000,
                "size": 1000,
                "query": {
                    "match_all": {}
                }
            })
        data = res['hits']['hits']
        for x in range(0, len(data)):
            content_name = data[x]['_source'][os.getenv('SOURCE_ATTRIBUTE')]
            split_content_names = content_name.split(" ")
            for j in range(0, len(split_content_names)):
                delete_special_characters(split_content_names)
                if not has_numbers(split_content_names[j]):
                    if len(split_content_names[j]) > 1:
                        content_names.append(split_content_names[j].lower().strip())
    print("Done")
    return content_names


def get_names_from_excel():
    print("Getting data from dictionary file...")
    dictionary = []
    sheets = ["A", "B", "C", "Ç", "D", "E", "F", "G", "H", "I", "İ", "J", "K", "L", "M", "N", "O", "Ö", "P", "R", "S",
              "Ş", "T", "U", "Ü", "V", "Y", "Z"]
    file = 'dictionary.xls'
    xl = pd.ExcelFile(file)

    for i in range(0, len(sheets)):
        df1 = xl.parse(sheets[i])
        sheets_length = len(df1[sheets[i]])
        for j in range(0, sheets_length):
            abc = sheets[i]
            split_name_with_comma = df1[abc][j].split(',')
            split_name_with_brackets = split_name_with_comma[0].split('(')
            delete_special_characters(split_name_with_brackets)
            if not has_numbers(split_name_with_brackets[0]):
                if len(split_name_with_brackets[0]) > 1:
                    dictionary.append(split_name_with_brackets[0].lower().strip())
    print("Done")
    return dictionary


def delete_special_characters(array):
    for i in range(0, len(array)):
        array[i] = re.sub("[-_!.|)(+%&/=?*:,>’'…\"]", '', array[i])


def has_numbers(input_string):
    return bool(re.search(r'\d', input_string))


def make_json_file():
    all_names = get_names_from_excel() + get_product_names_from_elastic()
    print("Writing data's to json file...")
    removed_duplicates = list(set(all_names))
    b = [{'keyword': removed_duplicates[i]} for i in range(len(removed_duplicates))]
    with open('keywords.json', 'w') as json_file:
        json.dump(b, json_file, ensure_ascii=False)
    print("Done")


def post_fuzzy_index():
    print("Reading data json and posting target index...")
    es2 = Elasticsearch([os.getenv('TARGET_ES_URL')])

    with open('keywords.json') as json_file:
        data = json.load(json_file)

    for i in range(len(data)):
        es2.index(index=os.getenv('TARGET_INDEX'), doc_type=os.getenv('DOC_TYPE'), body=data[i])
    print("Done")


make_json_file()
post_fuzzy_index()
