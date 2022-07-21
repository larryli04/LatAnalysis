from getWhitakers import getWhitakers
import pprint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

from heirarchypos import hierarchy_pos
from copy import copy, deepcopy

def printDecisionGraph(): # save build_graph as image.png
    print(build_graph.nodes())
    pos = hierarchy_pos(build_graph, "root")
    nx.draw(build_graph, pos,with_labels=True)
    plt.savefig("image.png")

def remainingWords(removed, sentence_info): # determines the remaining pool of words. removed: list of str | sentence_info: list of WordAnalysis objects
    s = deepcopy(sentence_info)

    return [x for x in s if x.words[0].name not in removed] # list of Word objects

def canConnect(word, node): # if two word objects can connect. both word and node are Word objects
    # returns (if the nodes can connect, edge should point out)

    print("out here", word.pos)
    if ((word.pos == "N" or word.pos == "PRON") and node.pos=="V"): # nouns to verbs
        print("in here", word.case)
        if(word.number == node.number): # should add an argument in the case for multiple singular nominatives with plural verb

            if(word.case == "NOM"):
                return [True, True]
                    
        if(word.case == "ACC"):
            return [True, False]
        # not adding verbs yet

    elif (word.pos=="ADJ" and node.pos == "N"): # adj to noun
        if(word.number==node.number and word.case==node.case):
            if(word.gender == "C" or node.gender == "C" or word.gender == node.gender): # no particular gender
                return [True, True]
    

    elif (word.pos=="ADV" and node.pos == "V"): # adverb to verb
        return [True, True]
        
    return [False]

def getVerbs(sentence_info): # get verbs from sentence_info
    verbs = [] # create a list of all verbs each verb is a Word object
    for word in sentence_info: # word is object
        # print(type(word))
        for pos in word.words:
            if pos.pos == "V":
                verbs.append(pos)
    print(verbs)
    return verbs

def initTree(verbs): # create Tree of graphs with a verb as the starting point
    build_graph = nx.DiGraph() # initialize graph of graphs where each verb is the start node
    build_graph.add_node("root", key={"name": "root", "depth":0})

    for verb in verbs:
        G = nx.DiGraph() # start of a sentence graph
        G.add_node(verb.name, key={"data":verb}) 

        build_graph.add_node(G, key={"name":verb.name, "depth":0}) # add to larger graph graph
        build_graph.add_edge("root", G)
    return build_graph

def genTree(large_graph, sentence_in): # populate the rest of the tree according to rules
    blanks = 1 # numbers the unusable nodes
    depth = 1 
    build_graph = large_graph
    sentence_info = sentence_in

    while(depth < len(sentence_info)):
        
        leaves = [x for x in build_graph.nodes() if build_graph.out_degree(x)==0 and build_graph.in_degree(x)==1] # define most recent graphs

        for graph in leaves:
            
            if(isinstance(graph, int)): # give a blank child to unusable nodes
                build_graph.add_node(blanks, key={"data":"zoinks", "depth": depth})
                build_graph.add_edge(graph, blanks)
                blanks+=1
                continue

            for wordanalysis in remainingWords([x for x in graph.nodes()], sentence_info): # pool of words to iterate over
                for word in wordanalysis.words:
                    
                    for node in [x[1]["key"]["data"] for x in graph.nodes(data=True)]: # var:node is a wordanalysis carried in the data of each node in graph
                        
                        
                        if(canConnect(word, node)[0]): # decide if node and word should be connected

                            newgraph = deepcopy(graph) # create editable copy
                            newgraph.add_node(word.name , key={"data":word})

                            if(not canConnect(word, node)[1]): # determine direction
                                newgraph.add_edge(node.name, word.name)
                            else:
                                newgraph.add_edge(word.name, node.name)

                            build_graph.add_node(newgraph, key={"depth":depth}) # add to larger graph
                            build_graph.add_edge(graph, newgraph)
                            
                        else:
                            # designate unusable nodes with integer
                            
                            build_graph.add_node(blanks, key={"depth":depth}) # add to larger graph
                            build_graph.add_edge(graph, blanks)

                            blanks+=1 # makes sure each unusable graph has a unique id
        
        depth = nx.shortest_path_length(build_graph, "root") # gets dict of all path values from root
        depth = max(depth.values()) # updates depth of tree by choosing the longest
    
    print("Depth of build_graph: ",depth)
    subgraphs = [x for x,y in build_graph.nodes(data=True) if y["key"]["depth"]==depth-1] # all graphs at lowest level

    return subgraphs

def cutTree(subgraph): # get rid of duplicate leaves
    graphlist = [] # cut down the total number of graphs to unique ones

    for graph in subgraph:
        if(not isinstance(graph, int)): # gets rid of unusable nodes

            f = True # bool if graph should be added to graphlist

            if(len(graphlist)==0): # adds first value to graphlist
                nx.draw(graph, with_labels=True)
                graphlist.append(graph)
                continue # go to next graph
            
            for ref in graphlist:

                # if a graph is the same as one already in graph list, do not add it to the loop
                if [x[0] for x in sorted([x for x in graph.nodes(data=True)])]==[x[0] for x in sorted([x for x in ref.nodes(data=True)])]:
                    if (sorted([[u,v] for u,v,a in sorted([x for x in ref.edges(data=True)])])==sorted([[u,v] for u,v,a in sorted([x for x in graph.edges(data=True)])])):
                        f = False

            if(f):
                nx.draw(graph, with_labels=True)
                graphlist.append(graph)
                
    plt.savefig("image3.png", dpi=1200)
    return graphlist

sentence = input().split(" ") # manual sentence input
sentence_info = []

for word in sentence: # create sentence_info
    sentence_info.append(getWhitakers(word))


verbs = getVerbs(sentence_info)

build_graph = initTree(verbs)

subgraphs = genTree(build_graph, sentence_info)

possibilities = cutTree(subgraphs)

# nx.write_gexf(final, "graph.gexf")