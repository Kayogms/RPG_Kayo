# Marco 2 — Representação e validação: CSES Shortest Routes I

**Data de criação:** 18/11/2026  
**Problema:** CSES Problem Set — Shortest Routes I

## Histórico de versões

| Versão | Data | Descrição das alterações | Grupo |
|---|---|---|---|
| 2.0 | 18/11/2026 | Justificativa da lista de adjacência, representação da instância do Marco 1, conferência manual da saída e classificação preliminar do problema. | E |

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

## 5. Classificação preliminar

O problema pertence à família de **caminho mínimo**: pede as menores distâncias a partir de uma única origem, em um grafo dirigido com pesos positivos. Não é um problema de árvore geradora mínima nem de fluxo. A classificação e a instância validada orientam a escolha do algoritmo nos marcos posteriores.
