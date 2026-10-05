L = 4
for inicio in range(L):
    for fim in range(inicio, L):
        texto = "0" * inicio + "1" * (fim - inicio + 1) + "0" * (L - 1 - fim)
        print(f"intervalo ({inicio},{fim}) -> máscara {texto} -> número {int(texto, 2)}")
        #apenas para eu entender como mascaras funcionam