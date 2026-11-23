# Marco 2 — Escolha do algoritmo: CSES Shortest Routes I

**Data de criação:** 18/11/2026  
**Problema:** CSES Problem Set — Shortest Routes I

## Histórico de versões

| Versão | Data | Descrição das alterações | Grupo |
|---|---|---|---|
| 2.0 | 18/11/2026 | Justificativa da lista de adjacência, representação da instância do Marco 1, conferência manual da saída e classificação preliminar do problema. | E |
| 2.1 | 23/11/2026 | Inclusão da justificativa de escolha do algoritmo (Dijkstra vs. Kruskal/Prim e Ford-Fulkerson/Edmonds-Karp) e da análise de complexidade de pior caso de tempo e espaço. | E |

## 1. Representação computacional

O grafo será armazenado em uma **lista de adjacência**. Para cada cidade `a`, sua lista contém os pares `(b, c)` de voos que saem de `a` e chegam a `b` com comprimento `c`.

Essa escolha preserva explicitamente o sentido de cada voo e seu peso. Como o número de voos é limitado a `2·10⁵`, a estrutura armazena apenas as cidades e as arestas que existem, usando espaço proporcional a `n + m`. Ela também permite percorrer diretamente todos os voos que partem de uma cidade.

## 2. Representação da instância do Marco 1

Entrada:

```text
4 5
1 2 6
1 3 2
3 2 1
2 4 2
3 4 10
```

Lista de adjacência:

| Cidade de origem | Voos de saída `(destino, comprimento)` |
|---:|---|
| 1 | `(2, 6)`, `(3, 2)` |
| 2 | `(4, 2)` |
| 3 | `(2, 1)`, `(4, 10)` |
| 4 | nenhum |

Por exemplo, `(3, 2)` na lista da cidade 1 significa que existe um voo de 1 para 3 com comprimento 2. Não se cria uma aresta inversa automaticamente.

## 3. Validação da instância e da saída esperada

### Verificação do formato

- A primeira linha informa `n = 4` e `m = 5`.
- Há exatamente cinco linhas de voos.
- Os extremos de cada voo estão entre 1 e 4.
- Todos os comprimentos respeitam o limite e são positivos.
- A partir da cidade 1 é possível chegar às cidades 2, 3 e 4.

### Conferência manual das distâncias

- **Cidade 1:** distância zero, pois a origem já está na própria cidade.
- **Cidade 2:** o voo direto custa 6; pela rota `1 → 3 → 2`, o custo é `2 + 1 = 3`. A menor distância é 3.
- **Cidade 3:** a rota `1 → 3` custa 2. A menor distância é 2.
- **Cidade 4:** pela rota `1 → 3 → 2 → 4`, o custo é `2 + 1 + 2 = 5`. Outras alternativas informadas custam 8 (`1 → 2 → 4`) e 12 (`1 → 3 → 4`). A menor distância é 5.

Saída esperada, na ordem das cidades 1, 2, 3 e 4:

```text
0 3 2 5
```

## 4. Critérios de validação

Uma validação da implementação deverá conferir que:

- são lidos `n`, `m` e exatamente `m` descrições de voos;
- cada voo mantém a direção e o comprimento apresentados na entrada;
- são impressos exatamente `n` valores na ordem das cidades;
- a origem tem distância 0 e os demais valores coincidem com as menores somas de comprimentos;
- valores de distância usam precisão suficiente para os limites do problema.

## 5. Classificação e escolha do algoritmo

O problema pertence à família de **caminho mínimo com origem única**: pede as menores distâncias saindo da cidade 1 até todas as outras, em um **grafo direcionado** (voos de mão única) e com **pesos positivos** (`c ≥ 1`).

Com base nessa classe, o algoritmo escolhido é o **Algoritmo de Dijkstra** (com lista de adjacência e fila de prioridade mínima):

- **Por que usar Dijkstra:** ele foi feito exatamente para encontrar o menor caminho a partir de uma única origem quando não há pesos negativos. A ideia é simples: começamos na cidade 1 com distância 0 e, a cada passo, escolhemos a cidade ainda não finalizada que tem a menor distância acumulada conhecida; em seguida, testamos todos os voos que saem dela para tentar melhorar (*relaxar*) a distância das cidades vizinhas. Como todos os pesos são positivos, quando uma cidade é escolhida da fila, não existe outro caminho passando por cidades futuras que possa deixá-la mais barata.
- **Por que não usar Kruskal ou Prim:** esses algoritmos resolvem problemas de **árvore geradora mínima**, ou seja, conectar todos os vértices de um grafo não direcionado gastando o menor custo total somado na rede inteira. Nosso objetivo não é ligar todas as cidades com a menor soma global de arestas, e sim achar a menor distância individual da cidade 1 até cada destino, respeitando o sentido único dos voos.
- **Por que não usar Ford-Fulkerson ou Edmonds-Karp:** esses algoritmos resolvem problemas de **fluxo máximo**, em que as arestas têm capacidades (por exemplo, quantos passageiros passam por um voo) e se quer enviar o maior volume possível de uma origem a um destino. Aqui as arestas representam distâncias a minimizar, não limites de capacidade.

## 6. Complexidade de pior caso (tempo e espaço)

Considerando `n` cidades (vértices) e `m` voos (arestas), usando **lista de adjacência** e **fila de prioridade mínima (heap binário)**:

### Tempo no pior caso: `O((n + m) log n)`

- **Leitura e montagem do grafo:** ler as `m` linhas e preencher as `n` listas de adjacência leva tempo `O(n + m)`.
- **Processamento dos vértices e arestas:** cada cidade é finalizada e tem seus voos de saída percorridos no máximo uma vez; ao todo, todas as `m` arestas são examinadas em tempo `O(n + m)`.
- **Uso da fila de prioridade:** no pior caso, cada voo que melhora a distância de um destino gera uma inserção ou atualização na fila de prioridade, o que custa `O(log n)` por operação (mesmo usando uma fila padrão sem remoção de entradas antigas, o tamanho do heap fica limitado a `m ≤ n²`, mantendo o custo logarítmico em `O(log n)`).
- **Total:** `O((n + m) log n)` no pior caso. Como todas as cidades são alcançáveis a partir da origem (`m ≥ n - 1`), isso também pode ser escrito como `O(m log n)`. Para `n ≤ 10⁵` e `m ≤ 2·10⁵`, o número de operações fica bem abaixo do limite de 1 segundo.

### Espaço no pior caso: `O(n + m)`

- **Lista de adjacência:** armazena `n` cabeçalhos de lista e exatamente `m` voos, usando `O(n + m)` de memória.
- **Vetor de distâncias (e controle de visitados):** armazena um valor por cidade, usando `O(n)`.
- **Fila de prioridade:** guarda no máximo `O(n)` elementos (em heap indexado) ou `O(m)` entradas no pior caso (em fila padrão com entradas desatualizadas).
- **Total:** `O(n + m)` no pior caso, o que cabe com folga no limite de 512 MB.
