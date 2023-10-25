import time
import math
from qgis.core import *
import qgis.utils

''' Todo: Qgiz, Oeste Americano (Teste), A* Bi-Direcional, BFS, DFS '''

''' FUNÇÃO ler_grafo
    GRAFO -> { 1: [(2, 803), (12, 842), (1363, 2428)], 2: [(n1, d1 ), (n2, d2) (nx, dx)], ... }
    dict key = origem 
    grafo[key] = [(destino_1, peso_1), (destino_2, peso_2), ...]
'''

def initialize_gqiz():
    pass

def ler_grafo_distancia(nome_arquivo): #CONCLUÍDA COM FORMATO DE RETORNO DEFINIDO ( ÍCARO )
    grafo = {}
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
    return grafo

def ler_grafo_coordenadas(nome_arquivo): #CONCLUÍDA COM FORMATO DE RETORNO DEFINIDO ( ÍCARO )
    grafo = {}
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if linha.startswith('v'): #if linha[0] == 'v'
                partes = linha.strip().split()
                origem = int(partes[1])
                latitude = int(partes[2])
                longitude = int(partes[3])
                if origem not in grafo:
                    grafo[origem] = []
                grafo[origem].append((latitude, longitude))
    return grafo

#FUNÇÃO QUE MAPEIA O CAMINHO TRAÇADO
def encontrar_caminho(anteriores, destino): #CONCLUÍDA ( ÍCARO )
    caminho = []
    no_atual = destino
    while no_atual is not None:
        caminho.append(no_atual)
        no_atual = anteriores[no_atual]
    caminho.reverse()
    return caminho

def dijkstra_comprehension(grafo, origem): #FUNCIONAL CONCLUÍDA ( ÍCARO )
    inicio = time.time()
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
        # print("fila ordenada: ", fila)
        
        distancia_atual, no_atual = fila.pop(0)
        
        if distancia_atual > distancias[no_atual]:
            continue
        
        for vizinho, distancia in grafo[no_atual]:
            distancia_total = distancia_atual + distancia

            if distancia_total < distancias[vizinho]:
                distancias[vizinho] = distancia_total
                anteriores[vizinho] = no_atual
                fila.append((distancia_total, vizinho))
    final = time.time()
    return distancias, anteriores, (final - inicio)

#Função que calcula a linha reta entre duas coordenadas (terra plana), ou seja,
#calcula a distância euclideana entre dois pontos.
def euclidean_dist(v1, v2, graph_co): #Função concluida (Carlos Gabriel)
    if v1 == v2:
        return 0.00
    lat1, long1, lat2, long2 = 0, 0, 0, 0
    for vertice, atributos in graph_co.items():
        if vertice == v1:
            # print(vertice, atributos)
            lat1 = atributos[0][0]
            long1 = atributos[0][1]
        if vertice == v2:
            lat2 = atributos[0][0]
            long2 = atributos[0][1]
        if lat1 and long1 and lat2 and long2:
            break

    # lat1, long1 = latitude e longitude do vertice de origem
    # lat2, long2 = latitude e longitude do vertice de destino

    #DIVISÃO POR 1 MILHAO
    lat1 = lat1 / 1e6
    lat2 = lat2 / 1e6
    long1 = long1 / 1e6
    long2 = long2 / 1e6
    
    #distancia = raiz(diferenças da latitude ao quadrado + diferenças da longitude ao quadrado)
    d = (((lat2 - lat1) ** 2) + ((long2 - long1) ** 2)) ** (1/2)
    return d

def haversine_dist(v1, v2, graph_co): #Função concluida (João Ícaro)
    if v1 == v2:
        return 0.00
    lat1, long1, lat2, long2 = 0, 0, 0, 0
    for vertice, atributos in graph_co.items():
        if vertice == v1:
            # print(vertice, atributos)
            lat1 = atributos[0][0]
            long1 = atributos[0][1]
        if vertice == v2:
            lat2 = atributos[0][0]
            long2 = atributos[0][1]
        if lat1 and long1 and lat2 and long2:
            break

    # lat1, long1 = latitude e longitude do vertice de origem
    # lat2, long2 = latitude e longitude do vertice de destino

    #DIVISÃO POR 1 MILHAO
    lat1 = lat1 / 1e6
    lat2 = lat2 / 1e6
    long1 = long1 / 1e6
    long2 = long2 / 1e6
    
    raio = 6371000 #raio da terra

    #converter graus decimais em radianos
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])

    # Diferenças de latitude e longitude
    dlat = lat2 - lat1
    dlon = long2 - long1

    # Fórmula de Haversine
    # a = seno da distancia das latitudes/2 elevado ao quadrado
    # somado com o cosseno de lat1 * cosseno de lat2 * seno da longitude/2 ao quadrado
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    # 2 multiplicado por arco da tangente do raiz de a pela raiz de 1 - a
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distância em metros
    distancia = raio * c

    return distancia

