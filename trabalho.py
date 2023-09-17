import exemplo_gerar_grafo as funcao
import time

''' Todo: Qgiz, Oeste Americano, Heuristica Harvesine, A*, DFS, Bi-Direcional '''

''' FUNÇÃO LER_GRAFO
    GRAFO -> { 1: [(2, 803), (12, 842), (1363, 2428)], 2: [(n1, ), (n2, ?), (nx, ?)], ... }
    dict key = origem 
    grafo[key] = [(destino_1, peso_1), (destino_2, peso_2), ...]
'''

''' FUNÇÃO LER_GRAFO
    ARESTAS -> [('1', '2', '803'), ('1', '12', 842'), ('1', '1363', '2428'), ...]
    Lista de tuplas com o formato (origem, destino, peso) para todas as estradas
'''

def ler_grafo(nome_arquivo): #CONCLUÍDA COM FORMATO DE RETORNO DEFINIDO ( ÍCARO )
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

#FUNÇÃO QUE MAPEIA O CAMINHO TRAÇADO
def encontrar_caminho(anteriores, origem, destino): #CONCLUÍDA MAS NÃO VERIFICADA ( ÍCARO )
    caminho = []
    no_atual = destino
    while no_atual is not None:
        caminho.append(no_atual)
        no_atual = anteriores[no_atual]
    caminho.reverse()
    return caminho

''' IGNORAR

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

def main():
    nome_arquivo = './src/newyork_roads.gr' 
    grafo, edges = ler_grafo(nome_arquivo)
    origem = 1  
    destino = 263466
    distancias, anteriores = dijkstra_comprehension(grafo, origem)

    distancia_minima = distancias[destino]
    caminho = encontrar_caminho(anteriores, origem, destino)

    print(f'Distância mínima de {origem} para {destino}: {distancia_minima}')
    print(f'Caminho: {caminho}')

    funcao.desenhar_grafo(edges[0:500])

if __name__ == "__main__":
    main()

