#coding: utf-8
import os
from flask import Flask, request, render_template
import pymorphy2
import preprocess
import csv

with open('ind_text.csv', mode='r') as infile:
    reader = csv.reader(infile, delimiter='\t')
    ind_text = {rows[0]:rows[1] for rows in reader}

with open('word_ind.csv', mode='r') as infile:
    reader = csv.reader(infile, delimiter='\t')
    word_ind = {rows[0]:rows[1] for rows in reader}

morph = pymorphy2.MorphAnalyzer()
punct = '”“".,«»\\/*!:;—()\'-%`.?―[]'

def href_make(t):
    if t in word_ind:
        if '\n' in t:
            t = t.replace('\n', '')
            return '<a href="/submit/"' + word_ind[t] + ' target="_blank">' + t + '</a><br>'
        else:
            return '<a href="/submit/"' + word_ind[t] + ' target="_blank">' + t + '</a><br>'
    else:
        return t.replace('\n', '<br>')
    
app = Flask(__name__)
@app.route('/index')
def index():
    return render_template('start.html')

@app.route('/upload')
def form():
    return render_template('text.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        if len(request.form['novel']) > 0:
            arr = []
            inp = request.values.get('novel').split()
            #inp = request.form['novel'].split()
            fr_d = preprocess.freq_dic()
            for token in inp:
                word = token.strip().strip(punct).replace(u'ё', u'е')
                word = token.lstrip(punct).strip(punct).strip(punct).lower()
                infoword = morph.parse(word)[0]
                lemma = infoword.normal_form.replace(u'ё', u'е')
                pos = preprocess.pos_converter(infoword.tag.POS)
                if pos != 0 and not token[0].isupper():
                    if (lemma, pos) in fr_d:
                        if pos == 's' and fr_d[(lemma, pos)] <= 2.3:
                            if preprocess.noun_filter(lemma):
                                to_arr = href_make(token)
                    else:
                        if pos == 's':
                            if preprocess.noun_filter(lemma):
                                to_arr = href_make(token)
                        if pos == 'a' and len(lemma) > 4:
                            if preprocess.adj_filter(lemma):
                                to_arr = href_make(token)
                else:
                    to_arr = token.replace('\n', '<br>')
                arr.append(to_arr)
            text = ' '.join(arr)
            return render_template('result.html', text=text)
            
@app.route('/submit/<index>')
def definition():
    defin = ind_text[index]
    return render_template('definition.html', defin=defin)           

app.run(debug=True)
