'''
Script for annotating the entire corpus with timestamped target words
ex: effective_2002

Word2vec training is done on entire corpus.
PCA or tSNE is used for visualization of target word displacement and neighborhoods


'''


import gensim 
import logging
import os
import MySQLdb
import argparse
import getpass
import re
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
 def __init__(self, dirname, yearmin = 1975, yearmax = 2015, step =3, cutoff = 1989):
     self.dirname = dirname
     self.yearmax = yearmax
     self.yearmin = yearmin
     self.step = step
     self.cutoff = cutoff
     password = getpass.getpass()
     self._connection = MySQLdb.connect(host="127.0.0.1",user="tfv338", passwd=password,db="ecj_copy",port=3306, charset='utf8',  use_unicode=True)
 def __iter__(self):

    years = range(self.yearmin, self.yearmax, self.step)
   

    with self._connection:
        cur = self._connection.cursor()
        for dir, subdirs, fnames in os.walk(self.dirname):
            for fname in fnames:
                
                if 'sentence' in fname:
                    celex = fname.split('_')[0]
                    cur.execute("SELECT date FROM cases WHERE celex = %s ", (celex,))
                    try:
                        date = cur.fetchall()[0][0]

                        if date.year > self.cutoff :

                            if date.year not in years:

                                listed = years+[date.year]
                                index =listed.index(date.year)
                                year = listed[index-1]
                            else:
                                year = date.year
                        else:
                            year = self.cutoff
                        for line in open(os.path.join(dir, fname)):
                            line = re.sub(r'\W',' ',line)
                            
                            line = line.lower()
                            line = re.sub(r'effectiveness ','effectiveness_%s ' %(year),line).split()
                            
                            
                            yield line
                    except:
                        pass

#sentences = MySentences('X:\\ECJ\\txt')
#model = gensim.models.Word2Vec(sentences, size=300, sg=1, min_count=3 ,workers=4)
#model.save('annotatedmodel_effectiveness')


model = gensim.models.Word2Vec.load('annotatedmodel_effectiveness')
vectorsandwords = [[model[word],word ] for word in model.vocab]

vectors = [x[0] for x in vectorsandwords]
words= [x[1] for x in vectorsandwords]
pca = PCA(n_components=2, whiten=True)
vectors2d = pca.fit(vectors).transform(vectors)


#get only similar words for plotting
neighbors = []
effectives = []
effectiveswords = []
for x in range(1975,2015, 3):
    if x > 1989:
        year = x
    else:
        year=1989
    effective = 'effectiveness_%s' %(year)
    effectives.append(vectors2d[words.index(effective)])
    effectiveswords.append(effective)
    neighborhood = model.most_similar(effective, topn = 300)
    for n in neighborhood:
            neighbors.append(n[0])


neighbors = set(neighbors)
effvecs =[vectors2d[words.index(n)] for n in neighbors]
effwords =[n for n in neighbors]

# draw image
plt.figure(figsize=(20,20))
plt.axis([-2.5, -1 , .3, 1.7])




first = True # color alternation to divide given groups
alternate = True

for point, word in zip(effvecs ,effwords):
    if 'effective' not in word:
        

        # plot points
        plt.scatter(point[0], point[1], c='r' )
        # plot word annotations
        plt.annotate(
            word.decode('utf8'), 
            xy = (point[0], point[1]),
            xytext = (-7, -6) if first else (7, -6),
            textcoords = 'offset points',
            ha = 'right' if first else 'left',
            va = 'bottom',
            size = "small"
        )
        first = not first if alternate else first

for point, word in zip(effectives,effectiveswords):
    plt.scatter(point[0], point[1], c='b')
    plt.annotate(
            word.decode('utf8'), 
            xy = (point[0], point[1]),
            xytext = (-7, -6) if first else (7, -6),
            textcoords = 'offset points',
            ha = 'right',
            va = 'bottom',
            size = "medium"
        )
plt.plot([x[0] for x in effectives], [x[1] for x in effectives ])
plt.tight_layout() 
plt.show()



