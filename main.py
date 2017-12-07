#coding: utf-8
from flask import Flask, request, render_template
import pymorphy2
import preprocess
import csv

 
with open('/home/lpolyanskaya/comment_web_app/new_ind_text.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='\t')
    ind_text = {rows[0]:rows[1] for rows in reader}


with open('/home/lpolyanskaya/comment_web_app/word_ind.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='\t')
    word_ind = {rows[1]:rows[0] for rows in reader}


with open('/home/lpolyanskaya/comment_web_app/ind_tool.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='\t')
    ind_tool = {rows[0]:rows[1] for rows in reader}

morph = pymorphy2.MorphAnalyzer()
punct = '”“".,«»\\/*!:;—()\'-%`.?―[]'


def href_make(l, t):
    if l in word_ind:
        if word_ind[l] in ind_tool:
            if '\n' in t:
                t = t.replace('\n', '')
                return '<a href="/drozhki/submit/' + word_ind[l] + '"' + ' target="_blank" data-toggle="tooltip" title="' + ind_tool[word_ind[l]] + '">' + t + '</a><br>'
            else:
                return '<a href="/drozhki/submit/' + word_ind[l] + '"' + ' target="_blank" data-toggle="tooltip" title="' + ind_tool[word_ind[l]] + '">' + t + '</a>'
        else:
            if '\n' in t:
                t = t.replace('\n', '')
                return '<a href="/drozhki/submit/' + word_ind[l] + '"' + ' target="_blank">' + t + '</a><br>'
            else:
                return '<a href="/drozhki/submit/' + word_ind[l] + '"' + ' target="_blank">' + t + '</a>'            
    else:
        return t.replace('\n', '<br>')

   
app = Flask(__name__)
@app.route('/drozhki')
def index():
    return render_template('start.html')

@app.route('/drozhki/upload')
def form():
    return render_template('text.html')

@app.route('/drozhki/english')
def english():
    return render_template('english.html')

@app.route('/drozhki/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        if len(request.form['novel']) > 0:
            arr = []
            inp = request.form['novel'].replace('\n', ' <br>').split()
            fr_d = preprocess.freq_dic()
            for token in inp:
                word = token.strip().strip(punct).replace('ё', 'е')
                word = token.lstrip(punct).strip(punct).strip(punct).lower()
                infoword = morph.parse(word)[0]
                lemma = infoword.normal_form.replace('ё', 'е')
                pos = preprocess.pos_converter(infoword.tag.POS)
                to_arr = token.replace('\n', '<br>')
                if pos != 0:
                    if (lemma, pos) in fr_d:
                        if pos == 's' and fr_d[(lemma, pos)] <= 2.3 and not token[0].isupper():
                            if preprocess.noun_filter(lemma):
                                to_arr = href_make(lemma, token)
                    else:
                        if pos == 's' and not token[0].isupper():
                            if preprocess.noun_filter(lemma):
                                to_arr = href_make(lemma, token)
                        if pos == 'a' and len(lemma) > 4:
                            if preprocess.adj_filter(lemma):
                                to_arr = href_make(lemma, token)
                arr.append(to_arr)
            text = ' '.join(arr)
            return render_template('result.html', text=text)
        else:
            return render_template('text.html')      
            
@app.route('/drozhki/submit/<index>')
def definition(index):
    defin = ind_text[index]
    return render_template('definition.html', defin=defin)


if __name__ == '__main__': 
    app.run(debug=True)
