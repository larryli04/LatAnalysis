from distutils.command.build import build
from getWhitakers import getWhitakers
import networkx as nx
import matplotlib.pyplot as plt

from heirarchypos import hierarchy_pos
from copy import copy, deepcopy

def printDecisionGraph(): # save build_graph as image.png
    
    pos = hierarchy_pos(build_graph, "root")
    labels = {key: (value["new"],value["delete"]) for (key, value) in nx.get_node_attributes(build_graph, 'key').items()}
    # print(labels)
    nx.draw(build_graph, pos, font_size = 1, node_size = 3,labels = labels)
    plt.savefig("images/direction.png", dpi=1000)

def remainingWords(removed, sentence_info): # determines the remaining pool of words. removed: list of str | sentence_info: list of WordAnalysis objects
    s = deepcopy(sentence_info)

    return [x for x in s if x.words[0].name not in removed] # list of Word objects

def canConnect(word, graphnode, graph): # if two word objects can connect. both word and node are Word objects
    # returns (if the nodes can connect, word to node arrow, "edge data", if the preposition doesn't have a noun, multiple connections)
    node = graphnode[1]["key"]["data"]
    # print(((word.pos == "N" or word.pos == "PRON") and node.pos=="PREP"))
    if ((word.pos == "N" or word.pos == "PRON") and node.pos=="V"): # nouns to verbs

        if(word.number == node.number): # should add an argument in the case for multiple singular nominatives with plural verb

            if(word.case == "NOM"):
                return [True, True, "subject of", None]
                    
        if(word.case == "ACC"): # an accusative with no preposition is just the DO anyways
            return [True, False, "object of", None]

        if(word.case == "GEN"): # when used adverbially
            return [True, True, "adverbial genitive", None]

        if(word.case == "ABL"):
            return [True, False, "case use no prep", None]

        if(word.case == "DAT"):
            return [True, False, "case use no prep", None]

    elif (word.pos == "ADJ" and node.pos=="V"): # substantive adjectives

        if(word.number == node.number): # should add an argument in the case for multiple singular nominatives with plural verb

            if(word.case == "NOM"):
                return [True, True, "(adj) subject of", None]
                    
        if(word.case == "ACC"): # an accusative with no preposition is just the DO anyways
            print(word.name, node.name)
            return [True, False, "(adj) object of", None]

        if(word.case == "GEN"): # when used adverbially
            return [True, True, "(adj) adverbial genitive", None]

        if(word.case == "ABL"):
            return [True, False, "(adj) case use no prep", None]

        if(word.case == "DAT"):
            return [True, False, "(adj) ase use no prep", None]

        # not adding verbs yet
    elif ((word.pos == "N" or word.pos == "PRON") and (node.pos == "N" or node.pos == "PRON")):
        if (word.case == "GEN"):
            return [True, True, "genitive of", None]

        pass
    elif ((word.pos == "N" or word.pos == "PRON") and node.pos=="PREP"): # only allow one

        if(node.plus == word.case):
            if(graph.out_degree(graphnode[0])==1): # prep connected only to verb and no noun
                return [True, False, "prep", False]


    elif (word.pos=="ADJ" and node.pos == "N"): # adj to noun
        if(word.number==node.number and word.case==node.case):
            if(word.gender == "C" or node.gender == "C" or word.gender == node.gender): # no particular gender
                return [True, True, "describes", None]
    
    elif (word.pos == "V" and node.pos == "V"):
        if(word.mood == "INF"):
            return [True, "both", "subject of", None] # work on this

            
    elif (word.pos=="ADV" and node.pos == "V"): # adverb to verb
        return [True, True, "describes", None]

    elif (word.pos=="ADV" and node.pos == "VPAR"): # adverb to verb
        return [True, True, "describes", None]

    elif (word.pos == "PREP" and node.pos == "V"): # attach all prepositions to verbs
        return [True, True, "prep to", True]

    elif (word.pos == "VPAR" and node.pos == "N"):
        if(word.number == node.number):
            if(word.case == node.case):
                if(word.gender == "X" or word.gender == node.gender):
                    return [True, True, "describes", None]
        if(node.pos == "ACC"):
            return [True, True, "object of", None]
    
    elif (word.pos == "VPAR" and node.pos == "V"):

        if(word.case == "ABL"):
            return [True, True, "Abl Abs", None]
    elif (word.pos == "N" and node.pos == "VPAR"):

        if(word.case == node.case):
            if(word.case == "ABL"):
                if(word.number == node.number):
                    return [True, True, "Abl Abs obj", None]
        
    return [False]

def getVerbs(sentence_info): # get verbs from sentence_info
    verbs = [] # create a list of all verbs each verb is a Word object
    for word in sentence_info: # word is object
        # print(type(word))
        for pos in word.words:
            if pos.pos == "V" and pos.mood != "INF":
                verbs.append(pos)
    print(verbs)
    return verbs

def initTree(verbs): # create Tree of graphs with a verb as the starting point
    build_graph = nx.DiGraph() # initialize graph of graphs where each verb is the start node
    build_graph.add_node("root", key={"name": "root", "depth":0, "delete": None, "new":"root"})

    for verb in verbs:
        G = nx.DiGraph() # start of a sentence graph
        G.add_node(verb.name, key={"data":verb}) 

        build_graph.add_node(G, key={"name":verb.name, "depth":0, "delete": None, "new":verb.name}) # add to larger graph graph
        build_graph.add_edge("root", G)
    return build_graph

