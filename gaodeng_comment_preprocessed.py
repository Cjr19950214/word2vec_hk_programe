import os
import string
from langconv import *
import pandas as pd
import re
import glob
import numpy as np
SaveFile_Path =  r'D:\gaodeng_data'       #拼接后要保存的文件路径
csv_list=[i for i in glob.glob('*.{}'.format('csv'))]   #加载当前文件里所有后缀为csv的文件。

def simple2tradition(line):
    # 将简体名字转换成繁体
    line = Converter('zh-hant').convert(line)
    return line


def remove_eng(x):
    intCount = 0  #用来记录列表中的int元素个数
    engCount = 0 #记录str元素个数
    spaceCount = 0
    comment_length = len(x)  #整个comment长度
    # 使用for循环遍历字符串，每次循环判断当前获取的元素的类型，并给对应计数器计数
    for i in x:
        if i.isdigit(): #判断i是不是int
            intCount += 1
        elif i in string.ascii_letters: #判断i是不是英文字符
            engCount += 1
        elif i.isspace():
            spaceCount +=1
    num_eng = intCount + engCount + spaceCount
    if (num_eng/comment_length) >= 0.85:
        if comment_length>=15:
            return 'English comment'
        else:
            return x
    else:
        return x

def delete_space(x):
    spaceCount=0
    comment_length =len(x)
    for i in x:
        if i.isspace():
            spaceCount+=1
    if comment_length == spaceCount:
        return np.NaN
    else:
        return x


def comment_preprocessed(csv_list,SaveFile_Path):
    pattern2 = re.compile('<a.*</a>')
    pattern1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    for csv_file in csv_list:
        data = pd.read_csv(csv_file,header=None)
        # 1.去除评论字符串两边的空格
        data[2] = data[2].str.strip()
        # 2.去除掉论坛独有的重复回复字符串
        for index_x, x in enumerate(data[2]):
            for index_y, y in enumerate(data[2][index_x + 1:]):
                if str(x) in str(y):
                    data.iloc[index_y + index_x + 1, 2] = str(data.iloc[index_y + index_x + 1, 2]).replace(str(x), '')
        # 3.再次去除评论两边的空格
        data[2] = data[2].str.strip()
        # 4.简体转繁体,需要先把评论转化为str类型
        data[2] = data[2].astype(str)
        data[2] = data[2].apply(lambda x: simple2tradition(x))
        # 5.去除URL
        data[2] = data[2].apply(lambda x: re.sub(pattern2, 'URL', x))  # 替换掉 网络地址 成 URL
        data[2] = data[2].apply(lambda x: re.sub(pattern1, 'URL', x))  # 替换掉 网络地址 成 URL
        # 6.将空格转换成NaN
        data[2] = data[2].apply(lambda x: delete_space(x))  # 将只有空格的样本换成NaN
        data.dropna(subset=[2], inplace=True)
        # 7.去除英文
        data[2] = data[2].apply(lambda x: remove_eng(x))
        # 8.将英文单词小写
        data[2] = data[2].str.lower()

        # 9.删除其它列，只保留comment列
        data.dropna(subset=[2], inplace=True)
        data = data[2]


        print(csv_file)
        if os.path.exists(SaveFile_Path):
            data.to_csv(SaveFile_Path + '\\' + 'modified_'+csv_file, encoding="utf_8_sig", index=False, header=False)
        else:
            os.makedirs(SaveFile_Path)
            data.to_csv(SaveFile_Path + '\\' +'modified_'+ csv_file, encoding="utf_8_sig", index=False, header=False)


comment_preprocessed(csv_list,SaveFile_Path)
