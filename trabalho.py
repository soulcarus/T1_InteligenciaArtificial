import exemplo_gerar_grafo as funcao
import time

# qg
# oeste americano

def ler_grafo(nome_arquivo):
    grafo = {}
    arestas = []
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if linha.startswith('a'): # if linha[0] == 'a'
                partes = linha.strip().split() # dividir linha
                origem = int(partes[1])
                destino = int(partes[2])
                distancia = int(partes[3])
                if origem not in grafo:
                    grafo[origem] = []
                grafo[origem].append((destino, distancia))
                arestas.append((str(origem), str(destino), distancia))
    return grafo, arestas

#TESTE

def encontrar_caminho(anteriores, origem, destino):
    caminho = []
    no_atual = destino
    while no_atual is not None:
        caminho.append(no_atual)
        no_atual = anteriores[no_atual]
    caminho.reverse()
    return caminho


'''
def ler_grafo_para_plotar(nome_arquivo):
    arestas = []
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if linha.startswith('a'):
                partes = linha.strip().split()
                no_origem = partes[1]
                no_destino = partes[2]
                tamanho_aresta = int(partes[3])
                arestas.append((no_origem, no_destino, tamanho_aresta))
    return arestas
'''

def dijkstra_comprehension(grafo, origem):
    #definir todos os nós para infinito
    distancias = {no: float('inf') for no in grafo} 
    #definir todos os nós anteriores como nulo
    anteriores = {no: None for no in grafo}
    #a distancia da origem é 0
    distancias[origem] = 0
    #a fila vai de 0 até a origem (0)
    fila = [(0, origem)]

    #enquanto a fila nao estiver vazia, iremos extrair o nó com menor distância
    while fila:
        #ordene-a
        fila.sort()
        
        distancia_atual, no_atual = fila.pop(0)
        
        if distancia_atual > distancias[no_atual]:
            continue

        for vizinho, distancia in grafo[no_atual]:
            distancia_total = distancia_atual + distancia

            if distancia_total < distancias[vizinho]:
                distancias[vizinho] = distancia_total
                anteriores[vizinho] = no_atual
                fila.append((distancia_total, vizinho))

    return distancias, anteriores


'''
funcao dijkstra(graph, source)

criar vertex set Q

para cada vertex v em graph:
    distancia[v] <- infinito
    anterior[v] <- indefinido
    adicionar v para Q
distancia[source] <- 0

enquanto Q não estiver vazia faça
    u <- vertex in Q com minima distancia[u]
    
    remover u de Q

    para cada vizinho v de u:
        alt <- distancia[u] + tamanho( u, v)
        se alt < distancia[v]:
            distancia[v] <- alt
            anterior[v] <- u

retorne distancia[], anterior[]
'''

'''
def dijkstra(G, startingNode):
	visited = set()
	parentsMap = {}
	pq = []
	nodeCosts = defaultdict(lambda: float('inf'))
	nodeCosts[startingNode] = 0
	heap.heappush(pq, (0, startingNode))
 
	while pq:
		# go greedily by always extending the shorter cost nodes first
		_, node = heap.heappop(pq)
		visited.add(node)
 
		for adjNode, weight in G[node].items():
			if adjNode in visited:	continue
				
			newCost = nodeCosts[node] + weight
			if nodeCosts[adjNode] > newCost:
				parentsMap[adjNode] = node
				nodeCosts[adjNode] = newCost
				heap.heappush(pq, (newCost, adjNode))
        
	return parentsMap, nodeCosts
'''

def main():
    nome_arquivo = 'newyork_roads.gr' 
    grafo, edges = ler_grafo(nome_arquivo)
    origem = 1  
    destino = 263466
    distancias, anteriores = dijkstra_comprehension(grafo, origem)

    distancia_minima = distancias[destino]
    caminho = encontrar_caminho(anteriores, origem, destino)

    print(f'Distância mínima de {origem} para {destino}: {distancia_minima}')
    print(f'Caminho: {caminho}')

    funcao.desenhar_grafo(edges[0:500])

# arvesini

if __name__ == "__main__":
    main()