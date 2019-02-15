import networkx as nx
import re
import collections
import operator
from matplotlib import pyplot as plt
graph = nx.read_gexf('../../data/echr-judgments-richmeta.gexf')

nodestrings = []
articles = []
for n in graph.nodes_iter():
	if 'articles' in graph.node[n]:
		nodestrings.append(graph.node[n]['articles'])
		for x in re.split(r';|\+',graph.node[n]['articles']):
			if x not in articles:
				articles.append(x)
print articles

artdict = {}
for x in nodestrings:
	for article in re.split(r';|\+', x):
		#article = article.split('-')[0]
		artdict[article]= artdict.get(article, 0) + 1

sorted_x = sorted(artdict.items(), key=operator.itemgetter(1))

print artdict
print sorted_x
for x in sorted_x:
	print x
print len(nodestrings)


h,a = nx.hits(graph)
l = [[nod, a[nod],graph.node[nod]['date']] for nod in a]
l.sort(key=lambda x: x[1])
for x in l:
	print x


xs = [x[1] for x in l]
ys = [x[2].split('-')[0] for x in l]
plt.scatter(xs,ys)
plt.show()
# sg = graph.subgraph( [n for n,attrdict in graph.node.items() if int(attrdict 
# ['date'].split('-')[0]) < 1980 ] )
# for x in sg.nodes_iter():
# 	print sg.node[x]['date']
# # for n,attrdict in graph.node.items():
# # 	# date = attrdict['date'].split('-')[0]
# # 	# if int(date)< 1980:
# # 	# 	print date