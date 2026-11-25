# Marco 2 — Representação e Validação: CSES Shortest Routes I (Problema 1671)

**Data de criação:** 18/11/2026  
**Problema:** CSES Problem Set — Shortest Routes I

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:-------|:-----------|:------------------------------------------------------------------------------------------------|:------|
| 2.0 | 18/11/2026 | Justificativa da lista de adjacência, representação da instância do Marco 1, conferência manual da saída e classificação preliminar do problema. | E |
| 2.1 | 23/11/2026 | Inclusão da justificativa de escolha do algoritmo e análise de complexidade. | E |
| 2.2 | 25/11/2026 | Adequação ao escopo do Marco 2 no T3: ajuste do título, inclusão do cálculo de espaço da matriz de adjacência, nota sobre indexação `1..N` e remoção da escolha detalhada/complexidade (consolidadas no Marco 3). | E |

---

## 1. Representação Computacional

O grafo será armazenado em uma **lista de adjacência**. Para cada cidade `a` (indexada diretamente de `1` a `n`, acompanhando a numeração da entrada sem necessidade de deslocar índices para `0..n-1`), sua lista contém os pares `(b, c)` de voos que saem de `a` e chegam a `b` com comprimento `c`.

Essa escolha preserva explicitamente o sentido de cada voo, seu peso e eventuais voos paralelos. Como $n \le 10^5$ e $m \le 2 \cdot 10^5$, uma matriz de adjacência exigiria $n^2 = 10^{10}$ células — inviável em memória e tempo de inicialização. A lista de adjacência armazena apenas as cidades e as arestas que existem, usando espaço proporcional a $n + m$, e permite percorrer diretamente todos os voos que partem de uma cidade.

---

## 2. Representação da Instância do Marco 1

**Entrada:**

```text
4 5
1 2 6
1 3 2
3 2 1
2 4 2
3 4 10
```

**Lista de adjacência:**

| Cidade de origem | Voos de saída `(destino, comprimento)` |
|---:|---|
| 1 | `(2, 6)`, `(3, 2)` |
| 2 | `(4, 2)` |
| 3 | `(2, 1)`, `(4, 10)` |
| 4 | nenhum |

Por exemplo, `(3, 2)` na lista da cidade 1 significa que existe um voo de 1 para 3 com comprimento 2. Não se cria uma aresta inversa automaticamente.

---

## 3. Validação da Instância e da Saída Esperada

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

**Saída esperada, na ordem das cidades 1, 2, 3 e 4:**

```text
0 3 2 5
```

---

## 4. Critérios de Validação

Uma validação da implementação deverá conferir que:

- são lidos `n`, `m` e exatamente `m` descrições de voos;
- cada voo mantém a direção e o comprimento apresentados na entrada;
- são impressos exatamente `n` valores na ordem das cidades;
- a origem tem distância 0 e os demais valores coincidem com as menores somas de comprimentos;
- valores de distância usam precisão suficiente para os limites do problema.

---

## 5. Classificação Preliminar do Problema

Com base na modelagem e na representação validadas acima, o problema pertence à família de **caminhos mínimos com origem única** (*Single-Source Shortest Paths*):

- **Origem única:** todas as distâncias são calculadas a partir da cidade `1`.
- **Grafo direcionado:** os voos são de mão única (`a → b`).
- **Pesos estritamente positivos:** $1 \le c \le 10^9$ em todas as arestas.
- **Arestas paralelas permitidas:** múltiplos voos entre o mesmo par ordenado podem existir na entrada.

A escolha formal do algoritmo, a comparação com outras famílias de problemas em grafos e a análise de complexidade de pior caso são desenvolvidas no **Marco 3**.