import time
import math
from functools import cache
import pandas as pd
import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, Point
import criar_csv
import psutil
import random
import os

global caminho

pathTraveledGoing = []
pathTraveledReturning = []

def gerar_shapefile(caminhos):
    grafo_coordenadas = ler_grafo_coordenadas("./USA-road-d.W.co")
    coordenadas = []
    for i, j in grafo_coordenadas.items():
        if i in caminhos:
            coordenadas.append(j[0])
    
    g = [Point(long, lat) for lat, long in coordenadas]
    # g = [LineString(coordenadas[i:i+2]) for i in range(len(coordenadas) - 1)]
    df = gpd.GeoDataFrame(geometry=g)

    df.to_file("caminho.shp")

def ler_grafo_distancia(nome_arquivo): #CONCLUÍDA COM FORMATO DE RETORNO DEFINIDO ( ÍCARO )
    grafo = {}
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        linhas = linhas[7:]
        for linha in linhas:
            partes = linha.split()
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
        linhas = linhas[7:]
        for linha in linhas:
            partes = linha.split()
            origem = int(partes[1])
            latitude = int(partes[2])
            longitude = int(partes[3])
            if origem not in grafo:
                grafo[origem] = []
            grafo[origem].append((latitude, longitude))
    return grafo



#FUNÇÃO QUE MAPEIA O CAMINHO TRAÇADO
def encontrar_caminho(anteriores, destino): #FUNÇÃO CONCLUÍDA ( ÍCARO )
    caminho = []
    no_atual = destino
    while no_atual is not None:
        caminho.append(no_atual)
        no_atual = anteriores[no_atual]
    caminho.reverse()
    return caminho


def dijkstra_comprehension(grafo, origem): #FUNÇÃO CONCLUÍDA ( ÍCARO )
    inicio = time.time()
    #definir todos os nós para infinito
    distancias = {no: float('inf') for no in grafo}
    print('distancias ok')
    #definir todos os nós anteriores como nulo
    anteriores = {no: None for no in grafo}
    print('anteriores ok')
    #a distancia da origem é 0
    distancias[origem] = 0
    #a fila vai de 0 até a origem (0)
    fila = [(0, origem)]
    #enquanto a fila nao estiver vazia, iremos extrair o nó com menor distância
    contador = 0
    while fila:
        #ordene-a
        fila.sort()
        # print(fila)
        # print("fila ordenada: ", fila)
        
        distancia_atual, no_atual = fila.pop(0)
        
        if distancia_atual > distancias[no_atual]:
            continue

        contador += 1
        
        for vizinho, distancia in grafo[no_atual]:
            # print(grafo[no_atual])
            distancia_total = distancia_atual + distancia

            if distancia_total < distancias[vizinho]:
                distancias[vizinho] = distancia_total
                anteriores[vizinho] = no_atual
                fila.append((distancia_total, vizinho))

    final = time.time()
    return distancias, anteriores, (final - inicio), contador

#Função que calcula a linha reta entre duas coordenadas (terra plana), ou seja,
#calcula a distância euclideana entre dois pontos.
def euclidean_dist(v1, v2, graph_co): #Função concluida (Carlos Gabriel)
    if v1 == v2:
        return 0.00

    atributos = graph_co.get(v1)
    atributos_2 = graph_co.get(v2)

    lat1 = atributos[0][0]
    long1 = atributos[0][1]
    lat2 = atributos_2[0][0]
    long2 = atributos_2[0][1]

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
    atributos = graph_co.get(v1)
    atributos_2 = graph_co.get(v2)

    lat1 = atributos[0][0]
    long1 = atributos[0][1]
    lat2 = atributos_2[0][0]
    long2 = atributos_2[0][1]

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
    atributos = graph_co.get(v1)
    atributos_2 = graph_co.get(v2)

    lat1 = atributos[0][0]
    long1 = atributos[0][1]
    lat2 = atributos_2[0][0]
    long2 = atributos_2[0][1]

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
        # time.sleep(1.5)

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
    
    return path, tempo, contador_expansao, current_vertice["g"]

