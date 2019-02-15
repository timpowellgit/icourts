'''

Script for training word2vec models on defined snapshot periods, or the entire corpus.
No retraining or annotation of the corpus
Model is saved and similarites can be loaded with test_similarities.py

'''

import gensim 
import logging
import os
import MySQLdb
import argparse
import getpass
import re
import sentences_iterator as si
from itertools import chain

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




def get_model(yearmin = 1950, yearmax= 2016, bigrams = False, dimensions = 300):


    #run function from sentences iterator to load sentences within a given period snapshot
    sentences = si.MySentences('X:\\ECJ\\txt', yearmin = yearmin, yearmax = yearmax ) # a memory-friendly iterator

    if bigrams:
        #if bigrams set to True, use gensim's phrases method to find bigram phrases, and train Wordd2vec on bigrams and unigrams
        bigram_transformer = gensim.models.Phrases([x for x in sentences])
        model = gensim.models.Word2Vec(bigram_transformer[[x for x in sentences]],size = dimensions, workers= 4, sg =1)
        model.save('mymodelbigrams%s-%s' %(yearmin, yearmax))
    
    else:
        model = gensim.models.Word2Vec(sentences, workers= 4, size = dimensions, sg=1)
        model.save('mymodel%s-%s' %(yearmin, yearmax))


def get_model_both(yearmin = 1950, yearmax= 2016, dimensions = 300):
    #run function from sentences iterator to load sentences within a given period snapshot
  
    sentences3 = chain(si.MySentences('X:\\ECHR_TXT', yearmin = yearmin, yearmax = yearmax,court ="ECHR" ),si.MySentences('X:\\ECJ\\txt', yearmin = yearmin, yearmax = yearmax, court = "ECJ" ))
    
    model = gensim.models.Word2Vec(sentences3, workers= 4, size = dimensions, sg=1)
    model.save('bothcourtsmodel%s-%s' %(yearmin, yearmax))

get_model_both(yearmin= 1950, yearmax = 1979 )
get_model_both(yearmin=1979, yearmax = 1989)
get_model_both(yearmin= 1989, yearmax = 2008 )
get_model_both(yearmin= 2008, yearmax = 2016 )


#sentences = si.Get_all_sentences('X:\\ECJ\\txt')
# bigram_transformer = gensim.models.Phrases([x for x in sentences])
#model = gensim.models.Word2Vec(sentences, workers= 4, size = 300, sg=1)
#model.save('allecj400dimensions')