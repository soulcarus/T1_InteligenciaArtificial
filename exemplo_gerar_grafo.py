import networkx as nx
import matplotlib.pyplot as plt

def desenhar_grafo(edges):
    # Criar um objeto de grafo direcionado
    G = nx.DiGraph()

    # Adicionar arestas com origem, destino e peso
    # edges = [("1", "2", 803), ("2", "1", 803), ("3", "4", 158), ("4", "3", 158)]

    for edge in edges:
        source, target, weight = edge
        G.add_edge(source, target, weight=weight)

    # Posições dos nós no gráfico
    pos = nx.spring_layout(G)

    # Obter pesos das arestas
    edge_labels = {(source, target): weight for source, target, weight in edges}

    # Plotar o grafo
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_color='red')
    plt.title("Mapa do Grafo")
    plt.show()