def manhattan_dist(v1, v2, graph_co): #Função concluida (Carlos Gabriel)
    if v1 == v2:
        return 0.00
    lat1, long1, lat2, long2 = 0, 0, 0, 0
    for vertice, atributos in graph_co.items():
        if vertice == v1:
            # print(vertice, atributos)
            lat1 = atributos[0][0]
            long1 = atributos[0][1]
        if vertice == v2:
            lat2 = atributos[0][0]
            long2 = atributos[0][1]
        if lat1 and long1 and lat2 and long2:
            break

    lat1 = lat1 / 1e6
    lat2 = lat2 / 1e6
    long1 = long1 / 1e6
    long2 = long2 / 1e6
    distx = abs(lat1 - lat2)
    disty = abs(long1 - long2)
    return 1 * (distx + disty)

def f_calc(vertice): #Função concluida (Carlos Gabriel)
    # f(n)=g(n)+h(n),
    # g(n) = custo até agora para chegar ao nó n
    # h(n) = custo estimado de n até a meta. Esta é a parte heurística da função de custo, portanto é como uma suposição.
    # f(n) = custo total estimado do caminho através do nó n
    return vertice["g"] + vertice["h"]

def a_star_search(initialVertice, finalVertice, graph, heuristica, graph_co):

    tempo_inicial = time.time()
    if heuristica == "euclidiana":
        initialVerticeDict = {
            "father": None,
            "vertice": initialVertice,
            "g": 0,
            "h": euclidean_dist(initialVertice, finalVertice, graph_co),
        }
    elif heuristica == "haversine":
        initialVerticeDict = {
            "father": None,
            "vertice": initialVertice,
            "g": 0,
            "h": haversine_dist(initialVertice, finalVertice, graph_co),
        }
    elif heuristica == "manhattan":
        initialVerticeDict = {
            "father": None,
            "vertice": initialVertice,
            "g": 0,
            "h": manhattan_dist(initialVertice, finalVertice, graph_co),
        }
    else:
        print("Heurística inválida.")
        return

    openingList = [initialVerticeDict]
    closedList = []
    contador_expansao = 0

    while openingList:
        contador_expansao += 1
        current_vertice = min(openingList, key=lambda v: f_calc(v))
        # print(f"current: {current_vertice}") #PRINT ESTILO GABRIEL

        if current_vertice["vertice"] == finalVertice:
            # O destino foi alcançado, pare o loop
            break

        openingList.remove(current_vertice)
        closedList.append(current_vertice)

        for neighbor, dist in graph[current_vertice["vertice"]]:
            neighborDict = {
                "father": current_vertice["vertice"],
                "vertice": neighbor,
                "g": current_vertice["g"] + dist,
                "h": 0,
            }

            if heuristica == "euclidiana":
                neighborDict["h"] = euclidean_dist(neighbor, finalVertice, graph_co)
            elif heuristica == "haversine":
                neighborDict["h"] = haversine_dist(neighbor, finalVertice, graph_co)
            elif heuristica == "manhattan":
                neighborDict["h"] = manhattan_dist(neighbor, finalVertice, graph_co)

            #COMENTE ISSO PARA VER SEM AS MINHAS IMPLEMENTAÇÕES (ÍCARO)

            # ATUALIZAÇÃO DE CAMINHOS E EFICIENCIA
            if neighborDict["vertice"] in [v["vertice"] for v in openingList]:
                for v in openingList:
                    if v["vertice"] == neighborDict["vertice"]:
                        if neighborDict["g"] < v["g"]:
                            v["g"] = neighborDict["g"]
                            v["father"] = current_vertice["vertice"]
            elif neighborDict["vertice"] in [v["vertice"] for v in closedList]:
                for v in closedList:
                    if v["vertice"] == neighborDict["vertice"]:
                        if neighborDict["g"] < v["g"]:
                            v["g"] = neighborDict["g"]
                            v["father"] = current_vertice["vertice"]
            else:
                openingList.append(neighborDict) #DEIDENTE ESSA PARTE SE COMENTAR

        #PRINT ESTILO ICARO (to cansado de ingles)
        # print(f"Expansão {contador_expansao}: Vertice={current_vertice['vertice']}, f={f_calc(current_vertice)}, g={current_vertice['g']}, h={current_vertice['h']}")

    #ENCONTRAR CAMINHO
    if current_vertice["vertice"] == finalVertice:
        path = []
        current = current_vertice
        while current is not None:
            path.append(current["vertice"])
            # print(path)
            current = [v for v in closedList if v["vertice"] == current["father"]][0] if current["father"] is not None else None
        # print(path)
        # print(path.reverse()) nao funciona?
        tempo_final = time.time()
        tempo = tempo_final - tempo_inicial
        print("Tempo de execução:", tempo)
        print("Caminho encontrado:", path)
    else:
        print("Caminho não encontrado.")
    
    return path, tempo, contador_expansao, neighborDict["g"]