def BFS_search(initialVertice, finalVertice, graph): #FEITA POR DEOCLÉCIO, CONCLUÍDA POR ÍCARO
    
    tempo_inicial = time.time()
    #nós expandidos
    no_expands=0
    #arestas geradas
    edges_expands=0
    #lista com o caminho do no inicial ao no final
    caminho = []
    #variavel pra cheacr fim da repetição
    fim =0
    
    
    #fila
    queue = []
    #Dicionario na forma {id: [pai, distancia de arestas, distancia em KM, cor]}
    dados = {}
    #inicia os vetores
    for v in graph:
        dados[v]=[-1,0,0,"W"]
    dados[initialVertice] = [-1,0,0,'G']
    
    #coloca o primeiro vertice na fila
    queue.append(initialVertice)
    
    while(len(queue) > 0):
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
        
    print(caminho)
            
            
    tempo_final = time.time()    
    tempo = tempo_final - tempo_inicial
    ramificacao = edges_expands//no_expands
    distancia = dados[new_id][2]
    
    return distancia, tempo, no_expands, caminho

def DFS_search(initialVertice, finalVertice, graph): #FEITA POR DEOCLÉCIO, CONCLUÍDA POR ÍCARO

    tempo_inicial = time.time()
    no_expands=0            #nós expandidos
    edges_expands=0         #arestas geradas
    caminho = []            #lista com o caminho do no inicial ao no final
    fim =0                  #variavel pra cheacr fim da repetição
    pilha = []


    #Dicionario na forma {id: [pai, tempo de chegada, tempo final, distancia em KM, cor]}
    dados = {}
    #inicia os vetores
    for v in graph:
        dados[v]=[-1,0,0,0,"W"]
    dados[initialVertice] = [-1,1,0,0,'G']
    pilha.append(initialVertice) 
    tempo = 1

    while(len(pilha)):
        id = pilha[-1]
        for v in graph[id]:
            new_id = v[0]
            if new_id in pilha:
                continue
            if dados[new_id][4] == 'W':
                tempo = tempo + 1
                edges_expands = edges_expands+1
                dados[new_id][0] = id
                dados[new_id][1] = tempo
                dados[new_id][3] = dados[id][3] + v[1]
                dados[new_id][4] = 'G'
                pilha.append(new_id)
                if new_id == finalVertice:
                    print("Vertice encontrado!")
                    id = new_id
                    fim = 1
                break
            if(fim):
                break
        if(fim):
            break
        if(id == pilha[-1]):
            dados[id][2]=tempo
            dados[id][4]='B'
            pilha.remove(id)
            no_expands = no_expands+1

    while(len(pilha)>1):
        pilha.remove(pilha[-1])
        no_expands = no_expands+1

    while(dados[id][0]>0):
        caminho.append(id)  
        id=dados[id][0]
    caminho.append(id)

    tempo_final = time.time()    
    tempo = tempo_final - tempo_inicial
    ramificacao = edges_expands//no_expands
    print(edges_expands)
    print(no_expands)

    distancia = dados[new_id][3]

    return distancia, tempo, no_expands, caminho

#CAMINHOS DE TESTE:

caminhos = [(1, 33),
            (9, 3),
            (4, 15),
            (9, 598),
            (3165, 3211),
            (3142, 1461),
            (1177, 1355),
            (3864, 1280),
            (598, 603),
            (1178, 3180),
            (1461, 1373),
            (15, 4),
            (4887, 1729),
            (1965, 1997),
            (2022, 1249),
            (4755, 4723),
            (2029, 1673),
            (990, 964),
            (1, 64),
            (1273, 1),
            (979, 955),
            (1235, 1276),
            (2445, 64),
            (977, 2338), 
            (1000, 5412), 
            (979, 1585), 
            (990, 2340), 
            (962, 1675), 
            (1255, 1729), 
            (987, 1584), 
            (963, 1817), 
            (991, 1688), 
            (1259, 1874), 
            (1253, 1813), 
            (1259, 2022), 
            (1273, 4926), 
            (990, 2340), 
            (1253, 2334), 
            (1260, 5411), 
            (990, 2027), 
            (1283, 5411), 
            (987, 1634), 
            (13754, 1049281), 
            (979, 2338), 
            (1253, 1729), 
            (1260, 2027), 
            (1273, 2333), 
            (13830, 13827), 
            (1282, 1729), 
            (707, 723), 
            (33, 704),
            ]

