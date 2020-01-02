import os
import string
import pandas as pd
import re
import glob
import jieba

jieba.load_userdict(r'C:\Users\81284\OneDrive\项目！！\1.神经网络情感分析\分词字典处理\merge_wordlist.txt') #添加切词字典
SaveFile_Path =  r'D:\total_cut_word_combined'       #拼接后要保存的文件路径
SaveFile_Name = r'veronbenny_cut.csv'                #拼接后所要保存的文件名
csv_list=[i for i in glob.glob('*.{}'.format('csv'))]   #加载当前文件里所有后缀为csv的文件。


for csv_file in csv_list:
    data = pd.read_csv(csv_file,header=None)
    data = data[0].apply(jieba.lcut)
    data.to_csv(SaveFile_Path + '\\' + SaveFile_Name, encoding="utf_8_sig", index=False, header=False, mode='a+')
    print(csv_file)
