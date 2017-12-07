#coding:utf-8
import pymorphy2

st = open('/home/lpolyanskaya/comment_web_app/stoplist.txt', 'r', encoding='utf-8').readlines()

def freq_dic():
    d = {}
    k = open('/home/lpolyanskaya/comment_web_app/freqrnc2011.csv', 'r', encoding='utf-8')
    for line in k:
        line = line.strip()
        line = line.split('\t')
        key = (line[0], line[1])
        if key not in d:
            d[key] = float(line[2])
    return d

def pos_converter(tag):
    converter = {'NOUN': 's',
                 'ADJF': 'a',
                 'ADJS': 'a',
                 'COMP': 'a',
                 'ADVB': 'adv'}
    if tag in converter:
        return converter[tag]
    else:
        return 0

#функция проверяет, подходит ли существительное по критериям
def noun_filter(noun):
    excl = set(['чь', 'ие', 'ец', 'ье', 'ок', 'ек', 'ий', 'ый', 'ой', 'ач', 'ша'])
    excl1 = set(['очка', 'ство', 'ость', 'ечка', 'ушка', 'тель', 'куда'])
    if not noun[0].isupper() and noun[-2:] not in excl and noun[-3:] != 'ица' and noun[-4:] not in excl1:
        return True
    else:
        return False

#функция проверяет, подходит ли прилагательное по критериям
def adj_filter(adj):
    end = ('либо', 'нибудь', '-то', 'енный', 'еный', 'ейший', 'айший', 'анький', 'енький')
    beg = ('не', 'ни')
    stop = ['такой', 'который', 'самый', 'каждый', 'таков', 'другой',
            'всякий', 'каковой', 'каков', 'остальной', 'какой', 'многий', 'сто']
    if not adj.endswith(end):
        if not adj.startswith(beg) and adj not in stop and adj not in st:
            return True
        else:
            return False


