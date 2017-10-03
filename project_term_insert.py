from pymongo import MongoClient
from pprint import pprint
import json
import file

NEWS_DATA_PATH = '/Users/pzn666/Documents/WorkSpace/FocalDatas/project_terms_20171002.json'
project_terms = []
with open(NEWS_DATA_PATH, 'r', encoding='utf-8', errors='ignore') as f:
    raw_data = f.readlines()
    for data in raw_data:
        test = False
        obj = json.loads(data)
        obj.pop('_id')
        for key in obj:
            if '.' in key:
                new_key = key.replace('.', '_')
                obj[new_key] = obj[key]
                obj.pop(key)
        project_terms.append(obj)
client = MongoClient('localhost', 27017)
result = client['focal']['project_terms'].insert_many(project_terms)
print(result)