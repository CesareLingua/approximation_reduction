import networkx as nx
from networkx.algorithms.approximation import vertex_cover
import matplotlib.pyplot as plt
import random
import warnings
import itertools
import _thread
MAX_WEIGHT = 4
MAX_NODE = 10
PROB_EDGE = 0.3

def createGraph(numNode, maxWeight):
    if numNode > MAX_NODE:
        warnings.warn("numNode too big!!")
        numNode = MAX_NODE
    if maxWeight > MAX_WEIGHT:
        warnings.warn("maxWeight too big!!")
        maxWeight = MAX_WEIGHT

    G = nx.erdos_renyi_graph(numNode, PROB_EDGE)
    mapping=dict(zip(G.nodes(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    G = nx.relabel_nodes(G,mapping)
    wDic = {}
    for n in G.nodes():
        wDic.update({n: random.randint(1,maxWeight)})

    nx.set_node_attributes(G, wDic, 'w')
    return G

def drawGraph(G1, G2, sol1, sol2):
    d = {}
    d1 = {}
    color = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
    for n in G1.nodes(data=True):
        d.update({n[0]:n[0]+','+str(n[1]['w'])})
    warnings.filterwarnings("ignore", category=UserWarning)
    f1 = plt.figure(1)
    f1.canvas.set_window_title('MIN WHEIGHTED VERTEX COVER')
    pos = nx.circular_layout(G1)
    # pos = nx.shell_layout(G1)
    # pos = nx.random_layout(G1)
    # pos = nx.spring_layout(G1)
    # pos = nx.spectral_layout(G1)
    nx.draw_networkx_nodes(G1, pos, node_color=color[:len(G1.nodes)])
    nx.draw_networkx_nodes(G1,pos,nodelist=sol1,node_color='r', node_shape=".")
    nx.draw_networkx_labels(G1, pos, d, font_color='w', font_size=9)
    nx.draw_networkx_labels(G1, pos, d, nodelist=sol1, font_color='w', font_size=9)
    nx.draw_networkx_edges(G1, pos)

    for n in G2.nodes(data=True):
        d1.update({n[0]:n[0]})
    warnings.filterwarnings("ignore", category=UserWarning)
    f2 = plt.figure(2)
    f2.canvas.set_window_title('MIN VERTEX COVER')
    pos = nx.circular_layout(G2)
    # pos = nx.shell_layout(G2)
    # pos = nx.random_layout(G2)
    # pos = nx.spring_layout(G2)
    # pos = nx.spectral_layout(G2)


    tmp = ""
    index = -1
    colormap = []
    for n  in G2.nodes():
        if n[0] != tmp:
            tmp = n[0]
            index += 1
        colormap.append(color[index])

    nx.draw_networkx_nodes(G2, pos, node_color=colormap)
    nx.draw_networkx_nodes(G2,pos,nodelist=sol2, node_color="r", node_shape=".")
    nx.draw_networkx_labels(G2, pos, d1, font_color='w', font_size=9)
    nx.draw_networkx_labels(G2, pos, d1, nodelist=sol2, font_color='w', font_size=9)
    nx.draw_networkx_edges(G2, pos, width=0.7)

    plt.show()

def getGroupNodes(G, w):
    W = []
    for n in G.nodes(data=True):
        if n[1]['w'] == w:
            W.append(n[0])
    return W

def f(G):
    newG = nx.Graph()
    for n in G.nodes(data=True):
        w = n[1]['w']
        for i in range(0, w):
            newG.add_node(str(n[0])+'_'+str(i), w=n[0])

    for e in G.edges():
        s = getGroupNodes(newG, e[0])
        d = getGroupNodes(newG, e[1])
        edges = list(itertools.product(s, d))
        newG.add_edges_from(edges)
    return newG

def getPermutations(G):
    n = len(G.nodes())
    permutations = list()
    for disp in itertools.product(*["01"] * n):
        row = list()
        for i, node in enumerate(G.nodes()):
            if int(disp[i]) == 1:
                row.append(node)

        permutations.append(row)
    return permutations

def isCover(G, c):
    is_cover = True
    for e in G.edges():
        if not (set(e) & set(c)):
            is_cover = False

    return is_cover
def solve(G):
    min_num_cover = len(G.nodes())
    min_cover = []
    all_permutations = getPermutations(G)

    for c in all_permutations:
        if isCover(G, c):
            if len(c) < min_num_cover:
                min_num_cover = len(c)
                min_cover = c
    return min_cover

def mapReducedSolution(sol):
    map_sol = set()
    for n in sol:
        map_sol.add(n[0])

    return map_sol

G = createGraph(5, 3)
reducedG = f(G)
reducedSolution = solve(reducedG)
print("Soluzione del grafo ridotto: \n\t", reducedSolution)
solution = mapReducedSolution(reducedSolution)
print("Soluzione del grafo di partenza: \n\t", solution)
drawGraph(G, reducedG, solution, reducedSolution)
