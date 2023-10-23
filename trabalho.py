import exemplo_gerar_grafo as funcao
import time
import math
import time

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

def ler_grafo_distancia(nome_arquivo): #CONCLUÍDA COM FORMATO DE RETORNO DEFINIDO ( ÍCARO )
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
                # arestas.append((str(origem), str(destino), distancia))
    # print(arestas) #teste
    # print(grafo) #teste
    return grafo

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
    lat1, long1, lat2, long2 = 0, 0, 0, 0
    with open('USA-road-d.NY.co', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(f"v {v1}"):
                parts = line.strip().split()
                lat1 = int(parts[2])
                long1 = int(parts[3])
            if line.startswith(f"v {v2}"):
                parts = line.strip().split()
                lat2 = int(parts[2])
                long2 = int(parts[3])
    lat1 = lat1 / 1e6
    lat2 = lat2 / 1e6
    long1 = long1 / 1e6
    long2 = long2 / 1e6
    
    d = (((lat2 - lat1) ** 2) + ((long2 - long1) ** 2)) ** (1/2)
    return d

def haversine_dist(v1, v2): #Função concluida (João Ícaro)
    if v1 == v2:
        return 0.00
    lat1, long1, lat2, long2 = 0, 0, 0, 0
    with open('USA-road-d.NY.co', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(f"v {v1}"):
                parts = line.strip().split()
                lat1 = int(parts[2])
                long1 = int(parts[3])
            if line.startswith(f"v {v2}"):
                parts = line.strip().split()
                lat2 = int(parts[2])
                long2 = int(parts[3])

    lat1 = lat1 / 1e6
    lat2 = lat2 / 1e6
    long1 = long1 / 1e6
    long2 = long2 / 1e6
    
    raio = 6371000

    #converter graus decimais em radianos
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])

    # Diferenças de latitude e longitude
    dlat = lat2 - lat1
    dlon = long2 - long1

    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distância em metros
    distancia = raio * c

    return distancia

def f_calc(vertice): #Função concluida (Carlos Gabriel)
    # f(n)=g(n)+h(n),
    # f(n) = custo total estimado do caminho através do nó n
    # g(n) = custo até agora para chegar ao nó n
    # h(n) = custo estimado de n até a meta. Esta é a parte heurística da função de custo, portanto é como uma suposição.
    return vertice["g"] + vertice["h"]

def a_star_search(initialVertice, finalVertice, graph, heuristica):

    tempo_inicial = time.time()
    if heuristica == "euclidiana":
        initialVerticeDict = {
            "father": None,
            "vertice": initialVertice,
            "g": 0,
            "h": euclidean_dist(initialVertice, finalVertice),
        }
    elif heuristica == "haversine":
        initialVerticeDict = {
            "father": None,
            "vertice": initialVertice,
            "g": 0,
            "h": haversine_dist(initialVertice, finalVertice),
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
        print(f"current: {current_vertice}") #PRINT ESTILO GABRIEL

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
                neighborDict["h"] = euclidean_dist(neighbor, finalVertice)
            elif heuristica == "haversine":
                neighborDict["h"] = haversine_dist(neighbor, finalVertice)

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
        print("Tempo de execução:", tempo_final - tempo_inicial)
        print("Caminho encontrado:", path)
    else:
        print("Caminho não encontrado.")

def main():
    nome_arquivo_gr = './USA-road-d.NY.gr'  # Arquivo de distâncias
    print("origem atual: 300")
    print("destino atual: 400")
    choose = input("Alterar origem e destino? S/N? -> ")

    origem = 300
    destino = 400

    if choose == 'S':
        origem = int(input("Origem: "))
        destino = int(input("Destino: "))
    
    while True:
        print("1 - A* com Heurística Euclidiana")
        print("2 - A* com Heurística de Haversine")
        print("3 - Dijkstra")
        print("0 - Sair")
        
        entrada = input("Selecione o Algoritmo -> ")

        if entrada == '1':
            grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
            a_star_search(origem, destino, grafo_distancias, "euclidiana")

        elif entrada == '2':
            grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
            a_star_search(origem, destino, grafo_distancias,"haversine")

        elif entrada == '3':
            grafo_distancias = ler_grafo_distancia(nome_arquivo_gr)
            distancias, anteriores = dijkstra_comprehension(grafo_distancias, origem)
            distancia_minima = distancias[destino]
            caminho = encontrar_caminho(anteriores, origem, destino)
            print(f'Distância mínima de {origem} para {destino}: {distancia_minima}')
            print(f'Caminho: {caminho}')

        elif entrada == '0':
            break
        else:
            print("Opção Inválida!")

if __name__ == "__main__":
    main()
