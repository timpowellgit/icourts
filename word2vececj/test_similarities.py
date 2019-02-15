'''
Load model created by word2vececj.py
Retrieve similar words to target words in saved model (by snapshot or entire corpsus)
*consider combining this script with word2vececj.py

'''

import gensim

def neighborhoods_by_year(yearmin, yearmax, words):

    model = gensim.models.Word2Vec.load('mymodel%s-%s' %(yearmin,yearmax))
    for x in words:
        neighbors = model.most_similar(x, topn = 30)
        print '******   ', yearmin, yearmax ,'        ********', '\n'
        print '******   ', x ,'        ********', '\n'
        print '**** model vocabulary size', len(model.vocab) , '****'
        for n in neighbors:
            print n
        print '\n'

words = ['effective', 'effectiveness']

neighborhoods_by_year(1950, 1990, words)
neighborhoods_by_year(2009,2016, words)

model = gensim.models.Word2Vec.load('allecj400dimensions')
for x in words:
    neighbors = model.most_similar(x, topn = 30)
    print '******   ', x, 'whole corpus' ,'        ********', '\n'
    print '**** model vocabulary size', len(model.vocab) , '****'
    for n in neighbors:
        print n
    print '\n'