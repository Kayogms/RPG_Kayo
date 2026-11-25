# Marco 1 — Modelagem: CSES Shortest Routes I (Problema 1671) — T3 (AP3)

**Data de Criação:** 18/11/2026

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:-------|:-----------|:------------------------------------------------------------------------------------------------|:------|
| 1.0 | 18/11/2026 | Criação do documento; formulação do problema de caminhos mínimos, modelagem do grafo, instância pequena e hipótese inicial de solução | E |
| 1.1 | 25/11/2026 | Unificação da instância pequena com os Marcos 2 e 3; padronização da linguagem para Python; ajuste de nomenclatura (T2/T3); adequação da Seção 4 como hipótese preliminar | E |

---

## 1. Enunciado, Entrada, Saída e Restrições

**Enunciado:**

Existem $N$ cidades conectadas por $M$ voos, e cada voo possui uma origem, um destino e uma distância. Partindo de **Syrjälä (cidade 1)**, precisamos determinar a **menor distância possível até cada cidade**, considerando que o trajeto pode passar por cidades intermediárias e que os voos são de mão única.

**Problema original:** [CSES — Shortest Routes I (1671)](https://cses.fi/problemset/task/1671)

**Entrada:**

```text
N M
a1 b1 c1
a2 b2 c2
...
aM bM cM
```

- $N$ = número de cidades, numeradas de $1$ a $N$; $M$ = número de voos.
- Cada uma das $M$ linhas seguintes contém três inteiros $(a, b, c)$, indicando um voo **da cidade $a$ para a cidade $b$**, com distância $c$.
- A cidade inicial é sempre a cidade $1$ (Syrjälä).

**Saída:**

- Uma única linha com $N$ inteiros: as menores distâncias da cidade $1$ até as cidades $1, 2, \ldots, N$, nessa ordem.
- A distância da cidade $1$ até ela mesma é `0`.
- O enunciado garante que é possível chegar a todas as cidades a partir da cidade $1$.

**Restrições:**

- $1 \le N \le 10^5$
- $1 \le M \le 2 \cdot 10^5$
- $1 \le a,b \le N$
- $1 \le c \le 10^9$
- Limite de tempo: **1 segundo**; limite de memória: **512 MB**.

**Observação central:** não basta verificar se uma cidade é alcançável ou contar a quantidade de voos utilizados. O objetivo é minimizar a **soma dos pesos** ao longo de cada caminho. Trata-se de um problema de **caminhos mínimos com origem única** (*Single-Source Shortest Paths*), com arestas direcionadas e pesos positivos.

---

## 2. Vértices, Arestas e Tipo de Grafo

**Grafo de entrada (rede de voos):** cada cidade é um vértice e cada voo é uma aresta direcionada com peso igual à sua distância. Como um voo de $a$ para $b$ não garante a existência do voo contrário, o grafo é **direcionado e ponderado**.

**Modelagem para caminhos mínimos:**

- **Vértices ($V$):** as $N$ cidades, numeradas de $1$ a $N$; $\vert{}V\vert{} = N$ (até 100.000).
- **Arestas ($E$):** para cada linha $(a,b,c)$, cria-se uma aresta $a \to b$ de peso $c$; $\vert{}E\vert{} = M$ (até 200.000).
- **Direção:** os deslocamentos devem respeitar o sentido de cada voo; não se cria automaticamente a aresta $b \to a$.
- **Pesos:** inteiros positivos que representam as distâncias dos voos. O custo de um caminho é a soma dos pesos de suas arestas.
- **Capacidades:** não se aplicam, pois o problema não envolve limite de fluxo ou quantidade de passageiros.
- **Arestas paralelas:** podem existir voos diferentes entre o mesmo par ordenado de cidades; cada voo deve ser considerado com seu próprio peso.
- **Indexação:** as cidades são tratadas de $1$ a $N$, acompanhando diretamente o formato da entrada (com a possibilidade de conversão para $0\ldots N-1$ caso alguma estrutura exija indexação baseada em zero).
- **Origem:** o vértice $1$.

**Relação com o problema:** para cada cidade $v$, precisamos calcular $dist[v]$, a menor soma de pesos entre a cidade $1$ e $v$. A resposta é o vetor $dist[1], dist[2], \ldots, dist[N]$; o enunciado **não solicita imprimir os caminhos**, apenas seus comprimentos.

### Resultado de Aprendizagem Aferido

Este marco mobiliza a modelagem de **caminhos mínimos em grafos direcionados e ponderados**. A competência avaliada é transformar uma rede de voos em um grafo, identificar corretamente a direção e o custo das arestas e distinguir **menor custo total** de simples alcançabilidade ou menor número de arestas.

---

## 3. Instância Pequena e Resultado Esperado

**Caso de teste (4 cidades e 5 voos):**

```text
4 5
1 2 6
1 3 2
3 2 1
2 4 2
3 4 10
```

**Lista de adjacência ponderada (saídas de cada cidade):**

| Cidade | Voos de saída (destino, distância) |
|:---|:---|
| **1** | (2, 6), (3, 2) |
| **2** | (4, 2) |
| **3** | (2, 1), (4, 10) |
| **4** | Nenhum |

**Resultado esperado:**

```text
0 3 2 5
```

**Explicação:**

- **Cidade 1:** distância `0`, porque é a origem.
- **Cidade 2:** o voo direto $1 \to 2$ custa `6`, mas o trajeto $1 \to 3 \to 2$ custa $2 + 1 = 3$, sendo o menor.
- **Cidade 3:** o voo direto $1 \to 3$ custa `2`.
- **Cidade 4:** o caminho $1 \to 3 \to 4$ custa `12` e $1 \to 2 \to 4$ custa `8`, mas o trajeto $1 \to 3 \to 2 \to 4$ custa $2 + 1 + 2 = 5$, sendo o menor.

**Observação sobre a saída:** para cada cidade, imprimimos apenas a **menor distância**, mesmo quando diferentes caminhos poderiam produzir o mesmo custo. Não é necessário informar a sequência de cidades percorridas.

---

## 4. Hipótese Preliminar de Solução

Como o grafo é direcionado, ponderado e possui apenas pesos positivos ($c \ge 1$), a hipótese preliminar é resolver o problema por meio do **Algoritmo de Dijkstra** com lista de adjacência e fila de prioridade mínima, mantendo um vetor de distâncias inicializado com infinito (exceto a origem, com `0`) e relaxando as arestas à medida que cada cidade de menor distância acumulada é processada.

**Cuidado com a ordem de grandeza das distâncias:** como cada voo pode custar até $10^9$ e um caminho pode atravessar até $N - 1$ arestas, as distâncias acumuladas podem chegar à ordem de $10^{14}$, ultrapassando o limite de inteiros de 32 bits. Na implementação do grupo em Python, o tipo `int` possui precisão arbitrária e evita *overflow* nativamente, bastando escolher uma sentinela inteira adequada (como `10**18`) para representar o infinito inicial.

A justificativa formal do algoritmo, a comparação com alternativas e a análise de complexidade são detalhadas no **Marco 3**, enquanto a avaliação e adaptação das classes de referência da disciplina ficam registradas nos **Marcos 3 e 4**.