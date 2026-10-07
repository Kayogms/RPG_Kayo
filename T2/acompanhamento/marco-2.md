# Marco 2 — Propriedade Estrutural: Kattis Paintball (Problema I)

**Data de Criação:** 28/09/2026

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:-------|:-----------|:-----------|:------|
| 2.0 | 28/09/2026 | Criação do documento: definição estrutural, estados da busca e teste de mesa do critério | E |
| 2.1 | 28/09/2026 | Execução manual refeita sobre a instância do Marco 1 (rastreabilidade entre marcos); instância de 6 jogadores mantida como evidência complementar do efeito cascata; descrições dos estados reescritas em linguagem concreta, sem notação de código | E |

---

## 1. Propriedade Exigida pelo Problema

A propriedade estrutural central exigida pelo Kattis Paintball é o **Emparelhamento Perfeito** (*Perfect Bipartite Matching*).

Um emparelhamento em um grafo é um subconjunto de arestas que não compartilham vértices entre si — ou seja, nenhum vértice participa de mais de uma aresta escolhida. O problema exige que todos os jogadores atirem e sejam atingidos exatamente uma vez. No modelo de grafo bipartido definido no Marco 1 (conjunto $A$ = atiradores, conjunto $B$ = alvos), isso significa encontrar um emparelhamento de tamanho exatamente $N$, cobrindo simultaneamente todos os vértices de $A$ e todos os vértices de $B$, cada um em exatamente uma aresta.

---

## 2. Critério Algorítmico

O critério usado para reconhecer o emparelhamento perfeito vem da teoria de Berge sobre **caminhos aumentantes**, aplicada computacionalmente pelo Algoritmo de Kuhn.

**Critério-chave:** um emparelhamento é máximo se, e somente se, não existir nenhum caminho aumentante no grafo.

**Caminho aumentante:** um caminho que começa em um atirador ainda sem alvo, alterna entre arestas fora do emparelhamento atual e arestas dentro dele, e termina em um alvo totalmente livre.

**Efeito de encontrar um caminho aumentante:** ao percorrê-lo, o status de cada aresta do caminho é invertido — o que não estava emparelhado passa a estar, e vice-versa. O tamanho total do emparelhamento cresce em exatamente 1 a cada caminho aumentante encontrado. O processo se repete para cada atirador, até que todos estejam emparelhados (emparelhamento perfeito) ou até que sobre algum atirador sem nenhum caminho aumentante disponível (caso em que a resposta é `Impossible`).

---

## 3. Estado Adicional à Busca

Além da marcação de visitados de uma busca convencional, o critério exige manter duas informações adicionais durante a execução:

| Estado | O que representa | Comportamento |
|---|---|---|
| **Registro de correspondência atual** | Para cada alvo, qual atirador está emparelhado com ele no momento — a "foto" do emparelhamento em construção. | Permanece entre as tentativas de diferentes atiradores; só é atualizado quando um caminho aumentante é efetivamente concluído. |
| **Controle de visita temporário** | Quais alvos já foram considerados durante a tentativa do atirador atual. | É reiniciado a cada novo atirador, diferente da marcação permanente de uma busca de alcançabilidade tradicional — sua única função é impedir que a busca reconsidere o mesmo alvo mais de uma vez dentro da mesma tentativa, evitando ciclos. |

A diferença central em relação a uma busca de alcançabilidade comum está no papel do registro de correspondência: a busca não apenas verifica se um alvo está livre, mas, ao encontrá-lo ocupado, tenta **deslocar** o atirador atualmente correspondente a esse alvo para outra opção, repetindo o processo recursivamente até esgotar as alternativas ou concluir o caminho aumentante.

---

## 4. Execução Manual na Instância do Marco 1

Para manter a rastreabilidade com o marco anterior, a execução abaixo usa a mesma instância pequena definida no Marco 1: 4 jogadores, com visibilidade em ciclo (1–2, 2–3, 3–4, 4–1).

**Correspondência inicial:** nenhum alvo ocupado.

