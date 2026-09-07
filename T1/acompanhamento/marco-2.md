# Marco 2 — Representação Computacional: Ladder Takahashi (Problema I)

**Data de Criação:** 15/08/2026

### Histórico de Versões

| Versão | Data       | Descrição das Alterações               | Grupo |
| :------ | :--------- | :----------------------------------------- | :---- |
| 1.0     | 15/08/2026 | Criação do documento e estrutura inicial | F     |
| 1.1     | 17/08/2026 | Simplificação                            | F     |

---

## 1. Escolha da Representação Computacional

**Estrutura de Dados Selecionada:**
Tabela de símbolos para compressão de coordenadas (`LadderSymbolGraph`) combinada com uma Lista de Adjacência nativa (`algs4.graph.Graph`, baseada em arrays de `algs4.bag.Bag`).

**Justificativa:**
Uma matriz de adjacência exigiria uma estrutura indexada pelo número do andar. Como os andares chegam a 10^9, isso resultaria em um estouro de memória (Memory Limit Exceeded). A solução é usar a **compressão de coordenadas**: um dicionário interno (tabela de símbolos) mapeia apenas os andares que aparecem na entrada para índices contínuos (de 0 até V-1). 
Após essa conversão, o grafo é instanciado usando vetores de listas encadeadas (`Bag`), o que resolve a esparsidade, garante consumo de memória proporcional apenas aos andares utilizados e mantém a complexidade de tempo em O(V + E), viabilizando o reuso direto dos algoritmos de busca e oráculos da biblioteca `algs4`.

---

## 2. Leitura da Entrada e Construção do Grafo

**Processo de Construção:**
1. A entrada é lida e convertida em um `numpy.array` matricial de shape (N, 2).
2. A classe `LadderSymbolGraph` itera sobre essa matriz. Se um andar ainda não possui índice, ele recebe o próximo ID sequencial disponível, salvo em um dicionário interno. O andar 1 é inserido forçadamente para garantir que a origem exista no grafo computacional.
3. Com o total de vértices distintos descoberto, a instância `algs4.graph.Graph` é inicializada.
4. O array é iterado novamente: para cada par (A, B) lido, a classe recupera os índices comprimidos (ex: u, v) e adiciona a aresta simetricamente, respeitando a natureza não direcionada do problema.

## 3. Medidas Estruturais (Unidade I)

**Análise do Grafo Construído (referente ao Sample 1):**

- **Número total de vértices instanciados ($|V|$):** 5 andares distintos foram instanciados no dicionário: $\{1, 3, 4, 8, 10\}$.
- **Número de arestas lidas ($|E|$):** 4 escadas foram lidas da entrada, correspondendo a $|E| = 4$ arestas no grafo.
- **Grau dos vértices ($d(v)$):**

| Andar (vértice) | Grau$d(v)$ | Vizinhos   |
| :--------------: | :----------: | :--------- |
|        1        |      1      | [4]        |
|        3        |      2      | [4, 8]     |
|        4        |      3      | [1, 3, 10] |
|        8        |      1      | [3]        |
|        10        |      1      | [4]        |

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
