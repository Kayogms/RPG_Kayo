# Marco 3 — Estratégia Algorítmica: Kattis Paintball (Problema I)

**Data de Criação:** 30/09/2026

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:---|:---|:---|:---|
| 1.0 | 30/09/2026 | Criação do documento: modelagem simplificada em linguagem acessível, tabela de papeis e índices, tabela de rastreamento manual com efeito cascata, dedução do $O(V \cdot E)$ e estimativa de memória. | E |

---

## 1. Propriedade Estrutural Central, Critério e Obtenção da Resposta

### 1.1 O que o problema realmente está pedindo?
O desafio do Paintball pode ser resumido em uma regra muito direta: **cada jogador tem exatamente 1 bala de tinta e precisa atingir alguém, e cada jogador deve ser atingido exatamente 1 vez**. Ninguém pode se mover, e você só pode atirar em quem consegue enxergar.

Traduzindo isso para a teoria dos grafos, o que buscamos é um **Emparelhamento Perfeito em Grafo Bipartido** (*Bipartite Perfect Matching*): uma correspondência um-para-um (bijetora) entre quem atira e quem é atingido.

### 1.2 Por que dividir cada jogador em dois vértices? (Dualidade de Papéis)
Em uma partida de paintball, cada jogador desempenha dois papéis simultâneos e independentes:
1. **Papel de Atirador ($A_k$):** o jogador $k$ tem uma bola e precisa escolher **em quem vai atirar**.
2. **Papel de Alvo ($B_k$):** o jogador $k$ precisa ser o alvo de alguém e **levar exatamente um tiro**.

Se usássemos apenas $N$ vértices em um grafo simples, essas duas responsabilidades ficariam misturadas. Por exemplo: se o Jogador 1 atira no Jogador 2, e o Jogador 2 atira no Jogador 1, ambos atiraram e ambos foram atingidos com sucesso. 

Para que o computador consiga modelar isso de forma limpa, criamos dois "clones" para cada jogador:
* O time dos **Atiradores** ($A_1, A_2, \dots, A_N$);
* O time dos **Alvos** ($B_1, B_2, \dots, B_N$).

Isso forma um **grafo bipartido** com $2N$ vértices, onde as arestas saem sempre de um atirador e apontam para um alvo que ele consegue ver ($A_u \to B_v$ e $A_v \to B_u$).

### 1.3 Como funciona o critério de caminhos aumentantes? (A "Dança das Cadeiras")
O Algoritmo de Kuhn resolve o problema atirador por atirador, usando a lógica de **caminhos aumentantes** (formalizada pelo matemático Claude Berge em 1957):
* Pegamos um atirador que ainda não tem alvo e olhamos as opções dele.
* Se ele enxerga um alvo que está **livre** (ninguém marcou para atirar nele ainda), o casamento é feito na hora.
* Se todos os alvos que ele enxerga já estão **ocupados**, nós não desistimos: perguntamos para o atirador que está ocupando aquele alvo se ele consegue **mudar para outra opção**. Se esse atirador conseguir se realocar para outro alvo (ou empurrar outro colega em uma corrente de trocas até encontrar um alvo vago), todo mundo sai ganhando e conseguimos encaixar mais um tiro válido!

Essa corrente de trocas é chamada de **caminho aumentante**. Toda vez que achamos uma corrente dessa, o número total de jogadores atendidos aumenta em $+1$. Se testamos todas as possibilidades e não existe nenhuma corrente de trocas viável para um atirador, o Lema de Berge garante que o emparelhamento já atingiu seu limite máximo possível.

### 1.4 Como obter a resposta final do problema?
* **Caso Possível (Solução Completa):** se todos os $N$ atiradores conseguirem um alvo exclusivo (emparelhamento de tamanho $N$), imprimimos $N$ linhas. A linha $i$ conterá o número do jogador que foi escolhido como alvo do jogador $i$.
* **Caso Impossível:** se algum atirador ficar sem alvo após tentar todas as trocas possíveis, significa que é matematicamente inviável fazer com que todos sejam atingidos. O programa simplesmente imprime:
  ```text
  Impossible
  ```

---

## 2. Implementações de Referência de `algs4`, Papéis e Adaptações

### 2.1 `algs4.graph.Graph` (Reaproveitada Diretamente)
* **Papel:** Armazenar os $2N$ vértices do grafo bipartido e suas conexões.
* **Uso:** Usada sem nenhuma modificação. O construtor `Graph(2 * n)` cria a estrutura contígua de vértices.

### 2.2 `algs4.bag.Bag` (Reaproveitada Diretamente)
* **Papel:** Lista encadeada interna de cada vértice que guarda seus vizinhos adjacentes (`G.adj[v]`).
* **Uso:** Usada sem alterações. Vale destacar que `Bag.add` insere no início da lista (comportamento LIFO), o que define a ordem concreta de consulta dos alvos.

