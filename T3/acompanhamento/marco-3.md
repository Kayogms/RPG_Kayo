# Marco 3 — Escolha do Algoritmo: CSES Shortest Routes I (Problema 1671)

**Data de Criação:** 23/11/2026

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:-------|:-----------|:-------------------------------------------------------------------------------------------------------------------------------------------|:------|
| 1.0 | 23/11/2026 | Criação do documento: justificativa do Algoritmo de Dijkstra, condições de aplicabilidade, invariante, execução na instância e estimativa de complexidade | E |

---

## 1. Classe do Problema e Algoritmo Escolhido

O problema pede a menor distância da cidade 1 até todas as outras, em um grafo direcionado (voos de mão única) e com pesos positivos ($1 \le c \le 10^9$). Isso o coloca na classe de caminhos mínimos com origem única, e o algoritmo escolhido é o Algoritmo de Dijkstra.

A escolha fica clara ao comparar com as alternativas que o problema poderia sugerir:

| Alternativa | Pergunta que ela responde | Por que não serve aqui |
|:---|:---|:---|
| Busca em Largura (BFS) | Qual o menor número de arestas até cada vértice? | Ignora os pesos. Na instância deste documento, o voo direto $1 \to 2$ usa 1 aresta, mas custa 6; o caminho $1 \to 3 \to 2$ usa 2 arestas e custa apenas 3. |
| Bellman-Ford | Menores distâncias, aceitando pesos negativos. | Resolve o problema corretamente, mas custa $O(n \cdot m)$: com $n = 10^5$ e $m = 2\cdot10^5$, são cerca de $2\cdot10^{10}$ operações, muito acima do que cabe em 1 segundo. Como não há pesos negativos, esse custo extra não traz benefício. |
| Kruskal / Prim | Qual a árvore que liga todos os vértices com a menor soma total de arestas? | É um problema de rede inteira, não de distância individual. A árvore geradora mínima pode até ligar a cidade 1 a outra por um caminho longo, pois só minimiza o custo global. |
| Ford-Fulkerson / Edmonds-Karp | Qual o maior volume que passa de uma origem a um destino? | As arestas aqui são distâncias a minimizar, não capacidades a respeitar. |

---

## 2. Condições de Aplicabilidade

O Algoritmo de Dijkstra só é correto quando certas condições valem. A tabela confere cada uma contra o enunciado:

| Condição | Vale neste problema? | Evidência |
|:---|:---|:---|
| Todos os pesos são não negativos | Sim | $c \ge 1$ em toda aresta |
| Há uma única origem | Sim | A origem é sempre a cidade 1 |
| O grafo pode ser direcionado ou não | Sim | Os voos são de mão única; basta guardar cada aresta só no sentido do voo |
| Pode haver arestas paralelas | Sim | Cada voo entra com seu próprio peso; o de maior custo nunca melhora o de menor |
| Todos os vértices precisam ser alcançáveis | Garantido | O enunciado assegura que é possível chegar a todas as cidades, então não há distância infinita na saída |

### Por que a condição de pesos não negativos é indispensável

Considere 4 cidades com os voos $1 \to 2$ (peso 2), $1 \to 3$ (peso 3), $3 \to 2$ (peso $-2$) e $2 \to 4$ (peso 1). As menores distâncias reais a partir da cidade 1 são $0, 1, 3, 2$: chega-se a 2 por $1 \to 3 \to 2$ com custo $3 - 2 = 1$, e a 4 por esse mesmo caminho com custo 2.

O Dijkstra clássico, que finaliza cada cidade uma única vez, responde $0, 2, 3, 3$: finaliza a cidade 2 com distância 2 antes de conhecer o atalho pela cidade 3, e nunca mais a reavalia. O erro vem do peso negativo, que permite que um caminho mais longo em número de passos acabe mais barato. Como neste problema $c \ge 1$, isso não acontece, e a condição está satisfeita.

---

## 3. Operação Central e Invariante

### Operação central: o relaxamento de aresta

Para cada voo $u \to v$ de peso $c$, o relaxamento testa se passar por $u$ melhora a distância conhecida de $v$:

$$\text{se } dist(u) + c < dist(v), \text{ então } dist(v) \leftarrow dist(u) + c$$

A distância de cada cidade começa em infinito (exceto a origem, com 0) e só pode diminuir ao longo da execução, sempre para um valor que corresponde a um caminho real da origem até ela.

### Invariante

Quando uma cidade $u$ é retirada da fila de prioridade, ela é, entre as cidades ainda não finalizadas, a de menor distância conhecida, e essa distância é exatamente a menor distância real da origem até $u$.