def main():
    nome_arquivo_gr = './USA-road-d.NY.gr'  # Arquivo de distâncias
    nome_arquivo_co = './USA-road-d.NY.co'
    print("origem atual: 300")
    print("destino atual: 400")
    choose = input("Alterar origem e destino? S/N? -> ")

    origem = 300
    destino = 400

    relatorio = {
        "Dijkstra": {
            "Caminho": None,
            "Distancia": None,
            "Fator de Ramificação Médio": None,
            "Tempo": None,
        },
        "A* HAVERSINI": {
            "Caminho": None,
            "Distancia": None,
            "Fator de Ramificação Médio": None,
            "Tempo": None,
        },
        "A* EUCLIDIANO": {
            "Caminho": None,
            "Distancia": None,
            "Fator de Ramificação Médio": None,
            "Tempo": None,
        },
        "A* MANHATTAN": {
            "Caminho": None,
            "Distancia": None,
            "Fator de Ramificação Médio": None,
            "Tempo": None,
        },
        "BFS": {
            "Caminho": None,
            "Distancia": None,
            "Fator de Ramificação Médio": None,
            "Tempo": None,
        },
        "DFS": {
            "Caminho": None,
            "Distancia": None,
            "Fator de Ramificação Médio": None,
            "Tempo": None,
        }
    }

    if choose == 'S':
        origem = int(input("Origem: "))
        destino = int(input("Destino: "))
    
    while True:
        print("1 - A* com Heurística Euclidiana")
        print("2 - A* com Heurística de Haversine")
        print("3 - A* com Heurística de Manhattan")
        print("4 - Dijkstra")
        print("5 - Relatório")
        print("0 - Sair")
        
        entrada = input("Selecione o Algoritmo -> ")

        if entrada == '1':
            grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
            grafo_coordenadas = ler_grafo_coordenadas(nome_arquivo_co)
            caminho, tempo, nos_expandidos, distancia = a_star_search(origem, destino, grafo_distancias, "euclidiana", grafo_coordenadas)
            relatorio["A* EUCLIDIANO"]["Caminho"] = caminho
            relatorio["A* EUCLIDIANO"]["Distancia"] = distancia
            relatorio["A* EUCLIDIANO"]["Fator de Ramificação Médio"] = nos_expandidos
            relatorio["A* EUCLIDIANO"]["Tempo"] = tempo

        elif entrada == '2':
            grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
            grafo_coordenadas = ler_grafo_coordenadas(nome_arquivo_co)
            caminho, tempo, nos_expandidos, distancia = a_star_search(origem, destino, grafo_distancias,"haversine", grafo_coordenadas)
            relatorio["A* HAVERSINI"]["Caminho"] = caminho
            relatorio["A* HAVERSINI"]["Distancia"] = distancia
            relatorio["A* HAVERSINI"]["Fator de Ramificação Médio"] = nos_expandidos
            relatorio["A* HAVERSINI"]["Tempo"] = tempo
        elif entrada == '3':
            grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
            grafo_coordenadas = ler_grafo_coordenadas(nome_arquivo_co)
            caminho, tempo, nos_expandidos, distancia = a_star_search(origem, destino, grafo_distancias,"manhattan", grafo_coordenadas)
            relatorio["A* MANHATTAN"]["Caminho"] = caminho
            relatorio["A* MANHATTAN"]["Distancia"] = distancia
            relatorio["A* MANHATTAN"]["Fator de Ramificação Médio"] = nos_expandidos
            relatorio["A* MANHATTAN"]["Tempo"] = tempo
        elif entrada == '4':
            grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
            distancias, anteriores, tempo = dijkstra_comprehension(grafo_distancias, origem)
            distancia_minima = distancias[destino]
            caminho = encontrar_caminho(anteriores, destino)
            print("caminho encontrado: ", caminho)
            print("distancia minima: ", distancia_minima)
            relatorio["Dijkstra"]["Caminho"] = caminho
            relatorio["Dijkstra"]["Distancia"] = distancia_minima
            relatorio["Dijkstra"]["Tempo"] = tempo

        elif entrada == "5":
            print("\nRELATÓRIO\n")
            for i, j in relatorio.items():
                print(f"{i}:")
                for cateogory, item in j.items():
                    print(f"{cateogory} - {item}")
                print("\n")

        elif entrada == '0':
            break
        else:
            print("Opção Inválida!")

if __name__ == "__main__":
    main()