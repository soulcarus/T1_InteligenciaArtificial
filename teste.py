# IGNORE

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

arq_gr = "./USA-road-d.W.gr"
arq_co = "./USA-road-d.W.co"

grafo_gr = ler_grafo_distancia(arq_gr)
grafo_co = ler_grafo_coordenadas(arq_co)

import json

caminho_gr = arq_gr + ".json"
caminho_co = arq_co + ".json"

with open(caminho_gr, "w") as arquivo:
    json.dump(grafo_gr, arquivo)

with open(caminho_co, "w") as arquivo:
    json.dump(grafo_co, arquivo)