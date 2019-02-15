# import numpy as np
# import re 
# import matplotlib.pyplot as plt
# import gensim 
# import logging
# import os
import MySQLdb
import getpass
# import argparse
# import getpass
# import shutil
# import html2text
# import codecs
# from tika import parser
from itertools import chain

def generator1():
    for item in 'abcdef':
        yield item

def generator2():
    for item in '123456':
        yield item

generator3 = chain(generator1(), generator2())
for item in generator3:
    print item

#self._connection = MySQLdb.connect(host="127.0.0.1",user="tfv338", passwd=p,db="ecj_copy",port=3306, charset='utf8', use_unicode=True)

# coding: utf-8
# import os
# import subprocess
# import sys
# import win32api
# from bs4 import UnicodeDammit, BeautifulSoup
# import glob


# for dir, subdirs, fnames in os.walk('X:\\ECJ\\ag_opinions'):
#     for fname in fnames:
#        if 'EN.pdf' in fname:
#             path =os.path.join(dir,fname)
#             proc = subprocess.Popen('java -jar D:\\lib\\tika-app-1.5.jar "%s"  ' %(path), stdout=subprocess.PIPE)
#             tmp = proc.stdout.read()
#             soup = BeautifulSoup(tmp)
#             text = soup.getText()
#             celex = fname.split('_')[0]
#             with open('X:\\ECJ\\txt\\%s_ag.txt' %(celex), 'w+') as f:
#                 f.write(text.encode('utf8'))


                

# years = range(1975, 2015, 3)

# print years
# for x in range(1974,2016):
#     print x
#     if x > 1989:

#         if x not in years:

#             listed = years+[x]
#             print listed
#             index =listed.index(x)
#             print listed[index-1]
#         else:
#             year = x
#     else:
#         year = 1989
#     print x,year

# model = TSNE(n_components=2, random_state=0)
# np.set_printoptions(suppress=True)
# import gensim 
# import logging
# import os
# import MySQLdb
# import argparse
# from sklearn.decomposition import PCA

# model = gensim.models.Word2Vec.load('mymodel1950-1995')
# vectors = [model[word] for word in model.vocab]


# pca = PCA(n_components=2, whiten=True)
# vectors2d = pca.fit(vectors).transform(vectors)

# # draw image
# plt.figure(figsize=(10,10))
# plt.axis([0, 0.5, 0, 0.5])

# first = True # color alternation to divide given groups
# alternate = True
# i = 1
# for point, word in zip(vectors2d ,[word for word in model.vocab]):
#     print i , 'of ', len(vectors2d)
#     print word.decode('utf8')
#     i+=1
#     # plot points
#     plt.scatter(point[0], point[1], c='r' if first else 'g')
#     # plot word annotations
#     plt.annotate(
#         word.decode('utf8'), 
#         xy = (point[0], point[1]),
#         xytext = (-7, -6) if first else (7, -6),
#         textcoords = 'offset points',
#         ha = 'right' if first else 'left',
#         va = 'bottom',
#         size = "x-large"
#     )
#     first = not first if alternate else first


# plt.tight_layout() 
# plt.show()










# model.save('allecjbigrams400dimensions')

# import matplotlib.pyplot as plt
# import matplotlib
# import numpy as np


# values1 = [4,6,23,6,7,8,5,32]
# values2 = [4,6,3,66,7,8,53,3]
# values3 = [4,6,3,67,7,38,5,3]
# x = [1974, 1977, 1980]
# y = np.array([np.mean(l) for l in [values1, values2, values3]])
# stdevs = np.array([np.std(l) for l in  [values1,values2,values3]])


# valuesa = [4,6,23,236,723,8,5,2332]
# valuesb = [4,236,3,66,7,8,5233,3]
# valuesc = [4,6,3,67,237,38,5,3]
# y2 = np.array([np.mean(l) for l in [valuesa, valuesb, valuesc]])
# stdevs2 = np.array([np.std(l) for l in  [valuesa,valuesb,valuesc]])


# ax = plt.gca()
# y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
# plt.gca().xaxis.set_major_formatter(y_formatter)

# # Remove the plot frame lines. They are unnecessary chartjunk.  
# ax.spines["top"].set_visible(False)  
# ax.spines["right"].set_visible(False)  

# # Ensure that the axis ticks only show up on the bottom and left of the plot.  
# # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
# ax.get_xaxis().tick_bottom()  
# ax.get_yaxis().tick_left()  

# min =y-stdevs
# max = y+stdevs


# min2 =y2-stdevs2
# max2 = y2+stdevs2

# plt.subplot(2,1,1)
# plt.fill_between(x,min ,max, color="#5DA5DA")  
# plt.plot(x,y , color="white", lw=2)
# plt.title('Cosine similarity between initial "effective" vector \nand later representations. Whole Vocabulary and Sample', fontsize = 14)
# plt.ylabel('Average and Std of Whole \nVocabulary Similarity Change', fontsize = 10)


# plt.subplot(2,1,2)
# plt.fill_between(x,min2 ,max2, color="#FAA43A")  
# plt.plot(x,y2, color='white', lw=2)
# plt.ylabel('Average and Std of \n Sample Words Similarity Change', fontsize= 10)

# plt.savefig('test2gether.png')