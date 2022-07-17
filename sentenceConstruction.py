

from getWhitakers import getWhitakers
import pprint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

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
    # returns can connect?, arrow out
    if (word.pos=="N" and node.pos=="V"):

        if(word.number == node.number):
            
            if(word.pos == "N"):
                print(word.case)
                if(word.case == "NOM"):

                    return [True, True]
                    
        if(word.case == "ACC"):

            return [True, False]
        # not adding verbs yet

    # cannot add noun to adj
    elif (word.pos=="ADJ" and node.pos == "N"): # adj to noun
        if(word.gender==node.gender and word.number==node.number and word.case==node.case):
            return [True]
        pass
    elif (word.pos=="ADV" and node.pos == "V"):
        return [True]
        
        pass
    return [False]

def printGraph(graph, root, path):
    # print(build_graph.nodes())
    if(root==None):
        nx.draw(graph, with_labels=True)
        plt.show()
    else:
        # pos = hierarchy_pos(graph, root)
        nx.draw(graph,with_labels=True)
        plt.show()
        plt.savefig(path, dpi=1200)
        

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
    G = nx.DiGraph()
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
            # give a blank child
            build_graph.add_node(blanks, key={"data":"zoinks", "depth": depth})
            build_graph.add_edge(graph, blanks)
            blanks+=1
            continue

        for wordanalysis in remainingWords([x for x in graph.nodes()], sentence_info): # pool of words to iterate over
            # if you find a match, add
            # else delete this graph chain
            for word in wordanalysis.words: # each different word in a wordanalysis
                
                print([x[1] for x in graph.nodes(data=True)])
                
                for node in [x[1]["key"]["data"] for x in graph.nodes(data=True)]: # var:node is a wordanalysis carried in the data of each node in graph
                    pprint.pprint(node.name)
                    pprint.pprint(word.name)
                    if(canConnect(word, node)[0]):
                        #connect new graph in build_graph with changes
                        # should be subject -> verb -> object
                        newgraph = deepcopy(graph)
                        
                        newgraph.add_node(word.name , key={"data":word})
                        if(not canConnect(word, node)[1]):
                            newgraph.add_edge(node.name, word.name)
                        else:
                            newgraph.add_edge(word.name, node.name)
                        build_graph.add_node(newgraph, key={"name":verb.name, "depth":depth})
                        build_graph.add_edge(graph, newgraph)

                        

                        print(newgraph)
                        
                        
                    else:
                        # cannot create a graph in this configuration, abandon this line
                        
                        build_graph.add_node(blanks, key={"depth":depth})
                        build_graph.add_edge(graph, blanks)
                        blanks+=1
                        
                        pass
    
    depth = nx.shortest_path_length(build_graph, "root")
    depth = max(depth.values())


# save build_graph as image.png

# print(build_graph.nodes())
# pos = hierarchy_pos(build_graph, "root")
# nx.draw(build_graph, pos,with_labels=True)
# plt.savefig("image.png")


print(depth)
subgraph = [x for x,y in build_graph.nodes(data=True) if y["key"]["depth"]==depth-1]
print(subgraph)


graphlist = [] # cut down the total number of graphs to unique ones
for graph in subgraph:
    if(not isinstance(graph, int)):
        print("how")
        if(len(graphlist)==0):
            print(1)
            nx.draw(graph, with_labels=True)
            graphlist.append(graph)
            continue
        f = True
        for ref in graphlist:


            if [x[0] for x in sorted([x for x in graph.nodes(data=True)])]==[x[0] for x in sorted([x for x in ref.nodes(data=True)])] and (sorted([[u,v] for u,v,a in sorted([x for x in ref.edges(data=True)])])==sorted([[u,v] for u,v,a in sorted([x for x in graph.edges(data=True)])])):
                f = False

                
        if(f):
            # debug info
            # print([x[0] for x in sorted([x for x in graph.nodes(data=True)])],[x[0] for x in sorted([x for x in ref.nodes(data=True)])], [u for u,v in sorted([x for x in ref.nodes(data=True)])]!=[u for u,v in sorted([x for x in graph.nodes(data=True)])])
            # print(sorted([[u,v] for u,v,a in sorted([x for x in ref.edges(data=True)])]),sorted([[u,v] for u,v,a in sorted([x for x in graph.edges(data=True)])]), (sorted([[u,v] for u,v,a in sorted([x for x in ref.edges(data=True)])])!=sorted([[u,v] for u,v,a in sorted([x for x in graph.edges(data=True)])])))
            
            nx.draw(graph, with_labels=True)
            graphlist.append(graph)
            

                
plt.show()
plt.savefig("image3.png", dpi=1200)
# nx.write_gexf(final, "graph.gexf")
        