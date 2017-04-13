#coding:utf-8
import pymorphy2
import codecs


def freq_dic():
    d = {}
    k = codecs.open('freqrnc2011.csv', 'r', 'utf-8')
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
    excl = set([u'чь', u'ие', u'ец', u'ье', u'ок', u'ек', u'ий', u'ый', u'ой', u'ач', u'ша'])
    excl1 = set([u'очка', u'ство', u'ость', u'ечка', u'ушка', u'тель', u'куда'])
    if not noun[0].isupper() and noun[-2:] not in excl and noun[-3:] != u'ица' and noun[-4:] not in excl1:
        return True
    else:
        return False

#функция проверяет, подходит ли прилагательное по критериям
def adj_filter(adj):
    end = (u'либо', u'нибудь', u'-то', u'енный', u'еный', u'ейший', u'айший', u'анький', u'енький')
    beg = (u'не', u'ни')
    stop = [u'такой', u'который', u'самый', u'каждый', u'таков', u'другой',
            u'всякий', u'каковой', u'каков', u'остальной', u'какой', u'многий']
    if not adj.endswith(end):
        if not adj.startswith(beg) and adj not in stop:
            return True
        else:
            return False


