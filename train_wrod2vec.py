from gensim.models import word2vec
import logging  #用来修改 显示日志用的
import pandas as pd
import glob

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

csv_list=[i for i in glob.glob('*.{}'.format('csv'))]  #获取当前文件下的所有csv文件

class MySentences(object):
    """生成迭代器"""
    def __init__(self, csv_list):
        self.csv_list = csv_list
 
    def __iter__(self):
        for csv_file in csv_list:
            data = pd.read_csv(csv_file,header=None)
            for i in data[0]:
                yield eval(i)     #要将str转换成list   i = '['str1,','str2'...]'
            
sentences = MySentences(r'D:\total_youtube_cut_word_combined')

n_dim=300  #设置为300维
w2vmodel = word2vec.Word2Vec(sentences,size=n_dim,min_count=5)

w2vmodel.wv.most_similar("xxx")

w2vmodel.save("word2vec.model")
