
import os
import wordcloud
import matplotlib.pyplot as plt
import math
import numpy as np

MODELS_DIR = "models"

final_topics = open(os.path.join(MODELS_DIR, "final_topics.txt"), 'rb')
curr_topic = 0

wordclouds = []
for line in final_topics:
    line = line.strip()[line.rindex(":") + 2:]
    scores = [float(x.split("*")[0]) for x in line.split(" + ")]
    words = [x.split("*")[1] for x in line.split(" + ")]
    freqs = []
    for word, score in zip(words, scores):
        freqs.append((word, score*1000))
    multiplied = []
    for x in freqs:
        word = x[0]
        for y in range(int(x[1])):
            multiplied.append(word)
    text = " ".join([word for word in multiplied])
    wc = wordcloud.WordCloud(height=250, width=600, prefer_horizontal=1.0, min_font_size=1).generate(text)
    wordclouds.append(wc)

    #elements = wordcloud.WordCloud().fit_words(freqs)
    #wordcloud.WordCloud().draw(elements, "gs_topic_%d.png" % (curr_topic), width=120, height=120)
    curr_topic += 1
final_topics.close()

ncolumns = int(math.ceil(math.sqrt(curr_topic)))
fig = plt.figure()
print ncolumns, curr_topic

for i in range(curr_topic):
    plt.subplot(ncolumns-1, ncolumns, i+1)
    #subplot_arg = '%s%s%s' %(curr_topic,ncolumns, i+1)
    #inted = int(subplot_arg)
    #fig.add_subplot(inted) 
    plt.axis("off")
    plt.subplots_adjust(bottom=0.1, left=0, right=.99, top=.91, hspace=.05, wspace=.05)

    plt.imshow(wordclouds[i])


plt.show()

fig, axes = plt.subplots(nrows=4, ncols=4)
fig.tight_layout() # Or equivalently,  "plt.tight_layout()"

plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
t = np.arange(0.0, 1.0, 0.001)
a0 = 5
f0 = 3
s = a0*np.sin(2*np.pi*f0*t)
l, = plt.plot(t,s, lw=2, color='red')
plt.axis([0, 1, -10, 10])

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
axamp  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)

sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0)
samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)

def update(val):
    amp = samp.val
    freq = sfreq.val
    l.set_ydata(amp*np.sin(2*np.pi*freq*t))
    fig.canvas.draw_idle()
sfreq.on_changed(update)
samp.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event):
    sfreq.reset()
    samp.reset()
button.on_clicked(reset)

rax = plt.axes([0.025, 0.5, 0.15, 0.15], axisbg=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

plt.show()