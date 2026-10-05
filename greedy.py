import heapq
import itertools
import time

from bfs import bfs_mascara_XOR, reconstruir_caminho, validar_solucao


def hamming(estado, objetivo):
    """Conta quantos bits são diferentes entre o estado e o objetivo."""
    return bin(estado ^ objetivo).count("1")


def greedy(inicial, objetivo, limite_estados=None):
    """Busca gulosa: expande sempre o estado com menor distância de Hamming."""
    inicio_tempo = time.perf_counter()
    L = len(inicial)
    ini = int(inicial, 2)
    obj = int(objetivo, 2)

    # Uma máscara para cada flip possível (igual ao BFS)
    mascaras = []
    for inicio in range(L):
        for fim in range(inicio, L):
            texto = "0" * inicio + "1" * (fim - inicio + 1) + "0" * (L - 1 - fim)
            mascaras.append((int(texto, 2), (inicio, fim)))

    contador = itertools.count()                       # desempate por ordem de chegada
    fila = [(hamming(ini, obj), next(contador), ini)]  # (distância, ordem, estado)
    pais = {ini: None}
    expandidos = 0

    while fila:
        distancia, _, estado = heapq.heappop(fila)     # pega o MAIS PERTO do objetivo
        expandidos += 1

        if estado == obj:
            operacoes = reconstruir_caminho(pais, obj)
            return {
                "encontrou": True,
                "operacoes": operacoes,
                "custo": len(operacoes),
                "estados_expandidos": expandidos,
                "estados_visitados": len(pais),
                "tempo": time.perf_counter() - inicio_tempo,
            }

        for mascara, operacao in mascaras:
            novo = estado ^ mascara
            if novo not in pais:
                pais[novo] = (estado, operacao)
                heapq.heappush(fila, (hamming(novo, obj), next(contador), novo))

        if limite_estados and len(pais) > limite_estados:
            return {"encontrou": False, "motivo": "limite_estados",
                    "estados_expandidos": expandidos,
                    "tempo": time.perf_counter() - inicio_tempo}

    return {"encontrou": False, "motivo": "sem_solucao"}


# ---------------- Testes ----------------
if __name__ == "__main__":
    casos = [("1010", "0000"), ("101", "000"), ("0011100", "0000000"),
             ("10101010", "00000000"), ("110011", "000000")]

    print("Comparando BFS e Greedy (casos pequenos):")
    for inicial, objetivo in casos:
        rb = bfs_mascara_XOR(inicial, objetivo)
        rg = greedy(inicial, objetivo)
        ok = validar_solucao(inicial, objetivo, rg["operacoes"])
        print(f"  {inicial}: BFS custo={rb['custo']} exp={rb['estados_expandidos']} | "
              f"Greedy custo={rg['custo']} exp={rg['estados_expandidos']} | válido={ok}")

    inicial = "00001001000011001100111"
    objetivo = "00000000000000000000000"

    print("\nSequência oficial com Greedy:")
    r = greedy(inicial, objetivo, limite_estados=10_000_000)
    if r["encontrou"]:
        print(f"  operações: {r['operacoes']}")
        print(f"  custo: {r['custo']}")
        print(f"  estados expandidos: {r['estados_expandidos']}")
        print(f"  estados visitados: {r['estados_visitados']}")
        print(f"  tempo: {r['tempo']:.4f}s")
        print(f"  válido: {validar_solucao(inicial, objetivo, r['operacoes'])}")
    else:
        print(f"  Não concluiu: {r['motivo']}")