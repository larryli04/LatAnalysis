

from distutils.command.build import build
from getWhitakers import getWhitakers
import pprint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import random
from heirarchypos import hierarchy_pos
from copy import copy, deepcopy

def remainingWords(removed, sentence_info): # takes sentence_info object and determines the remaining pool of words
    s = deepcopy(sentence_info)
    for word in s:
        if(word[0]["name"] in removed):
            s.remove(word)

    return s


def canConnect(word, node): # if two word objects can connect

    if (word["pos"]=="N" and node["pos"]=="V" or word["pos"]=="V" and node["pos"]=="N"):
        if(word["number"] == node["number"]): 
            if(word["pos"] == "N"):
                if(word["case"] == ["NOM"]):
                    return True
                    
        if(word["case"] == ["ACC"]):
                    return True
        # not adding verbs yet

    # cannot add noun to adj
    elif (word["pos"]=="ADJ" and node["pos"] == "N"): # adj to noun
        if(word["gender"]==node["gender"] and word["number"]==node["number"] and word["case"]==node["case"]):
            return True
        pass
    elif (word["pos"]=="ADV" and node["pos"] == "V"):
        return True
        
        pass
    return False

sentence = input().split(" ") # manual sentence input
sentence_info = []

for word in sentence:
    sentence_info.append(getWhitakers(word))
# print("SENTENCE INFO")
# pprint.pprint(sentence_info)
# pprint.pprint(getWhitakers("canis"))

# print(remainingWords(["canis"], sentence_info))
# exit()

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

# G = {}
build_graph = nx.DiGraph()
build_graph.add_node("root")#, key={"name": "root"})
for verb in verbs:
    G = nx.Graph()
    G.add_node(verb["name"], key={"data":verb})#, key={"name": verb}) # start of a sentence graph
    
    

    build_graph.add_node(G, key={"name":verb["name"]}) # add to decision graph
    build_graph.add_edge("root", G)


# iterate through the sentence pool (and over each verb start) OR maybe the graphs and then iterate through remaining words (iterate through changing list? when to stop?)
# NEW IDEA make a tree of graphs where each change is a new set of leaves. must recursively iterate through the tree until all are complete at each level k is a graph of size k

#  until all are complete at each level k is a graph of size k

blanks = 1
leaves = [x for x in build_graph.nodes() if build_graph.out_degree(x)==0 and build_graph.in_degree(x)==1]
print(len(leaves))
for graph in leaves:
    # print(type([x for x in graph.nodes()][0]))
    print("COOM")
    print([x for x in graph.nodes()])
    print(remainingWords(['canis'], sentence_info))
    for wordlist in remainingWords([x for x in graph.nodes()], sentence_info):
        # pprint.pprint(remainingWords([x for x in graph.nodes()], sentence_info))
        print("WORDLIST")
        pprint.pprint(wordlist)
        # if you find a match, add
        # else delete this graph chain
        for word in wordlist:
            for node in [x[1]["key"]["data"] for x in graph.nodes(data=True)]:
                # pprint.pprint(node)
                # pprint.pprint(word)
                if(canConnect(word, node)):
                    # make new graph in build_graph with changes
                    newgraph = deepcopy(graph)
                    newgraph.add_node(word["name"])
                    newgraph.add_edge(node["name"], word["name"])

                    build_graph.add_node(newgraph)
                    build_graph.add_edge(graph, newgraph)
                else:
                    # cannot create a graph in this configuration, abandon this line
                    # create dummy child with noParse flag
                    build_graph.add_node(blanks)
                    build_graph.add_edge(graph, blanks)
                    blanks+=1
                    pass


# print(build_graph.nodes())
# pos = hierarchy_pos(build_graph, "root")
# nx.draw(build_graph, pos, with_labels=True)
# plt.savefig("image.png")

print(build_graph.nodes())
pos = hierarchy_pos(build_graph, "root")
nx.draw(build_graph, with_labels=True)
plt.savefig("image.png")

# decide possible insertion locations based on metadata

# if there is multiple places where it could go, make copies of the graph
# if there are no places for it to go, delete the graph.

