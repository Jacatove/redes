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