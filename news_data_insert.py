from pymongo import MongoClient
from pprint import pprint
import json
import file

NEWS_DATA_PATH = '/Users/pzn666/Documents/WorkSpace/FocalDatas/news_100k.json'
news_datas = []
with open(NEWS_DATA_PATH, 'r', encoding='utf-8', errors='ignore') as f:
    raw_data = f.readlines()
    for data in raw_data:
        obj = json.loads(data)
        obj.pop('_id')
        if obj['keyword']:
            new_obj = {
                'keyword': {}
            }
            for key in obj['keyword']:
                new_key = key[0:1]
                new_obj['keyword'][new_key] = obj['keyword'][key]
            obj['keyword'] = new_obj
        news_datas.append(obj)
client = MongoClient('localhost', 27017)
result = client['focal']['news_data'].insert_many(news_datas)
print(result)