**Por que o invariante vale.** Suponha que existisse um caminho mais curto até $u$ do que a distância conhecida. Esse caminho sai do conjunto de cidades já finalizadas por alguma aresta, chegando a uma cidade $x$ ainda pendente. A distância conhecida de $x$ não é maior que o custo desse trecho inicial do caminho. Como os pesos são positivos, o trecho restante, de $x$ até $u$, só pode somar custo, então a distância conhecida de $x$ seria menor que a de $u$. Isso contradiz o fato de $u$ ter sido escolhida por ter a menor distância pendente.

**Exemplo concreto.** Na instância da Seção 4, quando a cidade 3 é finalizada com distância 2, a cidade 2 já tinha distância conhecida 6. Qualquer outro caminho até a cidade 3 teria de passar pela cidade 2, e portanto custaria pelo menos 6, que é mais que 2. Por isso o valor 2 já é definitivo naquele momento.

---

## 4. Execução do Algoritmo na Instância

A instância é a mesma representada no Marco 2:

```text
4 5
1 2 6
1 3 2
3 2 1
2 4 2
3 4 10
```

Estado inicial: $dist = (0, \infty, \infty, \infty)$ para as cidades 1, 2, 3 e 4, e a fila contém apenas a cidade 1.

| Passo | Cidade finalizada | Voos examinados | Distâncias (1, 2, 3, 4) |
|:---|:---|:---|:---|
| 1 | 1 (dist 0) | $1 \to 2$: $0+6 = 6$ melhora $\infty$; $1 \to 3$: $0+2 = 2$ melhora $\infty$ | 0, 6, 2, $\infty$ |
| 2 | 3 (dist 2) | $3 \to 2$: $2+1 = 3$ melhora 6; $3 \to 4$: $2+10 = 12$ melhora $\infty$ | 0, 3, 2, 12 |
| 3 | 2 (dist 3) | $2 \to 4$: $3+2 = 5$ melhora 12 | 0, 3, 2, 5 |
| 4 | 4 (dist 5) | nenhum voo sai da cidade 4 | 0, 3, 2, 5 |

A cidade 3 é finalizada antes da cidade 2, embora a cidade 2 tenha sido descoberta primeiro: o que decide a ordem é a menor distância conhecida (2 contra 6), e não a ordem de descoberta. As entradas antigas da cidade 2 (distância 6) e da cidade 4 (distância 12), que continuam na fila depois de melhoradas, são descartadas quando chegam ao início dela, pois já existe uma distância menor registrada.

Saída: `0 3 2 5`, igual à conferência manual do Marco 2.

---

## 5. Complexidade

Sejam $n$ o número de cidades e $m$ o número de voos.

### Tempo

- Leitura e montagem do grafo: $O(n + m)$.
- Relaxamentos: cada voo é examinado uma única vez, no momento em que sua cidade de origem é finalizada. São, no máximo, $m$ relaxamentos.
- Fila de prioridade: cada relaxamento que melhora uma distância insere uma entrada, então a fila recebe no máximo $m + 1$ entradas ao longo de toda a execução. Cada inserção e cada retirada custa $O(\log m)$ em um heap binário.
- Total: $O((n + m)\log m)$.

Como o enunciado admite voos paralelos, $m$ não é limitado por $n^2$, e por isso o termo correto é $\log m$. Quando não há paralelos, $m \le n^2$ e $\log m \le 2\log n$, o que leva à forma usual $O((n+m)\log n)$. Com uma fila de prioridade indexada, que mantém no máximo uma entrada por cidade, o custo é $O((n+m)\log n)$ diretamente.

Ordem de grandeza para o pior caso do problema ($n = 10^5$, $m = 2\cdot10^5$): cerca de $3\cdot10^5$ operações de fila, cada uma com custo próximo de $\log_2(2\cdot10^5) \approx 18$, ou seja, algo da ordem de $5\cdot10^6$ passos elementares. Essa é uma estimativa assintótica; o tempo real depende das constantes da linguagem e será medido no Marco 5, já que o limite do CSES é de 1 segundo.

### Espaço

- Lista de adjacência: $O(n + m)$.
- Vetor de distâncias: $O(n)$.
- Fila de prioridade: $O(m)$ com entradas repetidas, ou $O(n)$ com fila indexada.
- Total: $O(n + m)$, bem abaixo do limite de 512 MB.

### Valores das distâncias

Um caminho pode ter até $n - 1$ arestas de peso até $10^9$, então a maior distância possível é da ordem de $10^5 \cdot 10^9 = 10^{14}$. Esse valor não cabe em um inteiro de 32 bits, mas na implementação em Python é tratado nativamente sem perda de precisão pelo tipo `int` (precisão arbitrária), usando `10**18` como sentinela de infinito.