# Marco 2 — Representação Computacional: Ladder Takahashi (Problema I)

**Data de Criação:** 15/08/2026  

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo   |
| :--- | :--- | :--- |:--------|
| 1.0 | 15/08/2026 | Criação do documento e estrutura inicial | F |
| | | |         |

---

## 1. Escolha da Representação Computacional

**Estrutura de Dados Selecionada:**

Lista de adjacência implementada como um `defaultdict(list)` do módulo `collections`, no qual a **chave é o número original do andar** (não um índice comprimido sequencial) e o **valor é a lista de andares vizinhos** (andares diretamente acessíveis por uma escada).

**Justificativa:**

Uma matriz de adjacência tradicional exigiria um vetor/matriz indexado por número de andar, o que é inviável, já que os andares chegam a $10^9$ — resultaria em estouro de memória (*Memory Limit Exceeded*), pois a matriz teria dimensão $10^9 \times 10^9$.

A lista de adjacência é a estrutura adequada, pois o grafo é **esparso**: com $N \le 2\times10^5$ escadas, existem no máximo $|V| \le 2N+1 \le 4\times10^5+1$ andares distintos relevantes, e o restante dos $10^9$ andares nunca é visitado nem armazenado.

Optou-se por usar o **próprio número do andar como chave do dicionário** (`defaultdict(list)`), em vez de aplicar uma compressão de coordenadas para índices sequenciais $0..|V|-1$. O dicionário (tabela hash) já resolve o problema de esparsidade nativamente — apenas os andares que efetivamente aparecem na entrada (mais o andar 1) ocupam memória — e essa abordagem simplifica a leitura e a validação, já que os vértices no código continuam sendo identificados pelo mesmo valor apresentado no enunciado, sem necessidade de tradução entre índice comprimido e andar original.

Essa estrutura garante complexidade espacial e temporal $O(V + E)$, adequada para as buscas DFS/BFS que serão realizadas nos Marcos 3 e 4.

---

## 2. Leitura da Entrada e Construção do Grafo

**Processo de Construção:**

1. A entrada é lida do `stdin` e convertida diretamente em um **`numpy.array`** de shape $(N, 2)$ e `dtype=np.int64` (conforme especificado no Marco 1), garantindo suporte a valores de andar de até $10^9$ sem risco de overflow.
2. Para cada linha `[A_i, B_i]` do array (cada escada), a aresta é inserida **simetricamente** no dicionário de adjacência: `grafo[A_i].append(B_i)` e `grafo[B_i].append(A_i)`, refletindo que o grafo é **não direcionado**.
3. Como o `defaultdict(list)` cria automaticamente uma lista vazia para qualquer chave não existente, a presença do **andar 1** no dicionário é garantida por meio de um acesso explícito (`grafo[1]`) logo após a construção — isso assegura que o vértice de partida sempre exista na estrutura, mesmo que ele não apareça em nenhuma escada (caso do Sample 3 do Marco 1, cuja resposta é 1).

**Trecho de Código / Lógica Principal:**

```python
import sys
import numpy as np
from collections import defaultdict


def ler_entrada():
    """
    Lê a entrada padrão e retorna um numpy.array de shape (N, 2),
    dtype=np.int64, onde cada linha é o par (A_i, B_i) de uma escada.
    """
    data = sys.stdin.read().split()
    n = int(data[0])
    valores = np.array(data[1:1 + 2 * n], dtype=np.int64)
    edges = valores.reshape(n, 2)
    return edges


def construir_grafo(edges):
    """
    Constrói a lista de adjacência do grafo G = (V, E) usando
    defaultdict(list), com o número original do andar como chave.

    Otimização: edges.tolist() converte o numpy.array inteiro para
    uma lista nativa do Python em uma única operação vetorizada,
    evitando o overhead de conversão np.int64 -> int a cada iteração
    do loop (o que seria necessário se iterássemos diretamente sobre
    o array do numpy).

    Parâmetros:
        edges: numpy.array (N, 2) com os pares (A_i, B_i).

    Retorna:
        grafo: defaultdict(list) tal que grafo[andar] contém a
               lista de andares vizinhos (grafo não direcionado).
    """
    grafo = defaultdict(list)

    for a, b in edges.tolist():  # conversão em lote, iteração em Python puro
        grafo[a].append(b)
        grafo[b].append(a)  # aresta bidirecional (grafo não direcionado)

    grafo[1]  # garante a presença do andar 1, mesmo que isolado

    return grafo
```

---

## 3. Medidas Estruturais (Unidade I)

**Análise do Grafo Construído (referente ao Sample 1):**

- **Número total de vértices instanciados ($|V|$):** 5 andares distintos foram instanciados no dicionário: $\{1, 3, 4, 8, 10\}$.

- **Número de arestas lidas ($|E|$):** 4 escadas foram lidas da entrada, correspondendo a $|E| = 4$ arestas no grafo.

- **Grau dos vértices ($d(v)$):**

| Andar (vértice) | Grau $d(v)$ | Vizinhos |
|:---:|:---:|:---|
| 1  | 1 | [4] |
| 3  | 2 | [4, 8] |
| 4  | 3 | [1, 3, 10] |
| 8  | 1 | [3] |
| 10 | 1 | [4] |

O andar **4** possui o **grau máximo** ($d(4) = 3$), sendo o andar com mais conexões diretas — condizente com o fato de ele ser o "andar-hub" que liga o ponto de partida (andar 1) aos andares 3 e 10.

O **andar 1** (ponto de partida de Takahashi) possui **grau 1**, conectando-se apenas ao andar 4.

Essas medidas confirmam a teoria apresentada no Marco 1 (Seção 2): o grafo é esparso, não direcionado, com $|V| \le 2N+1$ e $|E| = N$, consistente com os valores obtidos ($|V|=5 \le 2(4)+1=9$ e $|E|=4=N$).

---

## 4. Validação da Representação (Instância Pequena)

**Entrada do Sample 1:**
```text
4
1 4
4 3
4 10
8 3
```

**Código de Impressão (para validação visual):**

```python
if __name__ == "__main__":
    edges = ler_entrada()
    grafo = construir_grafo(edges)

    print(dict(grafo))
```

**Estado Final da Memória (Lista de Adjacência Gerada):**

```python
{
  1: [4],
  4: [1, 3, 10],
  3: [4, 8],
  10: [4],
  8: [3]
}
```

A saída real do programa confirma que:

- O andar 1 está corretamente conectado ao andar 4.
- O andar 4 concentra as três conexões esperadas (1, 3 e 10), refletindo o grau máximo identificado na Seção 3.
- O andar 3 conecta-se a 4 e a 8, e o andar 8 conecta-se de volta a 3 — validando a **bidirecionalidade** das arestas (grafo não direcionado).
- O andar 10 conecta-se apenas a 4, sendo uma folha do componente.

Essa estrutura é **idêntica** à relação de adjacência descrita pela matriz de incidência apresentada no Marco 1 (Seção 3), confirmando que a representação computacional construída neste marco é fiel à modelagem teórica definida anteriormente.