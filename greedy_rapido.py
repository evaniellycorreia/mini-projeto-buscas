import time


def kadane(ganhos):
    """Encontra o trecho consecutivo com maior soma. Retorna (soma, inicio, fim)."""
    melhor_soma, melhor_ini, melhor_fim = ganhos[0], 0, 0
    soma_atual, ini_atual = 0, 0
    for i, g in enumerate(ganhos):
        if soma_atual <= 0:          # recomeça o trecho aqui
            soma_atual, ini_atual = g, i
        else:                        # continua o trecho
            soma_atual += g
        if soma_atual > melhor_soma:
            melhor_soma, melhor_ini, melhor_fim = soma_atual, ini_atual, i
    return melhor_soma, melhor_ini, melhor_fim


def greedy_rapido(inicial, objetivo):
    """Greedy: em cada passo aplica o flip que mais reduz a distância de Hamming."""
    inicio_tempo = time.perf_counter()
    # errado[k] = 1 se o bit k está diferente do objetivo
    errado = [1 if a != b else 0 for a, b in zip(inicial, objetivo)]
    operacoes = []

    while sum(errado) > 0:
        ganhos = [1 if e else -1 for e in errado]
        _, ini, fim = kadane(ganhos)
        for k in range(ini, fim + 1):           # aplica o flip
            errado[k] = 1 - errado[k]
        operacoes.append((ini, fim))

    return {
        "encontrou": True,
        "operacoes": operacoes,
        "custo": len(operacoes),
        "estados_expandidos": len(operacoes) + 1,
        "tempo": time.perf_counter() - inicio_tempo,
    }


def custo_otimo(inicial, objetivo):
    """Custo mínimo = número de blocos consecutivos de bits errados."""
    blocos, anterior = 0, "0"
    for a, b in zip(inicial, objetivo):
        atual = "1" if a != b else "0"
        if atual == "1" and anterior == "0":
            blocos += 1
        anterior = atual
    return blocos


# ---------------- Testes ----------------
if __name__ == "__main__":
    from greedy import greedy
    from bfs import validar_solucao

    inicial = "00001001000011001100111"
    objetivo = "00000000000000000000000"

    r = greedy_rapido(inicial, objetivo)
    print("Sequência oficial:")
    print("  operações:", r["operacoes"])
    print("  custo:", r["custo"], "| custo ótimo:", custo_otimo(inicial, objetivo))
    print("  válido:", validar_solucao(inicial, objetivo, r["operacoes"]))

    print("\nComparando com o Greedy antigo:")
    for ini, obj in [("1010", "0000"), ("10101010", "00000000"), ("110011", "000000")]:
        print(f"  {ini}: antigo={greedy(ini, obj)['custo']} | "
              f"rápido={greedy_rapido(ini, obj)['custo']} | ótimo={custo_otimo(ini, obj)}")