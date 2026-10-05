from collections import deque
import time

from bit_flips import flip_intervalo, gerar_sucessores


def reconstruir_caminho(pais, objetivo):
    operacoes = []
    estado = objetivo
    while pais[estado] is not None:
        estado_anterior, operacao = pais[estado]
        operacoes.append(operacao)
        estado = estado_anterior
    operacoes.reverse()
    return operacoes


def bfs(inicial, objetivo):
    """Busca em largura"""
    inicio_tempo = time.perf_counter()

    fila = deque([inicial])
    pais = {inicial: None}          
    estados_expandidos = 0

    while fila:
        estado = fila.popleft()
        estados_expandidos += 1

        if estado == objetivo:
            operacoes = reconstruir_caminho(pais, objetivo)
            return {
                "encontrou": True,
                "operacoes": operacoes,
                "custo": len(operacoes),
                "estados_expandidos": estados_expandidos,
                "estados_visitados": len(pais),
                "tempo": time.perf_counter() - inicio_tempo,
            }

        for novo_estado, operacao in gerar_sucessores(estado):
            if novo_estado not in pais:
                pais[novo_estado] = (estado, operacao)
                fila.append(novo_estado)

    return {"encontrou": False}


def validar_solucao(inicial, objetivo, operacoes):
    estado = inicial
    for inicio, fim in operacoes:
        estado = flip_intervalo(estado, inicio, fim)
    return estado == objetivo

def bfs_mascara_XOR(inicial, objetivo, limite_estados=None):
    """estados representados como inteiros e com o flip feito por XOR com uma máscara para economizar tempo de processamento"""
    inicio_tempo = time.perf_counter()
    L = len(inicial)
    ini = int(inicial, 2)
    obj = int(objetivo, 2)

    mascaras = []
    for inicio in range(L):
        for fim in range(inicio, L):
            mascara = ((1 << (fim - inicio + 1)) - 1) << (L - 1 - fim)
            mascaras.append((mascara, (inicio, fim)))

    def resultado(operacoes, expandidos):
        return {
            "encontrou": True,
            "operacoes": operacoes,
            "custo": len(operacoes),
            "estados_expandidos": expandidos,
            "estados_visitados": len(pais),
            "tempo": time.perf_counter() - inicio_tempo,
        }

    pais = {ini: None}
    if ini == obj:
        return resultado([], 0)

    fila = deque([ini])
    expandidos = 0

    while fila:
        estado = fila.popleft()
        expandidos += 1

        if expandidos % 100000 == 0:
            print(f"  ... {expandidos} estados expandidos, "
                  f"{len(pais)} visitados, {time.perf_counter() - inicio_tempo:.1f}s")

        for mascara, operacao in mascaras:
            novo = estado ^ mascara
            if novo not in pais:
                pais[novo] = (estado, operacao)
                if novo == obj:
                    return resultado(reconstruir_caminho(pais, obj), expandidos)
                fila.append(novo)

        if limite_estados and len(pais) > limite_estados:
            return {"encontrou": False, "motivo": "limite_estados",
                    "estados_expandidos": expandidos,
                    "tempo": time.perf_counter() - inicio_tempo}

    return {"encontrou": False, "motivo": "sem_solucao"}

# ---------------- Testes ----------------
# ---------------- Testes ----------------
if __name__ == "__main__":
    # 1) As duas versões precisam concordar nos casos pequenos
    casos = [("1010", "0000"), ("101", "000"), ("0011100", "0000000"),
             ("10101010", "00000000"), ("110011", "000000")]

    print("Comparando bfs e bfs_mascara_XOR:")
    for inicial, objetivo in casos:
        c1 = bfs(inicial, objetivo)["custo"]
        r2 = bfs_mascara_XOR(inicial, objetivo)
        ok = validar_solucao(inicial, objetivo, r2["operacoes"])
        print(f"  {inicial}: bfs={c1} | rapido={r2['custo']} | válido={ok}")

    # 2) Sequência oficial do projeto
    inicial = "00001001000011001100111"
    objetivo = "00000000000000000000000"

    print("\nSequência oficial (pode levar alguns minutos):")
    r = bfs_mascara_XOR(inicial, objetivo, limite_estados=10_000_000)

    if r["encontrou"]:
        print(f"  operações: {r['operacoes']}")
        print(f"  custo: {r['custo']}")
        print(f"  estados expandidos: {r['estados_expandidos']}")
        print(f"  estados visitados: {r['estados_visitados']}")
        print(f"  tempo: {r['tempo']:.2f}s")
        print(f"  válido: {validar_solucao(inicial, objetivo, r['operacoes'])}")
    else:
        print(f"  Não concluiu: {r['motivo']}")
