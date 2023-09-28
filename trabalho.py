import exemplo_gerar_grafo as funcao
import time

''' Todo: Qgiz, Oeste Americano, Heuristica Haversine, A*, DFS, Bi-Direcional '''

''' FUNÇÃO ler_grafo_arcos
    GRAFO -> { 1: [(2, 803), (12, 842), (1363, 2428)], 2: [(n1, ), (n2, ?), (nx, ?)], ... }
    dict key = origem 
    grafo[key] = [(destino_1, peso_1), (destino_2, peso_2), ...]
'''

''' FUNÇÃO ler_grafo_arcos
    ARESTAS -> [('1', '2', '803'), ('1', '12', 842'), ('1', '1363', '2428'), ...]
    Lista de tuplas com o formato (origem, destino, peso) para todas as estradas
'''

def ler_grafo_arcos(nome_arquivo): #CONCLUÍDA COM FORMATO DE RETORNO DEFINIDO ( ÍCARO )
    grafo = {}
    arestas = []
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if linha.startswith('a'): #if linha[0] == 'a'
                partes = linha.strip().split()
                origem = int(partes[1])
                destino = int(partes[2])
                distancia = int(partes[3])
                if origem not in grafo:
                    grafo[origem] = []
                grafo[origem].append((destino, distancia))
                arestas.append((str(origem), str(destino), distancia))
    # print(arestas) #teste
    # print(grafo) #teste
    return grafo, arestas

def ler_grafo_coordenadas(nome_arquivo):
    grafo = {}
    coordenadas = []
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if linha.startswith('v'):
                partes = linha.strip().split()
                no = int(partes[1])
                x = int(partes[2])
                y = int(partes[3])
                if no not in grafo:
                    grafo[no] = []
                coordenadas.append((no, x, y))
    return grafo, coordenadas


#FUNÇÃO QUE MAPEIA O CAMINHO TRAÇADO
def encontrar_caminho(anteriores, origem, destino): #CONCLUÍDA MAS NÃO VERIFICADA ( ÍCARO )
    caminho = []
    no_atual = destino
    while no_atual is not None:
        caminho.append(no_atual)
        no_atual = anteriores[no_atual]
    caminho.reverse()
    return caminho

def dijkstra_comprehension(grafo, origem): #FUNCIONAL CONCLUÍDA ( ÍCARO )
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

#Função que calcula a linha reta entre duas coordenadas (terra plana), ou seja,
#calcula a distância euclideana entre dois pontos.
def euclidean_dist(v1, v2): #Função concluida (Carlos Gabriel)
    if v1 == v2:
        return 0.00
    coord1x, coord1y, coord2x, coord2y = 0, 0, 0, 0
    with open('USA-road-d.NY.co', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(f"v {v1}"):
                parts = line.strip().split()
                coord1x = int(parts[2])
                coord1y = int(parts[3])
            if line.startswith(f"v {v2}"):
                parts = line.strip().split()
                coord2x = int(parts[2])
                coord2y = int(parts[3])
    d = (((coord2x - coord1x) ** 2) + ((coord2y - coord1y) ** 2)) ** (1/2)
    return d

def f_calc(vertice): #Função concluida (Carlos Gabriel)
    # f(n)=g(n)+h(n),
    # f(n) = custo total estimado do caminho através do nó n
    # g(n) = custo até agora para chegar ao nó n
    # h(n) = custo estimado de n até a meta. Esta é a parte heurística da função de custo, portanto é como uma suposição.
    return vertice["g"] + vertice["h"]

def a_star_search(initialVertice, finalVertice, graph):
    initialVerticeDict = {
        "father": None,
        "vertice": initialVertice,
        "g": 0,
        "h": euclidean_dist(initialVertice, finalVertice),
    }
    openingList = [initialVerticeDict]
    closedList = []
    while (True):
        if (len(openingList) == 0):
            print("Sem solução")
            break
        current_vertice = min(openingList, key=lambda v: f_calc(v))
        print(f"current: {current_vertice}")
        if current_vertice["vertice"] == finalVertice:
            print(current_vertice["vertice"])
            break
        else:
            openingList.remove(current_vertice)
            closedList.append(current_vertice)
            for neighbor, dist in graph[current_vertice["vertice"]]:
                print(f"visinho: {neighbor}, dist: {dist}")
                neighborDict = {
                    "father": current_vertice["vertice"],
                    "vertice": neighbor,
                    "g": current_vertice["g"] + dist,
                    "h": euclidean_dist(neighbor, finalVertice),
                }
                openingList.append(neighborDict)
    #           if (vizinho tem valor g menor que o atual e está na lista fechada):
    #               substitua o vizinho pelo novo valor g inferior
    #               o nó atual agora é o pai do vizinho
    #           else if (o valor atual de g é menor e este vizinho está na lista aberta):
    #               substitua o vizinho pelo novo valor g inferior
    #               mude o pai do vizinho para o nosso nó atual
    #           else if este vizinho is not in ambas as listas:
    #               adicione-o à lista aberta e defina seu g

def main():
    nome_arquivo = 'USA-road-d.NY.co'
    grafo, edges = ler_grafo_arcos(nome_arquivo)
    # origem = 1  
    # destino = 1356
    # distancias, anteriores = dijkstra_comprehension(grafo, origem)

    # distancia_minima = distancias[destino]
    # caminho = encontrar_caminho(anteriores, origem, destino)

    # print(f'Distância mínima de {origem} para {destino}: {distancia_minima}')
    # print(f'Caminho: {caminho}')
    
    # print(euclidean_dist(206203, 206204))
    a_star_search(206198, 206207, grafo)

    # funcao.desenhar_grafo(edges[0:500])

if __name__ == "__main__":
    main()

