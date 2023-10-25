import time
import math

''' Todo: Qgiz, Oeste Americano, Heuristica Haversine, A*, DFS, Bi-Direcional '''

''' FUNÇÃO ler_grafo
    GRAFO -> { 1: [(2, 803), (12, 842), (1363, 2428)], 2: [(n1, ), (n2, ?), (nx, ?)], ... }
    dict key = origem 
    grafo[key] = [(destino_1, peso_1), (destino_2, peso_2), ...]
'''

''' FUNÇÃO ler_grafo
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

def BFS_search(initialVertice, finalVertice, graph):
    
    tempo_inicial = time.time()                    
    no_expands=0                                   #nós expandidos
    edges_expands=0                                #arestas geradas
    caminho = []                                   #lista com o caminho do no inicial ao no final
    fim =0                                         #variavel pra cheacr fim da repetição
    queue = []                                     #fila
    dados = {}                                     #Dicionario na forma {id: [pai, distancia de arestas, distancia em KM, cor]}
    for v in graph:                                #inicia os vetores
        dados[v]=[-1,0,0,"W"]
    dados[initialVertice] = [-1,0,0,'G']
    
    
    queue.append(initialVertice)                   #coloca o primeiro vertice na fila
    while(len(queue) > 0):                         #BFS
        id = queue[0]
        no_expands = no_expands+1
        for v in graph[id]:
            edges_expands = edges_expands+1
            new_id = v[0]
            if dados[new_id][3] == 'W':
                dados[new_id][0] = id
                dados[new_id][1] = dados[id][1]+1
                dados[new_id][2] = dados[id][2] + v[1]
                dados[new_id][3] = 'G'
                queue.append(new_id)
            if new_id == finalVertice:
                print("Vertice encontrado!")
                id = new_id
                queue.clear()
                fim = 1
            if(fim):
                break
        if(fim):
            break
        queue.remove(id)
        dados[id][3]='B'
        
    while(dados[id][1]>0):
        caminho.append(id)  
        id=dados[id][0]
    caminho.append(id)
        
    while(len(caminho) != 0):
        print(" -> ", caminho[-1], end = "")
        caminho.remove(caminho[-1])
            
            
    tempo_final = time.time()    
    tempo = tempo_final - tempo_inicial
    ramificacao = edges_expands//no_expands
    
    return dados[new_id][2], ramificacao, tempo, no_expands

def main():
    nome_arquivo = 'USA-road-d.NY.gr'
    print("origem atual: 206198")
    print("destino atual: 206207")
    choose = input("alterar origem e destino? S/N? -> ")

    origem = 206198
    destino = 206207

    if choose == 'S':
        origem = int(input("Origem: "))
        destino = int(input("Destino: "))

    grafo, edges = ler_grafo(nome_arquivo)

    while True:
        print("1 - A*")
        print("2 - Dijkstra")
        print("3 - BFS")
        print("0 - Sair")
        
        entrada = input("Selecione o Algoritmo -> ")

        if entrada == '1':
            a_star_search(origem, destino, grafo)

        elif entrada == '2':
            
            distancias, anteriores = dijkstra_comprehension(grafo, origem)
            distancia_minima = distancias[destino]
            caminho = encontrar_caminho(anteriores, origem, destino)
            print(f'Distância mínima de {origem} para {destino}: {distancia_minima}')
            print(f'Caminho: {caminho}')
        elif entrada == '3':
            distancia, ramos, time, no = BFS_search(origem,destino,grafo)
            print("\ndistancia: ",distancia)
            print("\nfator de ramifaicacao= ",ramos)
            print("\ntempo deceorrido =", time)
            print("\nqtd de nós expandidos:", no)
        elif entrada == "4":
            #DFS_search(origem, destino, grafo,)
            pass
        elif entrada == '0':
            break
        else:
            print("Opção Inválida!")


if __name__ == "__main__":
    main()

