import networkx as nx
import matplotlib.pyplot as plt


vertices = [0, 1, 2, 3, 4, 5, 6, 7]
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
Vs = []
Us = []
Ds = []
s = 0



G = nx.DiGraph()
G.add_nodes_from(vertices)
G.add_weighted_edges_from(edges)

pos = nx.spring_layout(G)
edge_labels = nx.get_edge_attributes(G, 'weight')
plt.subplot(1, 4, 1)
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

plt.subplot(1, 4, 2)
pos = nx.spring_layout(Gs)
nx.draw_networkx_edge_labels(Gs, pos, edge_labels=nx.get_edge_attributes(Gs, 'weight'))
nx.draw(Gs, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15)



ciclos = list(nx.simple_cycles(Gs))

# w = f'w{0}'
# Uw1 = set(G.nodes).difference(ciclo)

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
ciclo = ciclos[0]
candidato = obtener_nueva_arista_en_ciclo(G, Gs, ciclo)

Gw = []
Gw0_base = []
Gw0_predecesores = []
Gw0_sucesores = []

aristas = list(G.edges)
vertice_contraido = 'w0'
for arista in aristas:
    extremo_inicial = arista[0]
    extremo_final = arista[1]
    peso_arista = G.get_edge_data(extremo_inicial, extremo_final)['weight']

    if extremo_inicial not in ciclo and extremo_final not in ciclo:
        Gw0_base.append(
            (
                extremo_inicial,
                extremo_final,
                peso_arista,
                # True, # Depronto me sirva para indicar que es original.
            ),
        )
    elif extremo_inicial in ciclo and extremo_final not in ciclo:
        Gw0_predecesores.append(
            (
                vertice_contraido,
                extremo_final,
                peso_arista,
                # True, # Depronto me sirva para indicar que es original.
            ),
        )
    elif extremo_inicial not in ciclo and extremo_final in ciclo:

        actual_predecesor = list(Gs.predecessors(extremo_final))[0] # En el ciclo solo hay una arista incidente
        peso_arista_incidente = G.get_edge_data(actual_predecesor, extremo_final)['weight']
        print('ei, ef')
        print(extremo_inicial, extremo_final)
        print(actual_predecesor)
        print(actual_predecesor)

        Gw0_sucesores.append(
            (
                extremo_inicial,
                vertice_contraido,
                peso_arista - peso_arista_incidente,
                # False,
            ),
        )

Gw = Gw0_base + Gw0_predecesores + Gw0_sucesores


Gss = nx.DiGraph()
Gss.add_nodes_from((set(vertices).difference(ciclo)).union({'w0'}))
Gss.add_weighted_edges_from(Gw)


plt.subplot(1, 4, 3)
pos = nx.spring_layout(Gss)
nx.draw_networkx_edge_labels(Gss, pos, edge_labels=nx.get_edge_attributes(Gss, 'weight'))
nx.draw(Gss, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15)




plt.subplot(1, 4, 4)
Gsss = obtener_digrafo_parcial_minimo(Gss)
pos = nx.spring_layout(Gsss)
nx.draw_networkx_edge_labels(Gsss, pos, edge_labels=nx.get_edge_attributes(Gsss, 'weight'))
nx.draw(Gsss, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='k', linewidths=1, font_size=15)

plt.tight_layout()
plt.show()