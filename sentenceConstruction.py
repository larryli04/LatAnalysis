
from getWhitakers import getWhitakers
import pprint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import random
from heirarchypos import hierarchy_pos
from copy import copy, deepcopy

def remainingWords(removed, sentence_info): # determines the remaining pool of words. removed: list of str | sentence_info: list of WordAnalysis objects
    s = deepcopy(sentence_info)

    
    # for wordanalysis in s:
    #     print(len(s))
    #     print(wordanalysis.words[0].name)
    #     if(wordanalysis.words[0].name in removed):
    #         s.remove(wordanalysis)
            

    return [x for x in s if x.words[0].name not in removed] # list of Word objects


# def canConnect(word, node): # if two word objects can connect. both word and node are Word objects

#     if (word["pos"]=="N" and node["pos"]=="V" or word["pos"]=="V" and node["pos"]=="N"):
#         if(word["number"] == node["number"]): 
#             if(word["pos"] == "N"):
#                 if(word["case"] == ["NOM"]):
#                     return True
                    
#         if(word["case"] == ["ACC"]):
#                     return True
#         # not adding verbs yet

#     # cannot add noun to adj
#     elif (word["pos"]=="ADJ" and node["pos"] == "N"): # adj to noun
#         if(word["gender"]==node["gender"] and word["number"]==node["number"] and word["case"]==node["case"]):
#             return True
#         pass
#     elif (word["pos"]=="ADV" and node["pos"] == "V"):
#         return True
        
#         pass
#     return False
def canConnect(word, node): # if two word objects can connect. both word and node are Word objects

    if (word.pos=="N" and node.pos=="V" or word.pos=="V" and node.pos=="N"):

        if(word.number == node.number):
            
            if(word.pos == "N"):
                print(word.case)
                if(word.case == "NOM"):

                    return True
                    
        if(word.case == "ACC"):

            return True
        # not adding verbs yet

    # cannot add noun to adj
    elif (word.pos=="ADJ" and node.pos == "N"): # adj to noun
        if(word.gender==node.gender and word.number==node.number and word.case==node.case):
            return True
        pass
    elif (word.pos=="ADV" and node.pos == "V"):
        return True
        
        pass
    return False

def printGraph(graph, root):
    # print(build_graph.nodes())
    if(root==None):
        nx.draw(graph, with_labels=True)
        plt.show()
    else:
        # pos = hierarchy_pos(graph, root)
        nx.draw(graph,with_labels=True)
        plt.show()
        plt.savefig("image.png")

sentence = input().split(" ") # manual sentence input
sentence_info = []

for word in sentence:
    sentence_info.append(getWhitakers(word))
print("SENTENCE INFO")
pprint.pprint(sentence_info)
print(sentence_info[0].words)

# pprint.pprint(getWhitakers("canis"))

# print(remainingWords(["canis"], sentence_info))
# exit()

# construct a graph based on possibilities

# start with the verb

# verbs
verbs = [] # list of all verbs each verb is a Word object
for word in sentence_info: # word is object
    # print(type(word))
    for pos in word.words:
        if pos.pos == "V":
            verbs.append(pos)
print("VERBS")
pprint.pprint(verbs)
# initialize array of graphs where each verb is the start node

depth = 0
# G = {}
build_graph = nx.DiGraph()
build_graph.add_node("root", key={"name": "root", "depth":depth})
for verb in verbs:
    G = nx.Graph()
    G.add_node(verb.name, key={"data":verb})#, key={"name": verb}) # start of a sentence graph
    
    

    build_graph.add_node(G, key={"name":verb.name, "depth":depth}) # add to decision graph
    build_graph.add_edge("root", G)

# iterate through the sentence pool (and over each verb start) OR maybe the graphs and then iterate through remaining words (iterate through changing list? when to stop?)
# NEW IDEA make a tree of graphs where each change is a new set of leaves. must recursively iterate through the tree until all are complete at each level k is a graph of size k

#  until all are complete at each level k is a graph of size k
blanks = 1
depth = 1
while(depth < len(sentence_info)):
    
    leaves = [x for x in build_graph.nodes() if build_graph.out_degree(x)==0 and build_graph.in_degree(x)==1]
    print(leaves)
    for graph in leaves:
        
        if(isinstance(graph, int)):
            # give a child
            build_graph.add_node(blanks, key={"data":"zoinks", "depth": depth})
            build_graph.add_edge(graph, blanks)
            blanks+=1
            # depth = nx.shortest_path_length(build_graph,"root")
            # depth = max(depth.values())
            continue
        # print(graph)
        # print(type([x for x in graph.nodes()][0]))
        print("COOM")
        print([x for x in graph.nodes()])
        
        # print([x[1] for x in graph.nodes(data=True)])
        print([x.words[0].name for x in remainingWords([x for x in graph.nodes()], sentence_info)])

        for wordanalysis in remainingWords([x for x in graph.nodes()], sentence_info): # pool of words to iterate over
            # pprint.pprint(remainingWords([x for x in graph.nodes()], sentence_info))
            print("WORD ANALYSIS")
            pprint.pprint(wordanalysis.words)
            # if you find a match, add
            # else delete this graph chain
            for word in wordanalysis.words: # each part of speech in a wordanalysis
                
                print([x[1] for x in graph.nodes(data=True)])
                
                for node in [x[1]["key"]["data"] for x in graph.nodes(data=True)]: # each node is a wordanalysis carried in the data of each node
                    pprint.pprint(node.name)
                    pprint.pprint(word.name)
                    if(canConnect(word, node)):
                        # make new graph in build_graph with changes
                        print("NEWGRAPH")
                        newgraph = deepcopy(graph)
                        
                        newgraph.add_node(word.name , key={"data":word})
                        newgraph.add_edge(node.name, word.name)

                        build_graph.add_node(newgraph, key={"name":verb.name, "depth":depth})
                        build_graph.add_edge(graph, newgraph)

                        

                        print(newgraph)
                        
                        
                    else:
                        # cannot create a graph in this configuration, abandon this line
                        

                        print("made blanks")
                        build_graph.add_node(blanks, key={"depth":depth})
                        build_graph.add_edge(graph, blanks)
                        blanks+=1
                        
                        pass
    
    depth = nx.shortest_path_length(build_graph, "root")
    depth = max(depth.values())


# print(build_graph.nodes())
# pos = hierarchy_pos(build_graph, "root")
# nx.draw(build_graph, pos, with_labels=True)
# plt.savefig("image.png")

print(build_graph.nodes())
pos = hierarchy_pos(build_graph, "root")
nx.draw(build_graph, pos,with_labels=True)
plt.savefig("image.png")

# decide possible insertion locations based on metadata

# if there is multiple places where it could go, make copies of the graph
# if there are no places for it to go, delete the graph.
print(depth)
subgraph = [x for x,y in build_graph.nodes(data=True) if y["key"]["depth"]==depth-1]
print(subgraph[0])
printGraph(subgraph[0], False)