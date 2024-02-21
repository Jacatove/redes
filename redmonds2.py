import networkx as nx
import matplotlib.pyplot as plt

from utils import obtener_digrafo_parcial_minimo, contraer

nodes = [0, 1, 2, 3, 4, 5, 6, 7]
edges = [
    (0, 1, 3),

    (1, 3, 1),
    (2, 1, 1),
    (3, 2, 1),
    (3, 4, 1),

    (4, 5, 2),

    (5, 6, 1),
    (7, 5, 1),
    (6, 7, 1),
    (6, 1, 2),
]

# Creamos grafo
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

Gs = [G]
Hs = []
s = 0
while True:

    H = obtener_digrafo_parcial_minimo(Gs[-1])
    Hs.append(H)

    ciclos = list(nx.simple_cycles(H))

    if ciclos:
        Gss = contraer(Gs[-1], H, ciclos[0], s)
        Gs.append(Gss)
        s += 1
        continue

    print('NO MORE CICLOS BITCH')
    break

pos = nx.spring_layout(Gs[-1])
nx.draw_networkx_edge_labels(Gs[-1], pos, edge_labels=nx.get_edge_attributes(Gs[-1], 'weight'))
nx.draw(Gs[-1], pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15)

plt.tight_layout()
plt.show()