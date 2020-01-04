from gensim.models import word2vec
import logging  #用来修改 显示日志用的
import pandas as pd

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)  #运行日志

load_model = word2vec.Word2Vec.load('wiki_corpus.model')   # 加载之前训练过的word2vec模型

len(load_model.wv.vocab)  # 看下原先的word2vec向量有多少词

#test
load_model.wv.most_similar("厭惡") 

load_model.wv.most_similar("民主", topn=10)  # 测试10个最相关的

data = pd.read_csv(r'D:\total_youtube_cut_word_combined\combined.csv',header=None) #此处读取新的要更新的 文本文件（csv格式）
data[0] = data[0].apply(lambda x: eval(x))  #将'['str1','str2'...]' 变为 list列表:['str1','str2'...]    消除引号

load_model.build_vocab(data[0],update=True)    #将新的文本词更新一遍

load_model.train(data[0],total_examples=load_model.corpus_count,epochs=load_model.epochs)  #开始训练，加入新的词向量

len(load_model.wv.vocab) 

load_model.wv.most_similar("高興", topn=10)  # 10个最相关的

load_model.save("wiki&comment_corpus1.model")   #导出新的word2vec模型
