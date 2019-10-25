from bs4 import BeautifulSoup
from nltk import tokenize
from nltk.corpus import stopwords
from collections import Counter
from math import sqrt


def parse(html):
    soap = BeautifulSoup(html, 'html.parser')
    text_from_html = soap.get_text()
    return get_tokens(text_from_html)


def get_tokens(text):
    tokenizer = tokenize.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    stw = set(stopwords.words('spanish'))
    tokens_no_sw = [x.lower() for x in tokens if x.lower() not in stw]
    tokens_no_sw = Counter(tokens_no_sw)
    norma = sum([tokens_no_sw[i] * tokens_no_sw[i] for i in tokens_no_sw])
    norma = sqrt(norma)
    for i in tokens_no_sw:
        tokens_no_sw[i] = tokens_no_sw[i] / norma
    return tokens_no_sw
