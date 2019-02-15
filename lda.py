__author__ = 'timothypowell'

import pandas as pd
from gensim import corpora, models, utils, similarities, matutils
import re
from collections import defaultdict
from gensim.models.ldamodel import LdaModel
from gensim.models.hdpmodel import HdpModel
from nltk.corpus import stopwords

import logging
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from random import shuffle
import argparse
import math



logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
    level=logging.INFO)



xl = pd.ExcelFile('/Users/timothypowell/Downloads/partopar.xls')
df = xl.parse("Sheet1")


"""
join all celex document in one row, and run LDA on entire documents rather than paragraphs

df['key'] = (df['celex'] != df['celex'].shift(1)).astype(int).cumsum()
grouped = df.groupby(['key', 'celex'])['par_text'].apply(' '.join)
documents = [x for x in grouped]

"""


"""
create corpus
"""
documents = [x for x in df['par_text']]

"""
shuffle the data to prevent topic drift
"""
shuffle(documents)


"""
preprocessing
"""
punctuation = re.compile(ur'[\W0-9]', re.U)
texts = [[punctuation.sub("", token) for token in document.lower().split()] 
        for document in documents] 
texts = [[token for token in text if token]
      for text in texts]
#remove stopwords
stoplist =stopwords.words('english')
#create custom list of 'stopwords' for the corpus
stoplist2 = ['article', 'paragraph', 'case', 'ec', 'court', 'ecr', 'mr', 'articles', 'paragraphs'] # add member, union, state, treaty??
texts = [[token for token in text if token not in stoplist and token not in stoplist2]
         for text in texts]
frequency = defaultdict(int)

for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1 and len(token)>1]
      for text in texts]


"""
Maybe try stemming, but NLTK stemmer might cut inflections incorrectly.
"""



dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/topicmodelling.dict') # store the dictionary, for future reference
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/topicmodelling.mm', corpus) # store to disk, for later use


"""don't use tf-idf for Mallet wrapper because it needs counts not floats"""
tfidf = models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]

"""
if using mallet wrapper, cannot use tf-idf corpus
"""

mallet_path = '/Users/timothypowell/Downloads/mallet-2.0.7/bin/mallet'

def show_table(final_topics, num_topics):
    
    ncolumns = int(math.ceil(math.sqrt(num_topics)))
    freqs = []

    for t,line in enumerate(final_topics):
        scores = [float(x.split("*")[0]) for x in line.split(" + ")]
        words = [x.split("*")[1] for x in line.split(" + ")]
        topicwords = []
        for word, score in zip(words, scores):
            topicwords.append((word, score*1000))
        freqs.append(topicwords)
        #plt.subplot(ncolumns, ncolumns, t + 1)  # plot numbering starts with 1
        totalfonts = 0
        maxfont = 0
        for i, (word, score) in enumerate(topicwords):
            totalfonts += score
            if score >= maxfont:
                maxfont = score
        plt.ylim(-100, 300)  # stretch the y-axis to accommodate the words
        plt.xticks([])  # remove x-axis markings ('ticks')
        plt.yticks([]) # remove y-axis markings ('ticks')
        plt.title('Topic #{}'.format(t))

        previous_score  = 0
        for i, (word, score) in enumerate(topicwords):
            if previous_score ==0:
                previous_score = score
            plt.text(0.03, 270-(i*25)-1.5, '%s.%s -%s' %(i+1,word, score/1000), fontsize=score) 
            previous_score = score
        plt.show()

    #plt.tight_layout()
    plt.show()

if __name__=="__main__":

    # parse command line options
    parser = argparse.ArgumentParser(description="""Run LDA""")
    parser.add_argument("--num_topics", required=True)
    parser.add_argument("--show_table", action='store_true')
    args = parser.parse_args()


    integer = int(args.num_topics)
    lda = models.wrappers.LdaMallet(mallet_path,corpus=corpus, id2word=dictionary,num_topics=integer, optimize_interval=10)
    #lda = LdaModel(corpus=corpus, id2word=dictionary,num_topics=integer)
    printed = lda.print_topics(num_topics=-1, num_words =15)
    if args.show_table:
        show_table(printed, integer)
