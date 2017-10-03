from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from pprint import pprint
from pymongo import MongoClient
import operator
import math
import os
import file


folder_path = os.path.dirname(os.path.realpath(__file__)) + '/pos_terms'
result = {}
raw_datas = []
datas = []
for f in os.listdir(folder_path):
    path = os.path.join(folder_path, f)
    if os.path.isfile(path) and '.json' in path:
        raw_datas += file.read_file(path)
for raw_data in raw_datas:
    concat = []
    concat = ' '.join(raw_data)
    datas.append(concat)

corpus = []
for data in raw_datas:
    corpus.append(' '.join(data))

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(corpus)
word = vectorizer.get_feature_names()
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(x)
word = vectorizer.get_feature_names()
weight = tfidf.toarray()
tfidf_result = {}
for i in range(len(weight)):
    temp_result = {}
    for j in range(len(word)):
        if weight[i][j]:
            temp_result[word[j]] = weight[i][j]
    print('======================')
    pprint(list(reversed(sorted(temp_result.items(), key=operator.itemgetter(1)))))
    if i >= 5:
        break
