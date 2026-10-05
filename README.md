# Mini-projeto: buscas clássicas e otimização

Projeto da primeira avaliação de buscas classicas. Uso de BFS, Greedy e Gradiente Descendente para resolver o problema de flip de bits.

## Requisitos

- Bibliotecas: 
	- numpy
	- pandas
	- matplotlib

## Arquivos

|---|---|
| `bit_flips.py` | Flip de intervalo e geração de sucessores |
| `bfs.py` | BFS (versão com texto e versão com máscara XOR) |
| `greedy.py` | Busca com greedy com distância de Hamming |
| `greedy_rapido.py` | Greedy com algoritmo de Kadane e cálculo do custo ótimo |
| `experimento_seq_aleatoria.py` | BFS vs Greedy em pares aleatórios (utilizado random.seed(42) para reproduzir resultados (L = 2 a 256) |
| `gerando graficos.py` | Gráficos a partir de `resultados.csv` para comparação de resultados - graficos estao na pasta em PNG |
| `experimento_L_grande.py` | Greedy vs custo ótimo (L = 2 a 4096) |
| `gradiente.py` | Gradiente descendente e a taxa de aprendizado |
| `custo_consecutivo.py` | Função J = L + λC, regra da cadeia e efeito de λ |

## Como reproduzir

```bash
python bfs.py
python greedy.py
python greedy_rapido.py
python experimento_seq_aleatoria.py
python "gerando graficos.py"
python experimento_L_grande.py
python gradiente.py
python custo_consecutivo.py
```

Os experimentos usam `random.seed(42)`, então os resultados são reproduzíveis.
