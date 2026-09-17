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

- **Vértices ($V$):** conjunto $A$ (jogadores como *atiradores*) $\cup$ conjunto $B$ (jogadores como *alvos*). $|V| = 2N$ (até 2.000).
- **Arestas ($E$):** para cada par de visibilidade $(x, y)$ da entrada — que é mútuo — criam-se duas possibilidades de tiro: $x \to y$ (aresta $x_A \to y_B$) e $y \to x$ (aresta $y_A \to x_B$). $|E| = 2M$ (até 10.000).
- **Tipo de grafo:** bipartido (arcos só de $A$ para $B$), não ponderado, simples (sem laços nem arestas paralelas).

**Relação com o problema:** encontrar o alvo de cada jogador equivale a encontrar um **Emparelhamento Máximo** neste grafo bipartido. Se o tamanho do emparelhamento for igual a $N$ (emparelhamento perfeito), todos atiram e todos são atingidos — a resposta é a atribuição correspondente. Caso contrário, a resposta é `Impossible`.

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

**Estratégia de resolução:** o emparelhamento máximo em grafo bipartido é resolvido pelo **Algoritmo de Kuhn**, que usa DFS para buscar **caminhos aumentantes**:

1. Para cada atirador ainda sem alvo, tenta-se uma DFS entre seus vizinhos (alvos que ele enxerga).
2. Se um alvo estiver livre, o emparelhamento é feito imediatamente.
3. Se o alvo já estiver ocupado por outro atirador, a DFS tenta **realocar recursivamente** esse atirador anterior para um alvo alternativo, liberando espaço para o atual.
4. Se todos os $N$ atiradores forem emparelhados, imprime-se a atribuição; senão, `Impossible`.

**Complexidade esperada:** $O(V \cdot E)$ — com $V \le 2000$ e $E \le 10\,000$, o pior caso fica na casa dos milhões de operações, dentro do limite de tempo padrão.

### Avaliação do reaproveitamento das classes de referência do professor

Nem toda classe do pacote `algs4` se aplica diretamente aqui — vale registrar essa avaliação explicitamente, já que o Algoritmo de Kuhn não é uma das buscas "prontas" da Unidade I:

| Classe do professor | Reaproveitável neste problema? | Justificativa |
|---|---|---|
| `Graph` (`algs4.graph.Graph`) | **Sim, com ressalva.** | Pode representar o grafo bipartido: `Graph(2N)`, indexando atiradores em `0..N-1` e alvos em `N..2N-1`, com `add_edge` para cada visibilidade. Ressalva: por ser pensada para grafos **não direcionados**, `add_edge` registra a aresta nos dois sentidos — inclusive de alvo para atirador, sentido que o algoritmo de Kuhn nunca percorre. Isso não quebra a lógica (o excesso de arestas simplesmente não é usado), mas é preciso documentar essa diferença de uso pretendido vs. real. |
| `Bag` (`algs4.bag.Bag`) | **Sim.** | É a estrutura interna de `Graph`, reaproveitada automaticamente junto com ela. |
| `DepthFirstPaths` (`algs4.depth_first_paths.DepthFirstPaths`) | **Não diretamente — precisa de reformulação, não apenas adaptação pontual.** | A DFS de referência resolve "quem é alcançável a partir de uma única origem fixa" com um `marked[]` **global e permanente**. O Algoritmo de Kuhn precisa de algo estruturalmente diferente: (1) o vetor de "visitados" deve ser **reiniciado a cada novo atirador tentado** (não é uma única busca global); (2) a recursão não decide "para onde ir" olhando só quem não foi visitado — ela decide se **vale a pena desalocar** o emparelhamento atual de um alvo ocupado; (3) a função precisa **retornar sucesso/falha** (booleano), algo que `has_path_to` não faz durante a busca, só depois de pronta. Por isso, a implementação usará o mesmo *padrão* recursivo com `marked[]` como base conceitual, mas a lógica de decisão dentro da recursão será escrita do zero para este problema. |
| `BreadthFirstPaths`, `UF`, `CC` | **Não aplicável.** | Resolvem alcançabilidade por níveis, conectividade e componentes conexas — nenhuma dessas perguntas corresponde ao que o problema exige (emparelhamento exclusivo, não alcançabilidade nem agrupamento). |

**Conclusão da avaliação:** `Graph`/`Bag` serão reaproveitadas como estrutura de dados do grafo bipartido. A busca em si (Algoritmo de Kuhn) será uma implementação nova, que se inspira no padrão recursivo de marcação da `DepthFirstPaths`, mas não é uma adaptação incremental dela — a lógica de decisão da recursão é fundamentalmente outra. Essa distinção será detalhada e implementada no Marco 2/3, quando o critério algorítmico completo for formalizado.