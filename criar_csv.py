import csv

def write_csv(dados):

    arquivo = "relatório_final.csv"

    colunas = ['Algoritmo', 'Pontos', 'Caminho', 'Distancia', 'Nós Expandidos', 'Tempo', 'Fator de Ramificação Médio']

    modo = "a"
    try:
        with open(arquivo, mode='r') as arq:
            linha = arq.readlines()
            if len(linha) >= 6:
                modo = "a"
            else:
                modo = "w"
    except Exception:
        pass

    with open(arquivo, mode=modo, newline='') as arquivo_excel:
        writer = csv.writer(arquivo_excel)

        if modo == "w":
            writer.writerow(colunas)
        # writer.writerow(f"{dados['Dijkstra']['Caminho'][0]} {dados['Dijkstra']['Caminho'][-1]}")
        for algoritmo, dados_algoritmo in dados.items():
            if algoritmo == "DFS":
                continue
            origem_destino = f"({dados_algoritmo['Caminho'][0]}, {dados_algoritmo['Caminho'][-1]})"
            # Ajuste para incluir origem e destino na coluna "Pontos"
            writer.writerow([algoritmo, origem_destino] + [dados_algoritmo[chave] for chave in colunas[2:]])