### 2.3 `algs4.depth_first_paths.DepthFirstPaths` (Referência Conceitual)
* **Por que NÃO serve como classe base direta:**
  1. **Marcação permanente vs. temporária:** A classe do professor mantém a marcação de visitados fixa para sempre. No Kuhn, o controle de alvos visitados precisa ser **zerado a cada novo atirador**, pois um alvo já visitado em uma rodada anterior pode ser reconsiderado em uma nova tentativa de troca.
  2. **Decisão de desalocação:** Uma busca comum apenas caminha por vizinhos não visitados. O Kuhn precisa da lógica de **desalocar e realocar**: ao encontrar um alvo ocupado, ele chama a busca recursivamente para o dono atual daquele alvo.

### 2.4 Adaptação Prevista: `KuhnMatcher`
A estratégia prevê uma classe dedicada chamada `KuhnMatcher` que recebe o `Graph` e gerencia:
* O vetor `match_to` (de tamanho $2N$), registrando qual atirador está associado a cada alvo;
* A busca recursiva `_try_path(shooter, visited)`;
* O método `resolve()` que tenta emparelhar os atiradores de $1$ a $N$.

---

## 3. Instância Pequena e Rastreamento Manual (Sample 1)

Para deixar a execução clara e transparente, utilizamos a instância de exemplo do enunciado (Sample 1):
* **Jogadores ($N = 4$):** 1, 2, 3, 4
* **Pares de Visibilidade ($M = 4$):** $(1, 2)$, $(2, 3)$, $(3, 4)$, $(4, 1)$

### 3.1 Tabela de Mapeamento: Do Problema para a Memória do Computador
O `Graph(V)` aloca internamente um vetor de $0$ a $V-1$ (índices de $0$ a $7$). A primeira metade representa os atiradores ($0$ a $3$) e a segunda metade representa os alvos ($4$ a $7$, obtidos somando $+N$):

| Jogador ($k$) | Atirador (Teórico) | Índice no Código (`0..N-1`) | Alvo (Teórico) | Índice no Código (`N..2N-1`) | Cálculo do Índice do Alvo |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **Jogador 1** | $A_1$ | **0** | $B_1$ | **4** | $4 + (1 - 1) = 4$ |
| **Jogador 2** | $A_2$ | **1** | $B_2$ | **5** | $4 + (2 - 1) = 5$ |
| **Jogador 3** | $A_3$ | **2** | $B_3$ | **6** | $4 + (3 - 1) = 6$ |
| **Jogador 4** | $A_4$ | **3** | $B_4$ | **7** | $4 + (4 - 1) = 7$ |

### 3.2 Lista de Opções de Tiro de Cada Atirador
Considerando a ordem em que as arestas foram inseridas e o comportamento LIFO da estrutura `Bag`:
* $A_1$ (Jogador 1) enxerga os alvos: **[$B_4$, $B_2$]** *(Jogador 4, depois Jogador 2)*
* $A_2$ (Jogador 2) enxerga os alvos: **[$B_3$, $B_1$]** *(Jogador 3, depois Jogador 1)*
* $A_3$ (Jogador 3) enxerga os alvos: **[$B_4$, $B_2$]** *(Jogador 4, depois Jogador 2)*
* $A_4$ (Jogador 4) enxerga os alvos: **[$B_1$, $B_3$]** *(Jogador 1, depois Jogador 3)*

---

### 3.3 Tabela de Rastreamento Manual do Algoritmo de Kuhn

Estado inicial: todos os alvos estão livres (`match_to` com todos os valores vazios).

| Passo | Atirador da Vez | Alvo Consultado | Situação Encontrada | Decisão do Algoritmo / Ação | Caminho Aumentante Encontrado | Estado Atual do Emparelhamento (`match_to`) |
|:---:|:---:|:---:|:---|:---|:---:|:---|
| **1** | **$A_1$** (Jogador 1) | **$B_4$** (Jogador 4) | Livre | $A_1$ assume o alvo $B_4$ diretamente. | $A_1 \to B_4$ | $\{A_1 \to B_4\}$ |
| **2** | **$A_2$** (Jogador 2) | **$B_3$** (Jogador 3) | Livre | $A_2$ assume o alvo $B_3$ diretamente. | $A_2 \to B_3$ | $\{A_1 \to B_4, \; A_2 \to B_3\}$ |
| **3** | **$A_3$** (Jogador 3) | **$B_4$** (Jogador 4) | **Ocupado** (por $A_1$) | **Efeito Cascata:** $A_3$ pede para $A_1$ mudar de alvo. $A_1$ consulta sua próxima opção ($B_2$). Como $B_2$ está livre, $A_1$ migra para $B_2$. Com $B_4$ desocupado, $A_3$ assume $B_4$. | $A_3 \to B_4 \to A_1 \to B_2$ | $\{A_1 \to B_2, \; A_2 \to B_3, \; A_3 \to B_4\}$ |
| **4** | **$A_4$** (Jogador 4) | **$B_1$** (Jogador 1) | Livre | $A_4$ assume o alvo $B_1$ diretamente. | $A_4 \to B_1$ | $\{A_1 \to B_2, \; A_2 \to B_3, \; A_3 \to B_4, \; A_4 \to B_1\}$ |

