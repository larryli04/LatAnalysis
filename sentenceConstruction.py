
from distutils.command.build import build
from getWhitakers import getWhitakers
import pprint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import random
from heirarchypos import hierarchy_pos

def remainingWords(removed, sentence_info): # takes sentence_info object and determines the remaining pool of words
    s = sentence_info
    for word in s:
        if(word[0]["name"] in removed):
            s.remove(word)

    return s


sentence = input().split(" ") # manual sentence input
sentence_info = []

for word in sentence:
    sentence_info.append(getWhitakers(word))

# pprint.pprint(sentence_info)

# construct a graph based on possibilities

# start with the verb

# verbs
verbs = [] # list of all verbs
for word in sentence_info:
    # print(type(word))
    for pos in word:
        if pos["pos"] == "V":
            verbs.append(pos)
pprint.pprint(verbs)
# initialize array of graphs where each verb is the start node

graphs = []
build_graph = nx.DiGraph()
build_graph.add_node("root")#, key={"name": "root"})
for verb in verbs:
    G = nx.Graph()
    G.add_node(verb["name"])#, key={"name": verb}) # start of a sentence graph

    build_graph.add_node(G) # add to decision graph
    build_graph.add_edge("root", G)

print(build_graph.nodes())
pos = hierarchy_pos(build_graph, "root")
nx.draw(build_graph, pos)
plt.savefig("image.png")



# iterate through the sentence pool (and over each verb start) OR maybe the graphs and then iterate through remaining words (iterate through changing list? when to stop?)
# NEW IDEA make a tree of graphs where each change is a new set of leaves. must recursively iterate through the tree until all are complete at each level k is a graph of size k

leaves = [x for x in build_graph.nodes() if build_graph.out_degree(x)==0 and build_graph.in_degree(x)==1]

for graph in leaves:
    for word in remainingWords([x for x in graph.nodes()], sentence_info):
        # if you find a match, add
        # else delete this graph chain
        for node in graph.nodes():
            if(canConnect(word, node)):
                graph.add_node()


# decide possible insertion locations based on metadata

# if there is multiple places where it could go, make copies of the graph
# if there are no places for it to go, delete the graph.

for word in remainingWords(graphs[0],sentence_info): # just use the first verb
    for type in word:
        pos = type["pos"]
        if (pos=="N"):
            # what things can attach to nouns, and what criteria do they have to satisfy?
            # verbs with matching number and case (NOM or ACC)
            # ADJ with matching case, gender, and number
            pass
        elif (pos=="V"):
            # what things can attach to verbs, and what criteria to they have to satisfy?
            # None rn because only one verb

            # currently just throw away the verb
            pass
        elif (pos=="ADJ"):
            # must attach to nouns with matching case, number, and gender
            pass
        elif (pos=="ADV"):
                    
            # must attach to verbs with no criteria
            pass

        print(pos)