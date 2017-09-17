from pymongo import MongoClient
from pymongo import errors
from pymongo.collection import Collection
import time
import os
import file
import multiprocessing as mp
import pprint
import jieba
import json

FOCAL_AUTH = {
    'account': 'pzn666',
    'password': 'xul4jp6cl4666'
}

EXCLUDE_LIST = ['（', '〔', '［', '｛', '《', '【', '〖', '〈', '(', '[' '{', '<',
                '）', '〕', '］', '｝', '》', '】', '〗', '〉', ')', ']', '}', '>',
                '“', '‘', '『', '』', '。', '？', '?', '！', '!', '，', ',', '', '；',
                ';', '、', '：', ':', '……', '…', '——', '—', '－－', '－', '-', ' ',
                '「', '」', '／', '/']


class Tokenizer:
    def __init__(self, host='localhost', db='focal', collection='news_data'):
        self.host = host
        self.db = db
        self.collection = collection

    def tokenize(self):
        start_time = time.time()
        limit = 10000
        chunk_num = 10
        docs = list(self.__read_docs(limit=limit))
        doc_chunks = list(self.__split_chunks_(limit // chunk_num, docs))
        pool = mp.Pool(mp.cpu_count())
        for i, chunk in enumerate(doc_chunks):
            raw_list = pool.map(self.jieba_tokenize, chunk)
            tokenized_list = self.__migrate_raw_data(raw_list)
            file_name = 'terms_' + str(i)
            self.__write_json(tokenized_list, file_name)
        print("--- %s seconds ---" % (time.time() - start_time))

    def __migrate_raw_data(slef, data_list):
        result = []
        for data in data_list:
            result += data
        return result

    def __read_docs(self, limit=0):
        client = MongoClient(self.host, 27017)
        collection = client[self.db][self.collection]
        docs = []
        if limit == 0:
            docs = collection.find({}, {'context': 1, '_id': 0})
        else:
            docs = collection.find({}, {'context': 1, '_id': 0}).limit(limit)
        return docs

    def __write_json(self, content, file_name):
        file_name = '/terms/' + file_name + '.json'
        save_path = os.path.dirname(os.path.realpath(__file__)) + file_name
        file.write_file(save_path, content, as_json=True)

    def __split_chunks_(slef, n, input_list):
        for i in range(0, len(input_list), n):
            yield input_list[i:i + n]

    def jieba_tokenize(self, doc):
        excluded_seg = []
        seg_list = list(jieba.cut(doc['context']))
        for seg in seg_list:
            if seg not in EXCLUDE_LIST:
                excluded_seg.append(seg)
        return excluded_seg


tokenizer = Tokenizer()
tokenizer.tokenize()