| Atirador | Tentativa | Situação encontrada | Ação |
|:---:|:---:|:---|:---|
| 1 | alvo 2 | livre | assume o alvo 2 |
| 2 | alvo 1 | livre | assume o alvo 1 |
| 3 | alvo 2 | ocupado (atirador 1) | tenta deslocar o atirador 1 → alvo 4, que está livre → atirador 1 passa para o alvo 4; alvo 2 fica livre para o atirador 3 |
| 4 | alvo 3 | livre | assume o alvo 3 |

**Correspondência final:** atirador 2 → alvo 1; atirador 3 → alvo 2; atirador 4 → alvo 3; atirador 1 → alvo 4.

Todos os 4 atiradores foram emparelhados — emparelhamento perfeito confirmado. Esta atribuição é diferente, jogador a jogador, da apresentada como exemplo no Marco 1 (que tinha atirador 1 → alvo 2, formando o ciclo no sentido oposto), mas ambas são igualmente válidas: o enunciado aceita qualquer atribuição em que todos sejam atingidos exatamente uma vez, e a diferença aqui decorre apenas da ordem em que os alvos de cada atirador foram considerados durante a busca (nesta simulação conceitual adotou-se a ordem natural dos vizinhos, e no Marco 3 formaliza-se o comportamento exato da lista encadeada LIFO do `Bag`).

---

## 5. Instância Complementar: Efeito Cascata em Múltiplos Níveis

A instância do Marco 1 demonstra um deslocamento de um único nível (Seção 4, atirador 3). Para evidenciar como o deslocamento pode se propagar em cadeia por vários atiradores antes de concluir um caminho aumentante, apresenta-se uma segunda instância, com 6 jogadores:

- Atirador 1 vê os alvos 2 e 3.
- Atirador 2 vê os alvos 1, 3 e 4.
- Atirador 3 vê os alvos 1, 2 e 4.
- Atirador 4 vê os alvos 2 e 3.
- Atirador 5 vê o alvo 6.
- Atirador 6 vê o alvo 5.

**Correspondência inicial:** nenhum alvo ocupado.

| Atirador | Tentativas em cadeia | Resultado |
|:---:|:---|:---|
| 1 | alvo 2: livre → assume | atirador 1 → alvo 2 |
| 2 | alvo 1: livre → assume | atirador 2 → alvo 1 |
| 3 | alvo 1: ocupado (atirador 2) → desloca atirador 2 → alvo 3: livre → atirador 2 assume o alvo 3 | atirador 3 → alvo 1; atirador 2 → alvo 3 |
| 4 | alvo 2: ocupado (atirador 1) → desloca atirador 1 → alvo 3: ocupado (atirador 2) → desloca atirador 2 → alvo 1: ocupado (atirador 3) → desloca atirador 3 → alvo 4: livre → atirador 3 assume o alvo 4; em cadeia, atirador 2 assume o alvo 1; atirador 1 assume o alvo 3; atirador 4 assume o alvo 2 | atirador 4 → alvo 2; atirador 1 → alvo 3; atirador 2 → alvo 1; atirador 3 → alvo 4 |
| 5 | alvo 6: livre → assume | atirador 5 → alvo 6 |
| 6 | alvo 5: livre → assume | atirador 6 → alvo 5 |

**Correspondência final:** atirador 1 → alvo 3; atirador 2 → alvo 1; atirador 3 → alvo 4; atirador 4 → alvo 2; atirador 5 → alvo 6; atirador 6 → alvo 5.

O passo do atirador 4 é o ponto central desta instância: uma única tentativa percorre uma cadeia de três deslocamentos (atiradores 1, 2 e 3, nessa ordem) antes de alcançar um alvo livre, ilustrando por que a complexidade do algoritmo é proporcional ao número de arestas percorridas em cada tentativa, e não apenas ao número de atiradores.

Vale notar, ainda, que os atiradores 5 e 6 formam um par isolado do restante do grafo (só se enxergam entre si): mesmo com dependências profundas no restante da instância, esse par é resolvido de forma independente, sem qualquer interação com as cadeias de deslocamento dos atiradores 1 a 4 — confirmando que o algoritmo trata corretamente componentes desconexos do grafo de visibilidade.
