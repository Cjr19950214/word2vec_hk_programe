from gensim.models import word2vec
import logging  #用来修改 显示日志用的
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

load_model = word2vec.Word2Vec.load('wiki_corpus.model')

len(load_model.wv.vocab)

#test
load_model.wv.most_similar("厭惡") 

load_model.wv.most_similar("民主", topn=10)  # 10个最相关的

data = pd.read_csv(r'D:\total_youtube_cut_word_combined\combined.csv',header=None)
data[0] = data[0].apply(lambda x: eval(x))

load_model.build_vocab(data[0],update=True)

load_model.train(data[0],total_examples=load_model.corpus_count,epochs=load_model.epochs)

len(load_model.wv.vocab)

load_model.wv.most_similar("高興", topn=10)  # 10个最相关的

load_model.save("wiki&comment_corpus1.model")
