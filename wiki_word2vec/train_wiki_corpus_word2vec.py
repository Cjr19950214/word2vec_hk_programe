from gensim.models import word2vec
import logging  #用来修改 显示日志用的
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

sentences = word2vec.LineSentence("wiki.zh.seg.txt")
model = word2vec.Word2Vec(sentences, size=300, window=6, min_count=8, workers=4)  #注意這裏window我選擇了6

model.wv.most_similar("xxx")

model.save("wiki_corpus.model")