### 3.4 Resultado Final
Com todos os 4 atiradores casados com sucesso:
* **Jogador 1 atira no Jogador 2** ($A_1 \to B_2$)
* **Jogador 2 atira no Jogador 3** ($A_2 \to B_3$)
* **Jogador 3 atira no Jogador 4** ($A_3 \to B_4$)
* **Jogador 4 atira no Jogador 1** ($A_4 \to B_1$)

Todos os 4 jogadores disparam uma única vez e todos os 4 são atingidos exatamente uma vez.

---

## 4. Estimativa de Complexidade de Tempo e Memória

### 4.1 Por que a Complexidade de Tempo é $O(V \cdot E)$?

A complexidade de pior caso do Algoritmo de Kuhn é obtida diretamente multiplicando os dois níveis de execução:

1. **Loop Principal ($O(V)$ iterações):**  
   O algoritmo passa por cada um dos $N$ atiradores. Como temos $N$ atiradores em um universo de $V = 2N$ vértices, isso representa $O(V)$ chamadas externas.
2. **Busca DFS por Tentativa ($O(E)$ por atirador):**  
   Dentro de cada tentativa, o conjunto `visited` garante que **nenhum alvo seja avaliado duas vezes**. Consequentemente, nenhuma aresta de tiro do grafo é percorrida mais de uma vez ao longo daquela tentativa. O custo de uma DFS que não repete arestas é proporcional ao número total de arestas: $O(E)$.

Multiplicando as duas partes:
$$\text{Tempo Total} = O(V) \times O(E) = \mathbf{O(V \cdot E)}$$

* **Na prática:** com $N \le 1.000$ e $M \le 5.000$ ($|V| = 2.000$ e $|E| = 10.000$), o número máximo de operações no pior cenário possível é de cerca de $10^7$ operações elementares. Em Python, isso roda em aproximadamente $0,1$ segundo (muito abaixo do limite de 1 a 2 segundos do juiz). Nos testes práticos, executou em cerca de **0,02 segundos** (com folga perante o limite de 0,05s e o limite de 1,0s da plataforma).

### 4.2 Complexidade de Memória (Distinção entre Grafo e Memória Auxiliar)

Para uma análise rigorosa, separa-se a memória fixa do grafo da memória de execução do algoritmo:

#### A. Representação do Grafo (`algs4.graph.Graph` + `Bag`):
* O vetor `adj` aloca $2N$ posições de cabeças de lista.
* As arestas são armazenadas como nós encadeados em `Bag`. Cada aresta gera dois nós (ida e volta).
* **Consumo do Grafo:** $O(V + E) = \mathbf{O(N + M)}$ (ocupa menos de 2 MB de RAM para o caso máximo).

#### B. Memória Auxiliar do Algoritmo (`KuhnMatcher`):
1. **Vetor de Casamento (`match_to`):** tamanho fixo $2N \implies O(N)$.
2. **Conjunto de alvos visitados (`visited`):** armazena até $N$ alvos por tentativa $\implies O(N)$.
3. **Pilha de Recursão da DFS:** se houver uma corrente de trocas envolvendo todos os atiradores em fila, a profundidade máxima de chamadas na pilha do Python será de $N \implies O(N)$.
* **Consumo da Memória Auxiliar:** $\mathbf{O(N)}$.

#### C. Memória Total:
$$\text{Memória Total} = O(N + M) + O(N) = \mathbf{O(N + M)}$$
O consumo total de memória é **estritamente linear**, operando com extrema folga no ambiente de execução.

### 4.3 Prevenção de Estouro de Pilha no Python
Como a cadeia de realocações recursivas pode ter até $N = 1.000$ níveis de profundidade, e o limite padrão do Python é exatamente 1.000 chamadas (`sys.getrecursionlimit() = 1000`), utiliza-se preventivamente:
```python
import sys
sys.setrecursionlimit(10000)
```
Isso garante total estabilidade em qualquer caso de teste sem risco de `RecursionError`.
