print(int("1010", 2))        # 10
print(int("0000", 2))        # 0
print(int("1111", 2))        # 15 (somatoria de 1 + 2 + 4 + 8))

estado = int("1010", 2)
mascara = int("1100", 2)
novo = estado ^ mascara
print(novo)                  # 6
print(format(novo, "04b"))   # 0110  (volta a mostrar em binário, com 4 dígitos)