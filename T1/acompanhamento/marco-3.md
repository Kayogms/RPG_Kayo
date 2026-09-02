# Marco 3 — Aplicação básica de DFS: Ladder Takahashi (Problema I)

**Data de Criação:** 17 de Agosto de 2026  

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo   |
| :--- | :--- | :--- |:--------|
| 1.0 | 17/08/2026 | Criação do documento e estrutura inicial | F |
| 1.1 | 17/08/2026 | Inclusão da implementação iterativa da DFS e validação por DSU | F |
| 2.0 | 19/08/2026 | Reescrita da implementação: DFS adaptada a partir de `algs4.depth_first_paths.DepthFirstPaths` (referência de Sedgewick & Wayne); validação passa a usar `UF` e `CC` do pacote `algs4`; documentado achado de `RecursionError` em teste de estresse | F |

---

## 1. Execução Manual da DFS (Sample 1)

**Ponto de Partida:** Vértice 1 (Andar 1), representado internamente pelo índice comprimido `0` (via `LadderSymbolGraph`).

**Passo a Passo da Travessia:**

1. Partimos do vértice `1`, marcando-o como visitado (`marked[0] = True`) e inicializando `maior_andar = 1`. A chamada recursiva `_dfs(G, 0)` é iniciada.
2. Dentro da chamada de `1`, percorremos seus vizinhos (`[4]`). O vértice `4` não foi visitado, logo recebe `1` como predecessor (`edge_to`) e a função chama recursivamente `_dfs(G, 4)` — **a pilha de chamadas do Python** desempenha aqui o papel da pilha explícita da versão anterior.
3. Dentro da chamada de `4`, `maior_andar` é atualizado para `max(1, 4) = 4`. Seus vizinhos são `[1, 3, 10]`. Como `1` já foi visitado, a recursão desce primeiro em `3` (`_dfs(G, 3)`).
4. Dentro da chamada de `3`, `maior_andar` permanece `4`. Seu vizinho não visitado é `8`; a recursão desce em `8` (`_dfs(G, 8)`).
5. Dentro da chamada de `8`, `maior_andar` permanece `4`. Não há vizinhos não visitados — a função retorna (a pilha de chamadas "desempilha" de volta para `3`, depois para `4`).
6. De volta em `4`, o próximo vizinho não visitado é `10`; a recursão desce em `10` (`_dfs(G, 10)`), atualizando `maior_andar` para `max(4, 10) = 10`.
7. Não havendo mais vizinhos não visitados em nenhum nível, todas as chamadas recursivas retornam em cadeia até a chamada original, encerrando a busca com `maior_andar = 10`.

> **Nota sobre a adaptação:** diferentemente da versão anterior deste documento (que usava uma pilha explícita `pilha = []`), a implementação atual (`LadderDFS`, baseada em `algs4.depth_first_paths.DepthFirstPaths`) é **recursiva**: quem desempenha o papel da pilha é a própria pilha de chamadas do interpretador Python. O resultado final (conjunto de visitados, predecessores e maior andar) é idêntico, mas a ordem de exploração de alguns ramos pode diferir sutilmente da versão iterativa, já que a recursão sempre mergulha no primeiro vizinho não visitado antes de considerar os demais.

---

## 2. Estados de Visita e Árvore de Busca

**Controle de Estados:**

O controle de visitados é feito por meio de uma **lista booleana indexada** (`marked = [False for _ in range(G.V)]`), herdada diretamente de `algs4.depth_first_paths.DepthFirstPaths`, e não por um `set()` como na versão anterior deste documento. Essa lista é indexada pelo **índice comprimido** de cada andar (0 a `|V|-1`), obtido via `LadderSymbolGraph`, e garante acesso e atualização em tempo $O(1)$.

**Estrutura da Árvore de Busca (DFS Tree):**

* **Raiz:** Andar 1 (índice comprimido `0`)
* **Arestas de Árvore (Geradoras):** (1, 4), (4, 3), (3, 8), (4, 10)
* **Predecessores mapeados (`edge_to`, já convertidos de índice para andar original):** `{1: None, 4: 1, 3: 4, 8: 3, 10: 4}`

---

## 3. Predecessores e Alcançabilidade

