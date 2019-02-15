import gensim
import logging

import os
import re
from scipy import spatial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from nltk.corpus import stopwords
import MySQLdb
import getpass
print gensim.__file__

from annotate_with_period import MySentences as sentences


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MySentences(object):
 def __init__(self, dirname, yearmin = 1950, yearmax = 2016):
     self.dirname = dirname
     self.yearmax = yearmax
     self.yearmin = yearmin

 def __iter__(self):
    password = getpass.getpass()
    connection = MySQLdb.connect(host="127.0.0.1",user="tfv338", passwd=password,db="ecj_copy",port=3306, charset='utf8',  use_unicode=True)
    with connection:
        cur = connection.cursor()
        for dir, subdirs, fnames in os.walk(self.dirname):
            for fname in fnames:
                
                if 'sentence' in fname:
                    celex = fname.split('_')[0]
                    cur.execute("SELECT date FROM cases WHERE celex = %s ", (celex,))
                    try:
                        date = cur.fetchall()[0][0]

                        if date.year <= self.yearmax and date.year > self.yearmin:
                            for line in open(os.path.join(dir, fname)):
                                line = re.sub(r'\W',' ',line)
                                print line
                                yield line.lower().split()
                    except:
                        pass



directory = 'X:\\ECJ\\txt'

#train for initial period snapshot eg 1954 -1990
model= gensim.models.Word2Vec(   size=200, sg=1, min_count=3 ,workers=4)
sentences = MySentences(directory, yearmin = 1953, yearmax= 1974)
model.build_vocab(sentences)
model.train(sentences)

#get vector for target word e.g: 'effective'
origin = model['effective']
vocab = [(x, model[x]) for x in model.vocab]

#to be used for plotting avg cosines with a random selection, rather than the whole vocab
random = np.random.choice([x for x in model.vocab if x not in stopwords.words('english')] ,100 )

random_vocab = [(x, model[x]) for x in random]

#start plot with cosine similarity at 1 for initial period, 1974
cosines =[1]

avgcosines = [1]
stds  =[0]

randavgcosines = [1]
randstds = [0]


timeaxis = [1974]
year = 1974
while year < 2016:

    sentencesnew = MySentences(directory, yearmin =year ,  yearmax= year+3 )
    year +=  3
   

    model.build_vocab(sentencesnew, update = True)
    model.train(sentencesnew)
    cos = 1 - spatial.distance.cosine(origin, model['effective'])
    cosines.append(cos)
    timeaxis.append(year)
    avgcos = []
    
    for word, vector in vocab:
        newvector = model[word]
        cos2 = 1 - spatial.distance.cosine(vector, newvector)
        avgcos.append(cos2)
    avgcosines.append(np.mean(avgcos))
    stds.append(np.std(avgcos))

    randcos = []
    for rword, rvector in random_vocab:
        rnewvector = model[rword]
        rcos2 = 1 - spatial.distance.cosine(rvector, rnewvector)
        randcos.append(rcos2)
    randavgcosines.append(np.mean(randcos))
    randstds.append(np.std(randcos))




#get x axis to be start at year used
x_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
plt.gca().xaxis.set_major_formatter(x_formatter)

# Remove the plot frame lines. 
ax = plt.gca()
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
  
# Ensure that the axis ticks only show up on the bottom and left of the plot.  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  

y = np.array(avgcosines)
stdevs = np.array(stds)
min =y-stdevs
max = y+stdevs

plt.subplot(2,1,1)
plt.fill_between(timeaxis,min ,max, color="#d3d3d3") 
plt.plot(timeaxis,cosines, color= 'k')
plt.plot(timeaxis,avgcosines, color = 'w')
plt.title('Cosine similarity between initial "effective" vector \nand later representations. Whole Vocabulary and Sample', fontsize = 14)
plt.ylabel('Average and Std of Whole \nVocabulary Similarity Change', fontsize = 10)

y2 = np.array(randavgcosines)
stdevs2 = np.array(randstds)
min2 =y2-stdevs2
max2 = y2+stdevs2


plt.subplot(2,1,2)
plt.fill_between(timeaxis,min2 ,max2, color="#d3d3d3") 
plt.plot(timeaxis,cosines, color= 'k')
plt.plot(timeaxis,randavgcosines, color = 'w')
plt.ylabel('Average and Std of \n Sample Words Similarity Change', fontsize= 10)
plt.savefig('randomcosines_and_whole.png')
print(random)