def genTree(large_graph, sentence_in): # populate the rest of the tree according to rules
    blank = 0
    depth = 1 
    build_graph = large_graph
    sentence_info = sentence_in

    while(depth < len(sentence_info)):
        
        leaves = [x for x in build_graph.nodes(data=True) if build_graph.out_degree(x[0])==0 and build_graph.in_degree(x[0])==1 and x[1]["key"]["depth"] == depth-1] # define most recent graphs

        # if depth is not the verb only, then remove duplicates
        if(depth > 1):
            leaves = cutTree(leaves, False)


        for lgraph in leaves:
            graph = lgraph[0]
            delete = lgraph[1]["key"]["delete"]

            for wordanalysis in remainingWords([x for x in graph.nodes()], sentence_info): # pool of words to iterate over
                for word in wordanalysis.words:
                    
                    for graphnode in graph.nodes(data=True): # var:node is a wordanalysis carried in the data of each node in graph

                        node = graphnode[1]["key"]["data"]
                        if(canConnect(word, graphnode, graph)[0]): # decide if node and word should be connected

                            newgraph = deepcopy(graph) # create editable copy
                            newgraph.add_node(word.name , key={"data":word})

                            if(canConnect(word, graphnode, graph)[1] == False): # determine direction
                                newgraph.add_edge(node.name, word.name, rel=canConnect(word, graphnode, graph)[2])
                            elif (canConnect(word, graphnode, graph)[1] == True):
                                newgraph.add_edge(word.name, node.name, rel=canConnect(word, graphnode, graph)[2])
                            elif (canConnect(word, graphnode, graph)[1]=="both"):
                                newgraph2 = deepcopy(newgraph)
                                newgraph.add_edge(node.name, word.name, rel="object of")
                                
                                newgraph2.add_edge(word.name, node.name, rel="subject of")

                            
                            if(canConnect(word, graphnode, graph)[3]!=None):
                                delete = canConnect(word, graphnode, graph)[3]

                            build_graph.add_node(newgraph, key={"depth":depth, "delete":delete, "new":word.name}) # add to larger graph
                            build_graph.add_edge(graph, newgraph, dir = blank)

                            if(canConnect(word, graphnode, graph)[1]=="both"):
                                print("double")
                                build_graph.add_node(newgraph2, key={"depth":depth, "delete":delete, "new":word.name}) # add to larger graph
                                build_graph.add_edge(graph, newgraph2, dir = blank)

                            delete = lgraph[1]["key"]["delete"]
                            blank += 1
                            
                        else:
                            pass
            

        depth += 1
        
    
    
    print("Depth of build_graph: ",depth)
    print(build_graph.number_of_nodes(), "nodes")
    subgraphs = [x for x in build_graph.nodes(data=True) if x[1]["key"]["depth"]==depth-1 and (x[1]["key"]["delete"]==False or x[1]["key"]["delete"]==None)] # all graphs at lowest level
    

    return subgraphs

def cutTree(subgraph, pr): # get rid of duplicate leaves
    graphlist = [] # cut down the total number of graphs to unique ones
    n=1
    for graph in subgraph:
        if(not isinstance(graph, int)): # gets rid of unusable nodes

            f = True # bool if graph should be added to graphlist

            if(len(graphlist)==0): # adds first value to graphlist
                if(pr):
                    pos = nx.planar_layout(graph[0])
                    nx.draw(graph[0], pos=pos, with_labels=True)
                    edge_labels = nx.get_edge_attributes(graph[0], "rel")
                    nx.draw_networkx_edge_labels(graph[0], pos, edge_labels = edge_labels, label_pos=.5)
                    plt.savefig(f"images/image{n}.png", dpi=1200)
                    plt.clf()
                    n+=1
                graphlist.append(graph)
                continue # go to next graph
            
            for ref in graphlist:

                # if a graph is the same as one already in graph list, do not add it to the loop
                if [x[0] for x in sorted([x for x in graph[0].nodes(data=True)])]==[x[0] for x in sorted([x for x in ref[0].nodes(data=True)])]:
                    if (sorted([[u,v] for u,v,a in sorted([x for x in ref[0].edges(data=True)])])==sorted([[u,v] for u,v,a in sorted([x for x in graph[0].edges(data=True)])])):
                        if nx.get_edge_attributes(ref[0],"rel") == nx.get_edge_attributes(graph[0], "rel"):
                            f = False

            if(f):
                if(pr):
                    pos = nx.planar_layout(graph[0])
                    nx.draw(graph[0], pos=pos, with_labels=True)
                    edge_labels = nx.get_edge_attributes(graph[0], "rel")
                    nx.draw_networkx_edge_labels(graph[0], pos, edge_labels = edge_labels, label_pos=.5)
                    plt.savefig(f"images/image{n}.png", dpi=1200)
                    plt.clf()
                    n+=1
                graphlist.append(graph)
                
    
    if(pr):
        print(n-1, "images saved")


    return graphlist

in_sentence = input().split(" ") # manual sentence input
sentence_info = []
sentence = []

sub_pool = {
    "a":"ab",
    "e":"ex"
}
for word in in_sentence:
    for key in sub_pool.keys():
        if word == key:
            sentence.append(sub_pool[key])
            break
        else:
            sentence.append(word)
            break

for word in sentence: # create sentence_info
    sentence_info.append(getWhitakers(word))


verbs = getVerbs(sentence_info)

build_graph = initTree(verbs)

subgraphs = genTree(build_graph, sentence_info)

possibilities = cutTree(subgraphs, True)

# printDecisionGraph()
# nx.write_gexf(final, "graph.gexf")