def flip_intervalo(estado, inicio, fim):
    bits = list(estado)
    for i in range(inicio, fim + 1):
        bits[i] = "1" if bits[i] == "0" else "0"
    return "".join(bits)


def gerar_sucessores(estado):
    sucessores = []
    L = len(estado)
    for inicio in range(L):
        for fim in range(inicio, L):
            novo_estado = flip_intervalo(estado, inicio, fim)
            sucessores.append((novo_estado, (inicio, fim)))
    return sucessores


# ---------------- Testes ----------------
if __name__ == "__main__":
    print("Teste 1: sucessores de '000'")
    for novo_estado, operacao in gerar_sucessores("000"):
        print(f"  flip {operacao} -> {novo_estado}")

    print("\nTeste 2: quantidade de sucessores")
    print("  L=4:", len(gerar_sucessores("0000")), "(esperado: 10)")
    print("  L=23:", len(gerar_sucessores("00001001000011001100111")), "(esperado: 276)")