def main():
    print("ESCOLHA UM MAPA (obs: coloque o arquivo na pasta)")
    print("1 - NEW YORK")
    print("2 - LESTE")
    print("3 - OESTE")
    print("4 - ESTADOS UNIDOS INTEIRO")
    escolha = input("MAPA -> ")
    if escolha == "1":
        nome_arquivo_gr = './USA-road-d.NY.gr'
        nome_arquivo_co = './USA-road-d.NY.co'
    elif escolha == "3":
        nome_arquivo_gr = './USA-road-d.W.gr'  # Arquivo de distâncias
        nome_arquivo_co = './USA-road-d.W.co'  # Arquivo de coordenadas
    elif escolha == "4":
        nome_arquivo_gr = './USA-road-d.USA.gr'
        nome_arquivo_co = './USA-road-d.USA.co'
    elif escolha == "2":
        nome_arquivo_gr = './USA-road-d.E.gr'
        nome_arquivo_co = './USA-road-d.E.co'
    else:
        nome_arquivo_gr = './USA-road-d.NY.gr'
        nome_arquivo_co = './USA-road-d.NY.co'

    print('\nlendo arquivo de distancias...')
    grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
    print('lendo arquivo de coordenadas...')
    grafo_coordenadas = ler_grafo_coordenadas(nome_arquivo_co)
    print("\norigem atual: 1")
    print("destino atual: 33")
    choose = input("Alterar origem e destino? S/N? -> ")

    origem = 1
    destino = 33

    relatorio = {
        "Dijkstra": {
            "Caminho": None,
            "Distancia": None,
            "Nós Expandidos": None,
            "Tempo": None,
            "Fator de Ramificação Médio": None
        },
        "A* HAVERSINI": {
            "Caminho": None,
            "Distancia": None,
            "Nós Expandidos": None,
            "Tempo": None,
            "Fator de Ramificação Médio": None
        },
        "A* EUCLIDIANO": {
            "Caminho": None,
            "Distancia": None,
            "Nós Expandidos": None,
            "Tempo": None,
            "Fator de Ramificação Médio": None
        },
        "A* MANHATTAN": {
            "Caminho": None,
            "Distancia": None,
            "Nós Expandidos": None,
            "Tempo": None,
            "Fator de Ramificação Médio": None
        },
        "BFS": {
            "Caminho": None,
            "Distancia": None,
            "Nós Expandidos": None,
            "Tempo": None,
            "Fator de Ramificação Médio": None
        },
        "DFS": {
            "Caminho": None,
            "Distancia": None,
            "Nós Expandidos": None,
            "Tempo": None,
            "Fator de Ramificação Médio": None
        },
    }

    if 's' in choose or 'S' in choose:
        origem = int(input("Origem: "))
        destino = int(input("Destino: "))
    
    while True:
        print("\n1 - A* com Heurística Euclidiana")
        print("2 - A* com Heurística de Haversine")
        print("3 - A* com Heurística de Manhattan")
        print("4 - Dijkstra")
        print("5 - BFS")
        print("6 - DFS")
        print("7 - GERAR SHAPEFILE DO ULTIMO ALGORITMO")
        print("8 - GERAR PONTOS ALEATÓRIOS - A* HAVERSINE")
        print("9 - Relatório")
        print("10 - Gerar Csv")
        print("11 - Calcular 10 rotas")
        print("0 - Sair\n")
        
        entrada = input("Selecione o Algoritmo -> ")

        def buscar_AEuclidean(origem, destino):
                caminho, tempo, nos_expandidos, distancia = a_star_search(origem, destino, grafo_distancias, "euclidiana", grafo_coordenadas)
                caminho = caminho[::-1]
                relatorio["A* EUCLIDIANO"]["Caminho"] = caminho
                relatorio["A* EUCLIDIANO"]["Distancia"] = distancia
                relatorio["A* EUCLIDIANO"]["Nós Expandidos"] = nos_expandidos
                relatorio["A* EUCLIDIANO"]["Tempo"] = tempo
                relatorio["A* EUCLIDIANO"]["Fator de Ramificação Médio"] = nos_expandidos / tempo
        
        def buscar_AHaversine(origem, destino):
                caminho, tempo, nos_expandidos, distancia = a_star_search(origem, destino, grafo_distancias,"haversine", grafo_coordenadas)
                caminho = caminho[::-1]
                relatorio["A* HAVERSINI"]["Caminho"] = caminho
                relatorio["A* HAVERSINI"]["Distancia"] = distancia
                relatorio["A* HAVERSINI"]["Nós Expandidos"] = nos_expandidos
                relatorio["A* HAVERSINI"]["Tempo"] = tempo
                relatorio["A* HAVERSINI"]["Fator de Ramificação Médio"] = nos_expandidos / tempo
        
        def buscar_AManhattan(origem, destino):
                caminho, tempo, nos_expandidos, distancia = a_star_search(origem, destino, grafo_distancias,"manhattan", grafo_coordenadas)
                caminho = caminho[::-1]
                relatorio["A* MANHATTAN"]["Caminho"] = caminho
                relatorio["A* MANHATTAN"]["Distancia"] = distancia
                relatorio["A* MANHATTAN"]["Nós Expandidos"] = nos_expandidos
                relatorio["A* MANHATTAN"]["Tempo"] = tempo
                relatorio["A* MANHATTAN"]["Fator de Ramificação Médio"] = nos_expandidos / tempo

        def buscar_dijkstra(origem, destino):
                distancias, anteriores, tempo, expansoes = dijkstra_comprehension(grafo_distancias, origem)
                distancia_minima = distancias[destino]
                caminho = encontrar_caminho(anteriores, destino)
                print("caminho encontrado: ", caminho)
                print("distancia minima: ", distancia_minima)
                relatorio["Dijkstra"]["Caminho"] = caminho
                relatorio["Dijkstra"]["Distancia"] = distancia_minima
                relatorio["Dijkstra"]["Tempo"] = tempo
                relatorio["Dijkstra"]["Nós Expandidos"] = expansoes
                relatorio["Dijkstra"]["Fator de Ramificação Médio"] = expansoes / tempo

        def buscar_bfs(origem, destino):
                distancia, tempo, nos_expandidos, caminho = BFS_search(origem, destino, grafo_distancias)
                caminho = caminho[::-1]
                relatorio["BFS"]["Caminho"] = caminho
                relatorio["BFS"]["Distancia"] = distancia
                relatorio["BFS"]["Nós Expandidos"] = nos_expandidos
                relatorio["BFS"]["Tempo"] = tempo
                relatorio["BFS"]["Fator de Ramificação Médio"] = nos_expandidos / tempo

        def buscar_dfs(origem, destino):
                distancia, tempo, nos_expandidos, caminho = DFS_search(origem, destino, grafo_distancias)
                caminho = caminho[::-1]
                relatorio["DFS"]["Caminho"] = caminho
                relatorio["DFS"]["Distancia"] = distancia
                relatorio["DFS"]["Nós Expandidos"] = nos_expandidos
                relatorio["DFS"]["Tempo"] = tempo
                relatorio["DFS"]["Fator de Ramificação Médio"] = nos_expandidos / tempo

        if entrada == '1':
            buscar_AEuclidean(origem, destino)

        elif entrada == '2':
            buscar_AHaversine(origem, destino)

        elif entrada == '3':
            buscar_AManhattan(origem, destino)

        elif entrada == '4':
            buscar_dijkstra(origem, destino)

        elif entrada == '5':
            buscar_bfs(origem, destino)
        
        elif entrada == '6':
            buscar_dfs(origem, destino)

        elif entrada == "7":
            gerar_shapefile(caminho)

        elif entrada == '8':

            total_nodes = 20 #valor ficticio para geração de aleatoriedade
            num_random_points = int(input("Quantas situações deve gerar? (Ex: 5) -> "))
            
            def generate_random_points(num_points):
                points = []
                for _ in range(num_points):
                    origin = random.randint(1, total_nodes)
                    destination = random.randint(1, total_nodes)
                    points.append((origin, destination))
                return points

            def run_a_star_haversine(points):
                results = []
                for origin, destination in points:
                    process = psutil.Process(os.getpid())
                    start_memory = process.memory_info().rss / 1024
                    caminho, tempo, nos_expandidos, distancia = a_star_search(origin, destination, grafo_distancias, "haversine", grafo_coordenadas)
                    end_memory = process.memory_info().rss / 1024
                    memory_consumption = end_memory - start_memory
                    fator_ramificacao = nos_expandidos / tempo
                    results.append((origin, destination, tempo, fator_ramificacao, memory_consumption, distancia, nos_expandidos))
                return results

            random_points = generate_random_points(num_random_points)
            # random_points = [(1, 2), (2, 3)]
            results = run_a_star_haversine(random_points)

            df = pd.DataFrame(results, columns=["origem", "destino", "tempo", "Nós Expandidos", "consumo de ram", "distancia final", "nos expandidos"])

            df.to_csv('resultado.csv', index=False)


        elif entrada == "9":
            print("\nRELATÓRIO\n")
            for i, j in relatorio.items():
                print(f"{i}:")
                for cateogory, item in j.items():
                    print(f"{cateogory} - {item}")
                print("\n")
        elif entrada == "10":
            criar_csv.write_csv(relatorio)
        elif entrada == "11":
            for i in caminhos:
                origem = i[0]
                destino = i[1]

                buscar_bfs(origem, destino)
                buscar_AEuclidean(origem, destino)
                buscar_AManhattan(origem, destino)
                buscar_AHaversine(origem, destino)
                buscar_dijkstra(origem, destino)

                criar_csv.write_csv(relatorio)

        elif entrada == "0":
            break
        else:
            print("Opção Inválida!")

if __name__ == "__main__":
    main()