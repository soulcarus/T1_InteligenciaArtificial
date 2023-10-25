import time

def get_vertice(longitude, latitude, file_name):
    vertice = 0
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('v'):
                parts = line.strip().split()
                long = int(parts[2])
                lat = int(parts[3])
                if (longitude == long and latitude == lat):
                    vertice = int(parts[1])
    if (vertice):
        return vertice
    else:
        print("Vertice não encontrado!!")
        pass
    

def BFS_search(long1, lat1, long2, lat2, file_name, graph):
    
    initialVertice = get_vertice(long1, lat1, file_name)
    finalVertice = get_vertice(long2, lat2, file_name)
    
    if not(initialVertice):
        print("Vertice 1 não encontrado!!")
        return 0,0,0,0
    elif not(finalVertice):
        print("Vertice 2 não encontrado!!")
        return 0,0,0,0
    
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
        
    while(len(caminho) != 0):
        print(" -> ", caminho[-1], end = "")
        caminho.remove(caminho[-1])
            
            
    tempo_final = time.time()    
    tempo = tempo_final - tempo_inicial
    ramificacao = edges_expands//no_expands
    
    return dados[new_id][2], ramificacao, tempo, no_expands

def DFS_search(initialVertice, finalVertice, graph, heuristica):
    pass

def main():
    grafo = {1:[(2, 4),(5,3),(9,10)], 2:[(1,4),(3,5),(4,4)], 3:[(2,5)], 4:[(2,4)], 5:[(1,3),(6,9)], 6:[(5,9),(7,5)], 7:[(6,5),(8,10)], 8:[(7,10)], 9:[(1,10),(10,15)], 10:[(9,15)]}
    arquivo = 'USA-road-d.NY.co'
    
    distancia, ramos, time, no = BFS_search(-73795916,40737894,-73795813,40737185,arquivo,grafo)
    print("\n",distancia)
    print(ramos)
    print(time)
    print(no)
    
    
main()
    