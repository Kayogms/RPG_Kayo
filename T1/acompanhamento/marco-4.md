# Marco 4 — Aplicação básica de BFS e conclusão: Ladder Takahashi (Problema I)

**Data de Criação:** 18 de Agosto de 2026  

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo   |
| :--- | :--- | :--- |:--------|
| 1.0 | 18/08/2026 | Criação do documento e estrutura inicial | F |
| 2.0 | 19/08/2026 | Reescrita da implementação: BFS reaproveitada sem alterações de `algs4.breadth_first_paths.BreadthFirstPaths`; validação cruzada passa a incluir DFS (Marco 3), UF e CC; justificativa da escolha da BFS passa a citar evidência empírica (`RecursionError`) em vez de apenas argumento teórico | F |

---

## 1. Execução Manual da BFS (Sample 1)

**Ponto de Partida:** Vértice 1 (Andar 1), representado internamente pelo índice comprimido `0` (via `LadderSymbolGraph`).

**Passo a Passo da Travessia:**

A fila inicia com `[1]` (índice `0`). Desenfileira `1`, enfileira `4`. Desenfileira `4`, enfileira `3` e `10`. Desenfileira `3`, enfileira `8`. Desenfileira `10`. Desenfileira `8`. Fila vazia — fim da exploração.

Essa travessia é executada integralmente pela classe **`algs4.breadth_first_paths.BreadthFirstPaths`**, sem nenhuma modificação em sua lógica interna (`_marked[]`, `edge_to[]`, `deque`). A adaptação ao problema ocorre **fora** da classe: a função `maior_andar_via_bfs` (em `marco4_bfs.py`) percorre o vetor de alcançabilidade (`has_path_to`) já calculado pela BFS e extrai o maior andar (convertendo cada índice de volta ao valor original via `LadderSymbolGraph.name`).

---

## 2. Níveis, Distâncias e Predecessores

| Andar | Nível (Distância) | Predecessor |
| :---: | :---: | :---: |
| 1 | 0 | `None` |
| 4 | 1 | 1 |
| 3 | 2 | 4 |
| 10 | 2 | 4 |
| 8 | 3 | 3 |

*(Níveis e predecessores obtidos diretamente do atributo `edge_to` de `BreadthFirstPaths`, já traduzidos de índice comprimido para andar original.)*

### 2.1 Validação Cruzada com DFS, UF e CC (Oráculos)

O valor de `maior_andar` obtido pela BFS foi comparado com os resultados já validados no Marco 3 (DFS, via `ValidadorDFS`) e com os dois oráculos estruturais independentes do pacote `algs4`: **UF** (Union-Find) e **CC** (Connected Components). Diferentemente da versão anterior deste documento (que comparava apenas BFS x DFS x DSU), a validação atual é **quádrupla**:

| Método | Maior andar alcançável |
| :---: | :---: |
| BFS | 10 |
| DFS | 10 |
| UF | 10 |
| CC | 10 |

**Saída real da validação (`ValidadorBFS.validar`, em `marco4_bfs.py`):**

```
=== Execução da BFS ===
Origem:                 1
Maior andar (BFS):      10

=== Comparação BFS x DFS x UF x CC ===
BFS -> maior andar alcançável: 10
DFS -> maior andar alcançável: 10
UF  -> maior andar alcançável: 10
CC  -> maior andar alcançável: 10
[OK] Todos os métodos concordam: resposta = 10
```

---

## 3. Comparação entre DFS e BFS

A DFS explora o grafo mergulhando no ramo mais profundo antes de retroceder (*backtracking*), o que é ideal para buscar caminhos longos. A BFS explora o grafo em camadas (níveis), processando todos os vizinhos imediatos antes de avançar, sendo ideal para encontrar distâncias mínimas em grafos não ponderados.

Nas implementações de referência utilizadas (`algs4`), essa diferença também se reflete na forma de controle de execução: `DepthFirstPaths` (base de `LadderDFS`, Marco 3) é **recursiva**, enquanto `BreadthFirstPaths` é **iterativa**, controlada por uma fila (`collections.deque`).

---

## 4. Escolha Justificada

Ambas resolvem o problema de conectividade, mas a **BFS foi escolhida para a submissão final**. Diferentemente da versão anterior deste documento — que apresentava essa escolha apenas como argumento teórico ("garante segurança contra limites de recursão profunda que **poderiam** ocorrer") —, esta versão apresenta **evidência empírica direta**, obtida em teste de estresse (ver Marco 3, Seção 4):

