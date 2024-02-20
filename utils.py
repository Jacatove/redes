import networkx as nx


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


def contraer(G, Gs, ciclo):
    """
    G grafo papa
    W ciclo
    """
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
                ),
            )
        elif extremo_inicial in ciclo and extremo_final not in ciclo:
            Gw0_predecesores.append(
                (
                    vertice_contraido,
                    extremo_final,
                    peso_arista,
                ),
            )
        elif extremo_inicial not in ciclo and extremo_final in ciclo:

            actual_predecesor = list(Gs.predecessors(extremo_final))[0] # En el ciclo solo hay una arista incidente
            peso_arista_incidente = G.get_edge_data(actual_predecesor, extremo_final)['weight']

            Gw0_sucesores.append(
                (
                    extremo_inicial,
                    vertice_contraido,
                    peso_arista - peso_arista_incidente,
                ),
            )

    Gw = Gw0_base + Gw0_predecesores
    Gw.append(
        min(Gw0_sucesores, key=lambda x: x[2])
    )

    Gss = nx.DiGraph()
    Gss.add_nodes_from((set(G.nodes).difference(ciclo)).union({'w0'}))
    Gss.add_weighted_edges_from(Gw)

    return Gss
