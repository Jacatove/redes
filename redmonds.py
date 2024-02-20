import networkx as nx
import matplotlib.pyplot as plt

# Creamos grafo
vertices = [0, 1, 2, 3, 4, 5, 6, 7]
edges = [
    (0, 1, 3),
    (0, 3, 5),
    (0, 5, 4),
    (0, 7, 3),
    (1, 3, 4),
    (2, 1, 1),
    (3, 2, 5),
    (3, 4, 3),
    (3, 6, 6),
    (4, 2, 2),
    (5, 6, 3),
    (6, 3, 8),
    (6, 4, 4),
    (6, 7, 2),
    (7, 4, 6),
    (7, 5, 3),
]
G = nx.DiGraph()
G.add_nodes_from(vertices)
G.add_weighted_edges_from(edges)

pos = nx.spring_layout(G)
edge_labels = nx.get_edge_attributes(G, 'weight')
plt.subplot(1, 2, 1)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15)
# plt.show()


def obtener_digrafo_parcial_minimo(G):
    # Asumimos que el vértice raíz está en list(G.nodes)[0]
    vertices = list(G.nodes)
    aristas_incidentes_minimas = []
    for vertice in list(G.nodes)[1:]:
        min_weight = float('inf')
        min_incidente_edge = None
        for predecessor in G.predecessors(vertice):
            edge_weight = G.get_edge_data(predecessor, vertice)['weight']
            if edge_weight < min_weight: # Si es igual pero viene de raiz, puede que se eliga mejor no?
                min_weight = edge_weight
                min_incidente_edge = predecessor

        aristas_incidentes_minimas.append((min_incidente_edge, vertice, min_weight))

    Gs = nx.DiGraph()
    Gs.add_nodes_from(vertices)
    Gs.add_weighted_edges_from(aristas_incidentes_minimas)

    return Gs

Gs = obtener_digrafo_parcial_minimo(G)

ciclos = list(nx.simple_cycles(Gs))
ciclo = set(ciclos[1])

# w = f'w{0}'
# Uw1 = set(G.nodes).difference(ciclo)

# Recorrer predecesores y sucesores de cada elemento de W
print(ciclo)

def obtener_nueva_arista_en_ciclo(G, Gs, ciclo):

    candidato = {
        'predecesor': None,
        'vertice': None,
        'predecesor_actual': None,
        'peso_adicional': float('inf'),
        'peso': float('inf'),
    }
    for vertice in ciclo:
        # por cada nodo, debemos seleccionar la menor diferencia.
        print(f'Por vertice {vertice} hallar la diferencia entre predecesor actual (i_predecesor) y otros.')
        actual_predecesor = list(Gs.predecessors(vertice))[0]
        actual_predecesor_peso = Gs.get_edge_data(actual_predecesor, vertice)['weight']
        print(f'predecesor {actual_predecesor}, peso: {actual_predecesor_peso}')
        for predecesor in G.predecessors(vertice):
            if predecesor == actual_predecesor:
                continue

            # print(predecesor, vertice, actual_predecesor, )
            peso = G.get_edge_data(predecesor, vertice)['weight']
            peso_adicional = peso - actual_predecesor_peso
            if  peso_adicional < candidato['peso_adicional']: # Podría hacerse <=. Se usa el ultimo que tenga el minimo o el primero.
                candidato['predecesor'] = predecesor
                candidato['vertice'] = vertice
                candidato['predecesor_actual'] = actual_predecesor
                candidato['peso_adicional'] = peso_adicional
                candidato['peso'] = peso

    return candidato

candidatos = []
for ciclo in ciclos:
    candidatos.append(obtener_nueva_arista_en_ciclo(G, Gs, ciclo))

for candidato in candidatos:
    Gs.remove_edge(
        candidato['predecesor_actual'],
        candidato['vertice'],
    )
    Gs.add_edge(
        candidato['predecesor'],
        candidato['vertice'],
        weight=candidato['peso'],
    )


poss = nx.spring_layout(Gs)
edge_labels_2 = nx.get_edge_attributes(Gs, 'weight')
plt.subplot(1, 2, 2)
nx.draw_networkx_edge_labels(Gs, poss, edge_labels=edge_labels_2)
nx.draw(Gs, poss, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15)

plt.tight_layout()
plt.show()
