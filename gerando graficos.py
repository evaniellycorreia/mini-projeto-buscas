import pandas as pd
import matplotlib.pyplot as plt

# Lê o CSV gerado pelo experimento
dados = pd.read_csv("resultados.csv")
dados = dados[dados["encontrou"] == True]

# Médias por algoritmo e tamanho L
medias = dados.groupby(["algoritmo", "L"])[["custo", "estados_expandidos", "tempo"]].mean().reset_index()

# Gráfico 1: estados expandidos
plt.figure(figsize=(6, 4))
for nome in ["BFS", "Greedy"]:
    parte = medias[medias["algoritmo"] == nome]
    plt.plot(parte["L"], parte["estados_expandidos"], marker="o", label=nome)
plt.yscale("log")
plt.xlabel("Tamanho da sequência (L)")
plt.ylabel("Estados expandidos (média, escala log)")
plt.title("BFS vs Greedy: estados expandidos")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("grafico_expandidos.png", dpi=200)

# Gráfico 2: custo médio
plt.figure(figsize=(6, 4))
for nome, marcador in [("BFS", "o"), ("Greedy", "x")]:
    parte = medias[medias["algoritmo"] == nome]
    plt.plot(parte["L"], parte["custo"], marker=marcador, label=nome)
plt.xlabel("Tamanho da sequência (L)")
plt.ylabel("Custo médio")
plt.title("BFS vs Greedy: custo da solução")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("grafico_custo.png", dpi=200)

print("Gráficos salvos: grafico_expandidos.png e grafico_custo.png")
plt.show()