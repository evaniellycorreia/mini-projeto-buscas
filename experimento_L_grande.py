import csv
import random

import pandas as pd
import matplotlib.pyplot as plt

from greedy_rapido import greedy_rapido, custo_otimo
from bfs import validar_solucao

random.seed(42)
L_valores = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
N = 10


def gerar_sequencia(L):
    return "".join(random.choice("01") for _ in range(L))


linhas = []
for L in L_valores:
    for i in range(N):
        inicial = gerar_sequencia(L)
        objetivo = gerar_sequencia(L)
        r = greedy_rapido(inicial, objetivo)
        linhas.append({
            "L": L,
            "instancia": i,
            "custo_greedy": r["custo"],
            "custo_otimo": custo_otimo(inicial, objetivo),
            "estados_expandidos": r["estados_expandidos"],
            "tempo": r["tempo"],
            "valido": validar_solucao(inicial, objetivo, r["operacoes"]),
        })
    print(f"L = {L} concluído")

with open("resultados_grande.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=linhas[0].keys())
    escritor.writeheader()
    escritor.writerows(linhas)

dados = pd.DataFrame(linhas)
medias = dados.groupby("L")[["custo_greedy", "custo_otimo", "tempo"]].mean().reset_index()

print("\nResumo (médias):")
print(medias.to_string(index=False))
print("\nTodas as soluções válidas:", dados["valido"].all())
print("Greedy igual ao ótimo em todos os casos:",
      (dados["custo_greedy"] == dados["custo_otimo"]).all())

# Gráfico: custo Greedy x custo ótimo
plt.figure(figsize=(6, 4))
plt.plot(medias["L"], medias["custo_otimo"], marker="o", label="Ótimo (nº de blocos)")
plt.plot(medias["L"], medias["custo_greedy"], marker="x", linestyle="--", label="Greedy")
plt.plot(medias["L"], medias["L"] / 4, linestyle=":", label="L/4 (teórico)")
plt.xscale("log", base=2)
plt.yscale("log")
plt.xlabel("Tamanho da sequência (L)")
plt.ylabel("Custo médio")
plt.title("Greedy vs custo ótimo")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("grafico_custo_grande.png", dpi=200)
print("\nGráfico salvo: grafico_custo_grande.png")