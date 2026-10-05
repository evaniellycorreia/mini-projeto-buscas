import numpy as np
import matplotlib.pyplot as plt

EPS = 1e-6


def calcular_z(x, y):
    g = 2 * (x - y)
    return np.sqrt(g ** 2 + EPS), g


def custo_C(z):
    return np.sum(np.diff(z) ** 2)


def J(x, y, lam):
    z, _ = calcular_z(x, y)
    return np.sum((x - y) ** 2) + lam * custo_C(z)


def gradiente_J(x, y, lam):
    """Gradiente analítico de J obtido pela regra da cadeia."""
    z, g = calcular_z(x, y)
    dC_dz = np.zeros_like(z)
    dif = np.diff(z)              # z[i+1] - z[i]
    dC_dz[:-1] -= 2 * dif         # contribuição do vizinho da direita
    dC_dz[1:] += 2 * dif          # contribuição do vizinho da esquerda
    dz_dx = 2 * g / z
    return 2 * (x - y) + lam * dC_dz * dz_dx


def verificar_gradiente(x, y, lam, h=1e-6):
    """Compara o gradiente analítico com a aproximação numérica."""
    numerico = np.zeros_like(x)
    for i in range(len(x)):
        e = np.zeros_like(x)
        e[i] = h
        numerico[i] = (J(x + e, y, lam) - J(x - e, y, lam)) / (2 * h)
    return np.max(np.abs(numerico - gradiente_J(x, y, lam)))


def minimizar(inicial, objetivo, lam, eta=0.05, passos=300):
    x = np.array([float(b) for b in inicial])
    y = np.array([float(b) for b in objetivo])
    historico = [x.copy()]
    for _ in range(passos):
        x = x - eta * gradiente_J(x, y, lam)
        historico.append(x.copy())
    return np.array(historico), y


if __name__ == "__main__":
    inicial = "00001001000011001100111"
    objetivo = "00000000000000000000000"

    # 1) Conferir se a derivada pela regra da cadeia está certa
    rng = np.random.default_rng(0)
    x_teste = rng.random(len(inicial))
    y_teste = np.array([float(b) for b in objetivo])
    print("Diferença gradiente analítico x numérico:",
          f"{verificar_gradiente(x_teste, y_teste, lam=1.0):.2e}")

    # 2) Minimizar J para diferentes lambdas, medindo o CAMINHO
    lambdas = [0, 0.01, 0.1, 1]
    fig, eixos = plt.subplots(len(lambdas), 1, figsize=(7, 8), sharex=True)
    print("\nlambda | passos até L<1e-6 | C médio no caminho | C no passo 10")
    for eixo, lam in zip(eixos, lambdas):
        hist, y = minimizar(inicial, objetivo, lam)

        erros = [np.sum((h - y) ** 2) for h in hist]
        custos = [custo_C(calcular_z(h, y)[0]) for h in hist]
        passos_conv = next((i for i, e in enumerate(erros) if e < 1e-6), None)
        c_medio = np.mean(custos)
        c_passo10 = custos[10]

        print(f"{lam:6} | {str(passos_conv):>17} | {c_medio:18.4f} | {c_passo10:.4f}")

        passo_10 = hist[10] - hist[0]
        eixo.bar(range(len(passo_10)), passo_10)
        eixo.set_ylabel(f"λ = {lam}")
    eixos[-1].set_xlabel("Posição do bit")
    fig.suptitle("Transformação nos 10 primeiros passos para cada λ")
    plt.tight_layout()
    plt.savefig("grafico_lambda.png", dpi=200)
    print("\nGráfico salvo: grafico_lambda.png")
