'''
Script for splitting data by sentence, using nltk sentence splitter
Sentence iterator method modified to make this script unnessecary
'''



import nltk.data
import re
import os

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

for dir,subdirs, files in os.walk("X:\\ECJ\\txt\\test"):
    for fname in files:
        if 'EN.HTML.txt' in fname:
            with open(os.path.join(dir, fname)) as fp:

                
                data = fp.read()
                data2 = re.sub('\n', ' ', data)
                data3 = re.sub(' +',' ', data2  )
                x = tokenizer.tokenize(data3.decode('utf8'))
                newname = '%s_sentence_per_line.txt' %(fname.split('.')[0])
                with open(os.path.join(dir,newname), 'wb') as fp2:
                    
                    fp2.write('\n'.join(x).encode('utf8'))