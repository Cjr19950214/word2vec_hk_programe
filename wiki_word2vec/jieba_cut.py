#文章分词
import jieba
import jieba.analyse
import codecs

jieba.load_userdict(r'C:\Users\81284\OneDrive\项目！！\1.神经网络情感分析\分词字典处理\merge_wordlist.txt') #添加切词字典
def cut_words(sentence):
   #print sentence
    return " ".join(jieba.cut(sentence)).encode('utf-8')
f=codecs.open('wiki_zh.txt','r',encoding="utf8")
target = codecs.open("wiki.zh.seg.txt", 'w',encoding="utf8")
print ('open files')
line_num=1
line = f.readline()
while line:
    print('---- processing', line_num, 'article----------------')
    line_seg = " ".join(jieba.cut(line))
    target.writelines(line_seg)
    line_num = line_num + 1
    line = f.readline()
f.close()
target.close()
exit()
while line:
    curr = []
    for oneline in line:
        #print(oneline)
        curr.append(oneline)
    after_cut = map(cut_words, curr)
    target.writelines(after_cut)
    print ('saved',line_num,'articles')
    exit()
    line = f.readline1()
f.close()
target.close()
