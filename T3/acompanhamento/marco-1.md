# Marco 1 — Modelagem: CSES Shortest Routes I (Problema 1671) — AV3

**Data de Criação:** 18/11/2026

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:-------|:-----------|:------------------------------------------------------------------------------------------------|:------|
| 1.0 | 18/11/2026 | Criação do documento; formulação do problema de caminhos mínimos, modelagem do grafo, instância pequena e hipótese inicial de solução | E |

---

## 1. Enunciado, Entrada, Saída e Restrições

**Enunciado:**

Existem $N$ cidades conectadas por $M$ voos, e cada voo possui uma origem, um destino e uma distância. Partindo de **Syrjälä (cidade 1)**, precisamos determinar a **menor distância possível até cada cidade**, considerando que o trajeto pode passar por cidades intermediárias e que os voos são de mão única.

**Problema original:** [CSES — Shortest Routes I (1671)](https://cses.fi/problemset/task/1671)

**Entrada:**

```
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

- **Vértices ($V$):** as $N$ cidades, numeradas de $1$ a $N$; $|V| = N$ (até 100.000).
- **Arestas ($E$):** para cada linha $(a,b,c)$, cria-se uma aresta $a \to b$ de peso $c$; $|E| = M$ (até 200.000).
- **Direção:** os deslocamentos devem respeitar o sentido de cada voo; não se cria automaticamente a aresta $b \to a$.
- **Pesos:** inteiros positivos que representam as distâncias dos voos. O custo de um caminho é a soma dos pesos de suas arestas.
- **Capacidades:** não se aplicam, pois o problema não envolve limite de fluxo ou quantidade de passageiros.
- **Arestas paralelas:** podem existir voos diferentes entre o mesmo par ordenado de cidades; cada voo deve ser considerado com seu próprio peso.
- **Origem:** o vértice $1$.

**Relação com o problema:** para cada cidade $v$, precisamos calcular $dist[v]$, a menor soma de pesos entre a cidade $1$ e $v$. A resposta é o vetor $dist[1], dist[2], \ldots, dist[N]$; o enunciado **não solicita imprimir os caminhos**, apenas seus comprimentos.

### Resultado de Aprendizagem Aferido

Este marco mobiliza a modelagem de **caminhos mínimos em grafos direcionados e ponderados**. A competência avaliada é transformar uma rede de voos em um grafo, identificar corretamente a direção e o custo das arestas e distinguir **menor custo total** de simples alcançabilidade ou menor número de arestas. Como todos os pesos são positivos, a hipótese de solução é o **Algoritmo de Dijkstra**, apresentado na Seção 4.

---

## 3. Instância Pequena e Resultado Esperado

**Caso de teste (4 cidades e 5 voos):**

```
4 5
1 2 10
1 3 3
3 4 4
2 4 2
1 4 12
```

**Lista de adjacência ponderada (saídas de cada cidade):**

| Cidade | Voos de saída (destino, distância) |
|:---|:---|
| **1** | (2, 10), (3, 3), (4, 12) |
| **2** | (4, 2) |
| **3** | (4, 4) |
| **4** | Nenhum |

**Resultado esperado:**

```
0 10 3 7
```

**Explicação:**

- **Cidade 1:** distância `0`, porque é a origem.
- **Cidade 2:** o voo direto $1 \to 2$ custa `10`; não há alternativa mais barata nessa instância.
- **Cidade 3:** o voo direto $1 \to 3$ custa `3`.
- **Cidade 4:** existem o voo direto $1 \to 4$, de custo `12`, e o trajeto $1 \to 2 \to 4$, de custo $10+2=12$. Entretanto, o caminho $1 \to 3 \to 4$ custa $3+4=7$, sendo o menor.

**Observação sobre a saída:** para cada cidade, imprimimos apenas a **menor distância**, mesmo quando diferentes caminhos poderiam produzir o mesmo custo. Não é necessário informar a sequência de cidades percorridas.

---

## 4. Hipótese Inicial de Solução

**Estratégia de resolução:** como o grafo é direcionado, ponderado e possui apenas pesos positivos, a proposta é utilizar o **Algoritmo de Dijkstra** com **lista de adjacência e fila de prioridade mínima**:

1. Inicializar as distâncias de todas as cidades com um valor muito grande (infinito), exceto a cidade $1$, cuja distância inicial é `0`.
2. Inserir a cidade $1$ na fila de prioridade com distância `0`.
3. Retirar a cidade de menor distância conhecida e examinar seus voos de saída.
4. Para cada voo $u \to v$ de peso $c$, verificar se $dist[u] + c < dist[v]$. Se for verdade, atualizar $dist[v]$ e a prioridade correspondente. Esse processo é chamado de **relaxamento de aresta**.
5. Continuar até que não existam mais cidades a processar e imprimir as menores distâncias na ordem de $1$ a $N$.

**Complexidade esperada:** $O((V+E)\log V)$ com uma fila de prioridade indexada e listas de adjacência; o armazenamento do grafo e das distâncias exige $O(V+E)$ de memória. Essa abordagem é adequada para os limites de até $10^5$ cidades e $2\cdot10^5$ voos.

**Cuidado com os valores:** como uma aresta pode ter peso de até $10^9$ e um caminho pode acumular muitas arestas, a distância total pode ultrapassar o limite de um inteiro de 32 bits. Em Java, uma implementação com distâncias inteiras deve usar **`long`** (e não `int`) para os custos acumulados.

### Avaliação do reaproveitamento das classes de referência do professor

Assim como na AV2, consideramos o reaproveitamento de classes da biblioteca `algs4`. Para este problema, a representação precisa preservar **direção e peso**; portanto, as classes genéricas de grafos não são suficientes por si só.

| Classe da `algs4` | Reaproveitável neste problema? | Justificativa |
|---|---|---|
| `EdgeWeightedDigraph` | **Sim.** | Representa um grafo direcionado e ponderado por meio de listas de adjacência. É apropriada para armazenar as cidades e os voos, inclusive arestas paralelas. Os índices da biblioteca começam em `0`, então as cidades da entrada podem ser convertidas de `1..N` para `0..N-1`. |
| `DirectedEdge` | **Sim.** | Representa cada voo com origem, destino e peso. É utilizada em conjunto com `EdgeWeightedDigraph`. |
| `Bag` | **Sim, indiretamente.** | É a estrutura utilizada internamente por `EdgeWeightedDigraph` para armazenar as listas de adjacência. |
| `DijkstraSP` | **Sim, com atenção à saída.** | Já implementa Dijkstra para grafos ponderados direcionados, calculando os menores caminhos a partir de uma origem. A classe utiliza `double` para as distâncias, enquanto o CSES exige inteiros na saída; será necessário formatar/converter corretamente os resultados. Os limites deste problema permitem representar exatamente essas somas inteiras em `double`, mas uma implementação própria com `long` também é válida. |
| `IndexMinPQ` | **Sim, caso a busca seja implementada.** | Fornece uma fila de prioridade mínima indexada, útil para selecionar a próxima cidade e atualizar sua prioridade durante os relaxamentos. Uma alternativa é usar `PriorityQueue` do Java, descartando entradas desatualizadas. |
| `Graph`, `Digraph` | **Não diretamente.** | `Graph` não preserva a direção; `Digraph` preserva a direção, mas não armazena pesos nas arestas. O problema precisa das duas características. |
| `DepthFirstPaths`, `BreadthFirstPaths`, `UF`, `CC` | **Não aplicável como solução.** | Essas classes tratam de percursos e conectividade. A BFS tradicional, por exemplo, minimiza o número de arestas em grafos não ponderados, e não a soma das distâncias dos voos. |
| `SymbolGraph`, `ST` | **Não necessário.** | As cidades já vêm identificadas por números consecutivos, dispensando uma tabela de símbolos para traduzir nomes. |

**Conclusão da avaliação:** `EdgeWeightedDigraph` e `DirectedEdge` atendem à representação do grafo. Para calcular os caminhos mínimos, é possível reaproveitar `DijkstraSP` (adaptando a saída ao formato do CSES) ou implementar Dijkstra com distâncias `long` e uma fila de prioridade. A decisão de implementação e seus detalhes ficam para o Marco 2.