* Uma entrada com $N = 2\times10^5$ escadas formando uma cadeia (`1-2, 2-3, 3-4, ..., N-(N+1)`) foi submetida a `LadderDFS` (recursiva) e resultou em:
  ```
  RecursionError confirmado: maximum recursion depth exceeded
  ```
* A mesma entrada, submetida a `resolver_para_submissao` (que usa `BreadthFirstPaths`, iterativa via `deque`), foi resolvida corretamente e com folga de tempo:
  ```
  200001
  tempo: 0.61 s
  ```

O processamento em camadas em uma fila iterativa é, portanto, não apenas teoricamente mais seguro, mas **comprovadamente necessário** para garantir corretude dentro do limite $N = 2\times10^5$ especificado nas restrições do problema (Marco 1).

---

## 5. Adaptação e Integração

A BFS de referência (`BreadthFirstPaths`) foi utilizada **sem nenhuma modificação em sua lógica interna**. A adaptação ao problema foi feita inteiramente por fora da classe, em uma função auxiliar que percorre o resultado já calculado e extrai o maior andar:

```python
def maior_andar_via_bfs(G: Graph, sg: LadderSymbolGraph, origem_idx):
    bfs = BreadthFirstPaths(G, origem_idx)
    maior = sg.name(origem_idx)
    for v in range(G.V):
        if bfs.has_path_to(v):
            maior = max(maior, sg.name(v))
    return maior, bfs
```

A solução foi integrada usando a mesma representação de grafo dos marcos anteriores: `algs4.graph.Graph` (construído por `LadderSymbolGraph`, que também resolve a compressão de coordenadas dos andares).

**Trecho de Código Integrado (`marco4_bfs.py`):**

```python
class ValidadorBFS:
    @staticmethod
    def validar(sg: LadderSymbolGraph, edges, origem=1, maior_dfs=None):
        G = sg.graph()
        origem_idx = sg.index(origem)

        maior_bfs, _ = maior_andar_via_bfs(G, sg, origem_idx)

        maior_uf = maior_andar_via_uf(edges, sg, origem_idx)
        maior_cc = maior_andar_via_cc(G, sg, origem_idx)

        valores = {maior_bfs, maior_uf, maior_cc}
        if maior_dfs is not None:
            valores.add(maior_dfs)

        assert len(valores) == 1, f"Divergência entre métodos! Valores: {valores}"
        return maior_bfs
```

---

## 6. Testes e Complexidade

O resultado da BFS foi validado cruzando-o simultaneamente com a DFS (Marco 3), UF e CC, conforme demonstrado na Seção 2.1. A complexidade final de tempo e espaço manteve-se em $O(V + E)$, garantindo eficiência ótima para o problema, com $|V| \le 2N+1$ e $|E| = N \le 2\times10^5$.

Adicionalmente, foi realizado um **teste de estresse** com $N = 2\times10^5$ escadas em formato de cadeia (pior caso estrutural para profundidade de recursão), confirmando que a solução de submissão (BFS) resolve o caso em aproximadamente **0,61 segundos**, dentro dos limites aceitáveis de tempo de execução do AtCoder.

---

## 7. Submissão

O código integrado com a BFS foi submetido na plataforma **AtCoder** e recebeu o veredito **`Accepted`** (evidência salva na pasta `evidencias/accepted.png`).

**Código de submissão final (`marco4_bfs.py` — `resolver_para_submissao`):**

```python
def resolver_para_submissao(origem=1):
    edges = LeitorEntrada.ler()
    sg = LadderSymbolGraph(edges, vertice_partida=origem)
    G = sg.graph()
    origem_idx = sg.index(origem)
    maior, _ = maior_andar_via_bfs(G, sg, origem_idx)
    print(maior)
```

---

## 8. Ensaio da Apresentação

Registro do ensaio da exposição oral (até 5 minutos), conforme roteiro do trabalho:

| Slide | Conteúdo | Tempo alvo |
| :---: | :--- | :---: |
| Capa | Identificação do grupo e do problema | — |
| 1 | Problema (Ladder Takahashi) | 1 min |
| 2 | Modelagem (Marco 1) | 1 min |
| 3 | Representação computacional (Marco 2) | 1 min |
| 4 | DFS/BFS (Marcos 3 e 4), incluindo o achado do `RecursionError` como evidência prática da escolha da BFS | 1 min |
| 5 | Validação (`Accepted`) | 1 min |

*Observação: preencher com data do ensaio e ajustes identificados após a prática cronometrada.*