O rastreio gerado pela classe `LadderDFS` (definida em `marco3_dfs.py`, adaptada de `algs4.depth_first_paths.DepthFirstPaths`) comprova os seguintes resultados para o Sample 1:

| Vértice (Andar) | Predecessor na DFS | Status de Alcançabilidade (`has_path_to`) |
| :---: | :---: | :---: |
| 1 | `None` (Origem) | Visitado |
| 3 | 4 | Visitado |
| 4 | 1 | Visitado |
| 8 | 3 | Visitado |
| 10 | 4 | Visitado |

### 3.1 Validação Cruzada com UF e CC (Oráculos)

Diferentemente da versão anterior (que usava apenas uma estrutura `DSU` própria), a validação atual compara o `maior_andar` obtido pela DFS com **dois** oráculos independentes, ambos importados sem alteração do pacote `algs4`:

* **`algs4.uf.UF`** — Union-Find com *weighted quick-union* e *path compression*.
* **`algs4.cc.CC`** — Componentes Conexas, calculadas via uma DFS recursiva independente (implementação própria do pacote, não reaproveita `LadderDFS`).

| Método | Maior andar alcançável |
| :---: | :---: |
| DFS | 10 |
| UF | 10 |
| CC | 10 |

**Saída real da validação (`ValidadorDFS.validar`, em `marco3_dfs.py`):**

```
=== Execução da DFS ===
Origem:                 1
Maior andar (DFS):      10

=== Comparação DFS x UF x CC ===
DFS -> maior andar alcançável: 10
UF  -> maior andar alcançável: 10
CC  -> maior andar alcançável: 10
[OK] DFS, UF e CC concordam: resposta = 10
```

Essa validação cruzada confirma que a árvore de busca gerada pela DFS alcança corretamente todos os vértices do componente conexo do andar 1, e que o valor máximo identificado (10) é consistente com **dois** métodos de conectividade independentes do algoritmo de busca em profundidade.

---

## 4. Aplicabilidade ao Problema, Adaptação e Limitação Identificada

**Estratégia de Adaptação:**

A DFS de referência (`DepthFirstPaths`) foi adaptada em `LadderDFS` para carregar uma variável de controle (`maior_andar`), atualizada a cada chamada recursiva, convertendo o índice comprimido de volta ao andar original via `LadderSymbolGraph.name(v)`:

```python
self.maior_andar = max(self.maior_andar, self._sg.name(v))
```

Dessa forma, a busca garante não apenas a descoberta de toda a componente conexa, mas também resolve diretamente o objetivo de encontrar o maior andar alcançável.

**Trecho de Código Integrado (`marco3_dfs.py`):**

```python
class LadderDFS:
    def __init__(self, G: Graph, sg: LadderSymbolGraph, origem_idx):
        self.marked = [False for _ in range(G.V)]
        self.edge_to = [None for _ in range(G.V)]
        self.s = origem_idx
        self._sg = sg
        self.maior_andar = sg.name(origem_idx)
        self._dfs(G, origem_idx)

    def _dfs(self, G, v):
        self.marked[v] = True
        self.maior_andar = max(self.maior_andar, self._sg.name(v))
        for w in G.adj[v]:
            if not self.marked[w]:
                self.edge_to[w] = v
                self._dfs(G, w)

    def has_path_to(self, v):
        return self.marked[v]
```

### Limitação identificada: recursão profunda em componentes "em cadeia"

Como `LadderDFS` herda a **recursão** da implementação de referência `DepthFirstPaths`, ela está sujeita ao limite de recursão padrão do Python (1000 chamadas). Isso foi confirmado empiricamente com um teste de estresse: uma entrada com $N = 2\times10^5$ escadas formando uma cadeia ($1-2, 2-3, 3-4, \dots$) faz com que a recursão da DFS ultrapasse essa profundidade.

**Saída real do teste de estresse:**

```
RecursionError confirmado: maximum recursion depth exceeded
```

Esse resultado é o principal motivo técnico, comprovado na prática (e não apenas teórico), pelo qual a **BFS (iterativa)** foi escolhida como método de submissão final no Marco 4, e não a DFS — mesmo ambas resolvendo corretamente o problema de conectividade em grafos pequenos como o Sample 1.
