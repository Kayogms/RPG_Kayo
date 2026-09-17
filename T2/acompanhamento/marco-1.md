# Marco 1 — Modelagem: Kattis Paintball (Problema I)

**Data de Criação:** 16/09/2026

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:-------|:-----------|:------------------------------------------------------------------------------------------------|:------|
| 1.0    | 16/09/2026 | Criação do documento, modelagem inicial e adaptação estrutural para o problema de emparelhamento | E     |
| 1.1    | 17/09/2026 | Simplificação do documento; unificação de seções redundantes; avaliação de reaproveitamento das classes de referência do professor na hipótese de solução | E |

---

## 1. Enunciado, Entrada, Saída e Restrições

**Enunciado:**

Marek e seus colegas terminaram a universidade e decidiram celebrar com uma partida de paintball. Após o jogo, cada jogador possui exatamente uma bala restante. Marek quer saber se é possível que **todos os jogadores sejam atingidos exatamente uma vez**, considerando que ninguém pode se mover, dado quem consegue ver quem (e, portanto, quem pode atirar em quem).

**Entrada:**

```
N M
u1 v1
u2 v2
...
uM vM
```

- $N$ = número de jogadores (numerados de 1 a $N$); $M$ = número de pares que se enxergam mutuamente.
- Cada uma das $M$ linhas seguintes contém um par $(u, v)$ que se enxerga.

**Saída:**

- `Impossible`, se não houver atribuição de alvos em que todos sejam atingidos.
- Caso contrário, $N$ linhas: a linha $i$ contém o alvo escolhido pelo jogador $i$. Havendo mais de uma solução, qualquer uma é aceita.

**Restrições:**

- $2 \le N \le 1\,000$
- $0 \le M \le 5\,000$
- $1 \le u, v \le N$, com $u \ne v$; cada par aparece no máximo uma vez.

**Observação central:** como cada jogador precisa de exatamente um alvo, e cada jogador precisa ser alvo de exatamente uma pessoa, o problema é, no fundo, encontrar um **Emparelhamento Perfeito** (*Bipartite Perfect Matching*) — não uma propriedade de alcançabilidade ou conectividade simples.

---

## 2. Vértices, Arestas e Tipo de Grafo

**Modelagem:** para transformar "cada jogador escolhe um alvo, e cada jogador é alvo de exatamente um atirador" em um problema de emparelhamento, cada jogador é dividido em duas cópias, formando um grafo bipartido:

- **Vértices ($V$):** conjunto $A$ (jogadores como *atiradores*) $\cup$ conjunto $B$ (jogadores como *alvos*). $\vert{}V\vert{} = 2N$ (até 2.000).
- **Arestas ($E$):** para cada par de visibilidade $(x, y)$ da entrada — que é mútuo — criam-se duas possibilidades de tiro: $x \to y$ (aresta $x_A \to y_B$) e $y \to x$ (aresta $y_A \to x_B$). $\vert{}E\vert{} = 2M$ (até 10.000).
- **Tipo de grafo:** bipartido (arcos só de $A$ para $B$), não ponderado, simples (sem laços nem arestas paralelas).

**Relação com o problema:** encontrar o alvo de cada jogador equivale a encontrar um **Emparelhamento Máximo** neste grafo bipartido. Se o tamanho do emparelhamento for igual a $N$ (emparelhamento perfeito), todos atiram e todos são atingidos — a resposta é a atribuição correspondente. Caso contrário, a resposta é `Impossible`.

**Resultado de aprendizagem aferido:** A resolução deste problema afere a capacidade de identificar, modelar e calcular **Emparelhamentos** (*Bipartite Matching*), aplicando conhecimentos estruturais avançados para estabelecer uma correspondência exclusiva entre dois conjuntos independentes.

---

## 3. Instância Pequena e Resultado Esperado

**Caso de teste (ciclo de 4 jogadores):**

```
4 4
1 2
2 3
3 4
4 1
```

**Matriz de adjacência bipartida (atiradores nas linhas, alvos nas colunas):**

| | Alvo 1 | Alvo 2 | Alvo 3 | Alvo 4 |
|:---|:---:|:---:|:---:|:---:|
| **Atirador 1** | 0 | 1 | 0 | 1 |
| **Atirador 2** | 1 | 0 | 1 | 0 |
| **Atirador 3** | 0 | 1 | 0 | 1 |
| **Atirador 4** | 1 | 0 | 1 | 0 |

**Resultado esperado:**

```
2
3
4
1
```

**Explicação:** o jogador 1 atira no 2, o 2 no 3, o 3 no 4, e o 4 no 1 — um ciclo de tamanho 4. Todos atiram exatamente uma vez e são atingidos exatamente uma vez, satisfazendo a condição do enunciado.

---

## 4. Hipótese Inicial de Solução

**Estratégia de Resolução Conceptual:**
Para resolver o problema de alocação exclusiva (onde cada atirador precisa de um alvo único e cada alvo só pode ser atingido por um atirador), a solução modelará o cenário como a busca por um **Emparelhamento Máximo em um Grafo Bipartido**. A estratégia central será utilizar o **Algoritmo de Kuhn**.

**O Papel da DFS (Busca de Caminhos Aumentantes):**
A Busca em Profundidade (DFS) atuará como o motor lógico para encontrar "caminhos aumentantes". O algoritmo iterará sobre cada atirador tentando associá-lo a um alvo. 
- Se o alvo desejado estiver livre, o emparelhamento é estabelecido imediatamente.
- Se o alvo desejado já estiver ocupado por outro jogador, a DFS fará uma exploração recursiva. Ela verificará se o atirador "dono" atual desse alvo pode ser realocado para um alvo alternativo que esteja livre (ou cujo dono também possa ser realocado). Esse processo de "desalocar e realocar" em cascata é o que permite aumentar o tamanho do emparelhamento iterativamente.

**Validação e Retorno:**
Ao final da execução para todos os atiradores, se o total de pareamentos bem-sucedidos for exatamente igual a $N$, alcançamos um Emparelhamento Perfeito. Imprimimos a atribuição resultante. Caso contrário, concluímos que é inviável e imprimimos `Impossible`.

**Complexidade Esperada:**
O Algoritmo de Kuhn utilizando DFS possui complexidade de tempo no pior caso de $O(V \cdot E)$. Como teremos $\vert{}V\vert{} \le 2000$ e $\vert{}E\vert{} \le 10000$, o número máximo de operações fica na casa dos milhões. Essa abordagem algorítmica é altamente eficiente e garante que a execução ocorrerá com folga dentro do limite de tempo da plataforma.

**Conclusão da avaliação:** `Graph`/`Bag` serão reaproveitadas como estrutura de dados do grafo bipartido. A busca em si (Algoritmo de Kuhn) será uma implementação nova, que se inspira no padrão recursivo de marcação da `DepthFirstPaths`, mas não é uma adaptação incremental dela — a lógica de decisão da recursão é fundamentalmente outra. Essa distinção será detalhada e implementada no Marco 2/3, quando o critério algorítmico completo for formalizado.