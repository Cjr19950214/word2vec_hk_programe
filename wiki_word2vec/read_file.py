import codecs

f = codecs.open('wiki_zh.txt', 'r', encoding="utf8")  # 这里打开哪个文件就改为哪个文件的文件名
line = f.readline()
print(line)
