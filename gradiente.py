import numpy as np
import matplotlib.pyplot as plt


def gradiente_descendente(inicial, objetivo, eta, passos=20):
    """Minimiza L(x) = soma (x - y)^2. Retorna o histórico de x e do erro."""
    x = np.array([float(b) for b in inicial])
    y = np.array([float(b) for b in objetivo])
    historico_x = [x.copy()]
    historico_erro = [np.sum((x - y) ** 2)]

    for _ in range(passos):
        gradiente = 2 * (x - y)
        x = x - eta * gradiente          # a transformação deste passo é -eta*gradiente
        historico_x.append(x.copy())
        historico_erro.append(np.sum((x - y) ** 2))

    return np.array(historico_x), historico_erro


if __name__ == "__main__":
    inicial = "00001001000011001100111"
    objetivo = "00000000000000000000000"

    # 1) Erro ao longo dos passos para diferentes valores de eta
    plt.figure(figsize=(6, 4))
    for eta in [0.1, 0.25, 0.5, 0.75, 1.0]:
        hx, erro = gradiente_descendente(inicial, objetivo, eta)
        print(f"eta={eta:4}: erro final={erro[-1]:.6f} | menor valor de x={hx.min():.3f}")
        plt.plot(erro, marker=".", label=f"η = {eta}")
    plt.xlabel("Passo")
    plt.ylabel("Erro L(x)")
    plt.title("Gradiente descendente: efeito de η")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("grafico_eta.png", dpi=200)

    # 2) Um bit (x=1, y=0) ficando negativo quando eta > 1/2
    plt.figure(figsize=(6, 4))
    for eta in [0.25, 0.75]:
        hx, _ = gradiente_descendente("1", "0", eta, passos=8)
        plt.plot(hx[:, 0], marker="o", label=f"η = {eta}")
    plt.axhline(0, color="gray", linewidth=0.8)
    plt.xlabel("Passo")
    plt.ylabel("Valor do bit x")
    plt.title("Bit saindo do intervalo [0,1] para η > 1/2")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("grafico_bit_negativo.png", dpi=200)

    print("\nGráficos salvos: grafico_eta.png e grafico_bit_negativo.png")