import os
import string
from langconv import *
import pandas as pd
import re
import glob
SaveFile_Path =  r'D:\youtube_data\7.城寨'       #拼接后要保存的文件路径
csv_list=[i for i in glob.glob('*.{}'.format('csv'))]   #加载当前文件里所有后缀为csv的文件。

def simple2tradition(line):
    # 将简体名字转换成繁体
    line = Converter('zh-hant').convert(line)
    return line

def remove_username(x,userlist):
    flag=False
    for i in userlist:
        if str(i) in x[:26] and x.index(str(i))==0:
            flag = True
            new_comment = x.replace(str(i),'Username',1) #替换1次
    if flag == True:
        return new_comment
    else:
        return x

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
    if num_eng >= 35:
        return 'english comment'
    elif (num_eng/comment_length) >= 0.85:
        if comment_length>=15:
            return 'english comment'
        else:
            return x
    else:
        return x



def comment_preprocessed(csv_list,SaveFile_Path):
    pattern2 = re.compile('<a.*</a>')
    pattern1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    for csv_file in csv_list:
        data = pd.read_csv(csv_file)
        data.dropna(subset=['comment'], inplace=True)  # 清除空的评论
        data['comment'] = data['comment'].astype(str) # 转换成字符串格式
        # 去除评论字符串两边的空格
        data['comment'] = data['comment'].str.strip()
        # 简体转繁体
        data['comment'] = data['comment'].apply(lambda x: simple2tradition(x))
        # 去除用户名改成Username
        userlist = data['author']
        data['comment'] = data['comment'].apply(lambda x: remove_username(x, userlist))  # 去除用户名
        # 去除URL
        data['comment'] = data['comment'].apply(lambda x: re.sub(pattern2, 'URL', x))  # 替换掉 网络地址 成 URL
        data['comment'] = data['comment'].apply(lambda x: re.sub(pattern1, 'URL', x))  # 替换掉 网络地址 成 URL
        # 去除英文
        data['comment'] = data['comment'].apply(lambda x: remove_eng(x))
        #将英文单词小写
        data['comment'] = data['comment'].str.lower()
        #删除其它列，只保留comment列
        data = data['comment']

        print(csv_file)
        if os.path.exists(SaveFile_Path):
            data.to_csv(SaveFile_Path + '\\' + 'modified_'+csv_file, encoding="utf_8_sig", index=False, header=False)
        else:
            os.makedirs(SaveFile_Path)
            data.to_csv(SaveFile_Path + '\\' +  'modified_'+csv_file, encoding="utf_8_sig", index=False, header=False)

        # try:
        #     os.mkdir("C:\\test\\aaa")
        # except Exception as e:
        #     print(e)
        # try:
        #     os.makedirs("C:\\tests\\bbb")


comment_preprocessed(csv_list,SaveFile_Path)
