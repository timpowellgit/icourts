import gensim
import logging
import os
import re

class Get_all_sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):

        for dir, subdirs,fnames in os.walk(self.dirname):
            for fname in fnames: 
                
                if 'sentence' in fname:
                    
                    for line in open(os.path.join(dir, fname)):
                        line = re.sub(r'\W',' ',line)
                        yield line.lower().split()



dimensions = [300,400,500,600]
algo = [0, 1]
window = [5, 10]


logging.basicConfig(filename = 'evallogfile', filemode = 'a',format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = gensim.models.Word2Vec.load('allecj400dimensions')
model.accuracy("questions-words.txt", restrict_vocab = 10000)
sentences = Get_all_sentences('X:\\ECJ\\txt')


for d in dimensions:
    for al in algo:
        for w in window:
            
            model = gensim.models.Word2Vec(sentences, size=d, sg=al, window = w, min_count=3 ,workers=4)
            model.accuracy("questions-words.txt", restrict_vocab = 10000)
            logging.info('%s %s %s' %(d, al, w))