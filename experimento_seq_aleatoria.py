import csv
import random

from bfs import bfs_mascara_XOR
from greedy import greedy

random.seed(42)            
L_valores = [2, 4, 8, 16, 32, 64, 128, 256]  
N = 10                     
LIMITE = 3_000_000         


def gerar_sequencia(L):
    return "".join(random.choice("01") for _ in range(L))


linhas = []

for L in L_valores:
    for i in range(N):
        inicial = gerar_sequencia(L)
        objetivo = gerar_sequencia(L)

        for nome, algoritmo in [("BFS", bfs_mascara_XOR), ("Greedy", greedy)]:
            r = algoritmo(inicial, objetivo, limite_estados=LIMITE)
            linhas.append({
                "algoritmo": nome,
                "L": L,
                "instancia": i,
                "inicial": inicial,
                "objetivo": objetivo,
                "encontrou": r["encontrou"],
                "custo": r.get("custo", ""),
                "estados_expandidos": r.get("estados_expandidos", ""),
                "tempo": r.get("tempo", ""),
            })

    print(f"L = {L} concluído")

# Salva todos os resultados em uma planilha CSV
with open("resultados.csv", "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=linhas[0].keys())
    escritor.writeheader()
    escritor.writerows(linhas)

# Resumo na tela: médias por algoritmo e por L
print("\nResumo (médias):")
for L in L_valores:
    for nome in ["BFS", "Greedy"]:
        dados = [x for x in linhas if x["L"] == L and x["algoritmo"] == nome and x["encontrou"]]
        if dados:
            custo = sum(x["custo"] for x in dados) / len(dados)
            exp = sum(x["estados_expandidos"] for x in dados) / len(dados)
            print(f"  L={L:2d} | {nome:6s} | custo médio={custo:.2f} | "
                  f"expandidos médio={exp:.1f} | concluídos={len(dados)}/{N}")