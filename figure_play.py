
import math
import matplotlib.pyplot as plt
 
def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs,path

    try:
        makedirs(mypath)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise

#final_topics = [u'0.183*member + 0.029*state + 0.013*national + 0.012*union + 0.011*regulation + 0.011*residence + 0.011*states + 0.010*law + 0.009*freedom + 0.009*community + 0.008*treaty + 0.008*workers + 0.008*nationals + 0.007*effect + 0.007*provisions', u'0.018*member + 0.016*law + 0.015*national + 0.013*community + 0.012*state + 0.009*commission + 0.009*treaty + 0.009*states + 0.009*effect + 0.007*order + 0.007*caselaw + 0.007*principle + 0.006*decision + 0.006*public + 0.006*tax']
final_topics =['0.038*member + 0.028*state + 0.019*union + 0.016*states + 0.015*law + 0.014*national + 0.013*nationality + 0.013*nationals + 0.012*treaty + 0.011*treatment', '0.041*regulation + 0.030*state + 0.027*member + 0.025*social + 0.022*benefits + 0.018*security + 0.016*benefit + 0.016*workers + 0.015*legislation + 0.012*national','0.039*law + 0.036*national + 0.022*community + 0.015*order + 0.014*principle + 0.014*question + 0.014*interpretation + 0.013*courts + 0.012*caselaw + 0.012*legal']
num_topics = 3
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
    plt.figure(figsize=(10,10))

    plt.ylim(0, 300)  # stretch the y-axis to accommodate the words
    print totalfonts
    plt.xticks([])  # remove x-axis markings ('ticks')
    plt.yticks([]) # remove y-axis markings ('ticks')
    plt.title('Topic #{}'.format(t+1))
    previous_score  = 0
    for i, (word, score) in enumerate(topicwords):
        if previous_score ==0:
            previous_score = score
            print type(word)
        plt.text(0.03, 270-(i*25), '%s.%s -%s' %(i,word, score/1000), fontsize=score) 
        previous_score = score
    mkdir_p(str(num_topics))
    plt.savefig('{0}/figure{1}.png'.format(num_topics,t), dpi = 300) 
    plt.close()

#plt.tight_layout()
