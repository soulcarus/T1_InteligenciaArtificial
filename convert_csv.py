# import pandas as pd
# import csv
# import json

# # def teste(arq):
# #     with open(arq, "r", newline="") as file:
# #         reader = file.readlines()
# #     return reader

# # def process_file(input_file, output_file):
# #     df = pd.read_csv(input_file)

# #     grouped_df = df.groupby('origem').apply(lambda x: list(zip(x['destino'], x['peso']))).reset_index(name='caminhos_pesos')
# #     # print(grouped_df)
# #     grouped_df.to_csv(output_file, index=False, columns=['origem', 'caminhos_pesos'])
    
# # # ler_grafo_distancia("./USA-road-d.NY.gr")

# arq = "./USA-road-d.E.gr"

# # # df = pd.read_csv(arq)
# # # df = df.iloc[4:]
# # # df = df.drop(4)
# # # print(df)

# # reader = teste(arq)
# # reader = reader[6:] if arq == "./USA-road-d.NY.gr" else reader[7:]

# # with open(f"{arq.replace('.gr', '')}.csv", "w", newline="") as f:
# #     writer = csv.writer(f)
# #     writer.writerow(["origem", "destino", "peso"])
# #     for i in reader:
# #         writer.writerow(i.replace("\n", "").split(" ")[1:])

# # process_file(input_file=arq.replace(".gr", ".csv"), output_file=arq.replace(".gr", ".csv"))

# meu_dict = {}
# caminho_arquivo = arq.replace(".gr", ".csv")

# with open(caminho_arquivo, newline='') as csvfile:
#     leitor_csv = csv.DictReader(csvfile)
#     for linha in leitor_csv:
#         origem = int(linha['origem'])
#         destino_peso = eval(linha['caminhos_pesos'])
#         meu_dict[origem] = destino_peso

# # caminho_arquivo = f"{arq.replace('gr', '.json')}"

# # with open(caminho_arquivo, 'w') as json_file:
# #     json.dump(meu_dict, json_file)