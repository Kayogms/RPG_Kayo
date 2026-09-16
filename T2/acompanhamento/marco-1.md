# Marco 1 — Modelagem: Kattis Paintball (Problema I)

**Data de Criação:** 16/09/2026

### Histórico de Versões

| Versão | Data       | Descrição das Alterações                                                                        | Grupo |
|:-------|:-----------|:------------------------------------------------------------------------------------------------|:------|
| 1.0    | 16/09/2026 | Criação do documento, modelagem inicial e adaptação estrutural para o problema de emparelhamento | E     |

---

## 1. Enunciado, Entrada, Saída e Restrições

### Resumo do Problema

#### Enunciado
Marek e seus colegas terminaram a universidade e decidiram celebrar com uma partida de paintball. Após uma hora de jogo, uma situação peculiar ocorreu: cada jogador possui exatamente uma bala restante.

Marek quer saber se é possível que **todos os jogadores sejam atingidos exatamente uma vez**, considerando que ninguém pode se mover. É dada a descrição de quais jogadores conseguem se ver. Se um jogador consegue ver outro, ele pode atirar nele. O objetivo é encontrar um alvo para cada jogador de modo que a condição seja satisfeita.

#### Entrada
A entrada consiste em dois números inteiros separados por espaço, **N** e **M**, onde **N** é o número de jogadores. Os jogadores são numerados de 1 a **N**. Em seguida, há **M** linhas, cada uma contendo dois inteiros separados por espaço, **u** e **v**, indicando que os jogadores **u** e **v** conseguem se ver mutuamente. Cada par aparece no máximo uma vez na entrada.

#### Saída
Se não houver uma atribuição de alvos tal que todos sejam atingidos, o programa deve imprimir `Impossible`. Caso contrário, deve imprimir **N** linhas. A i-ésima linha deve conter o número do alvo do i-ésimo jogador. Se houver mais de uma solução, qualquer uma é válida.

#### Restrições
* **N** (número de jogadores): 2 a 1000.
* **M** (número de linhas de visão): 0 a 5000.
* **u**, **v**: 1 a **N** (com **u** diferente de **v**).
* Cada jogador atira exatamente 1 vez e recebe exatamente 1 tiro.

#### Observações Importantes
O problema requer que se resuma a entrada, saída e restrições. Este é um problema clássico cuja solução exige a aplicação de conhecimentos estruturais da Unidade II, sendo classificado como um desafio avançado (Problema I*).
* Como cada jogador precisa de um alvo único e exclusivo, o problema trata-se fundamentalmente de encontrar um **Emparelhamento Perfeito** (Bipartite Matching).
* A validação será se conseguimos formar **N** pares únicos entre "atiradores" e "alvos".

---

## 2. Vértices, Arestas e Tipo do Grafo

A modelagem de vértices e arestas e a classificação do grafo são requisitos obrigatórios do Marco 1.

### Vértices (V)
A modelagem divide conceitualmente os jogadores em dois conjuntos independentes para formar um grafo bipartido:
* **Conjunto A (Atiradores):** Vértices representando os jogadores no momento de atirar.
* **Conjunto B (Alvos):** Vértices representando os mesmos jogadores no momento de receber o tiro.
* Logo, total de vértices = 2**N** (máximo de 2000).

### Arestas (E)
Cada **aresta** representa a linha de visão. Como a visão é mútua na entrada original, para cada par (x, y), adicionamos as possibilidades de tiro:
* O jogador x (atirador) pode atirar em y (alvo).
* O jogador y (atirador) pode atirar em x (alvo).
* Total de arestas = 2**M** (máximo de 10000).

### Tipo de Grafo
O grafo original de visão é não direcionado, mas modelaremos o problema transformando-o em um:
* **Grafo Bipartido Direcionado:** As conexões vão exclusivamente do Conjunto A (Atiradores) para o Conjunto B (Alvos).
* **Não ponderado:** Todas as linhas de visão têm o mesmo peso.
* **Simples:** Sem laços ou arestas paralelas.

### Relação com o Problema e Resultado de Aprendizagem
O resultado de aprendizagem aferido é a identificação e resolução de emparelhamentos. O objetivo se resume a:
1. Construir o grafo bipartido conectando Atiradores e Alvos.
2. Encontrar o **Emparelhamento Máximo** neste grafo.
3. Se o tamanho do emparelhamento for igual a **N**, todos atiram e todos são atingidos (emparelhamento perfeito). Retornar os pares. Caso contrário, retornar `Impossible`.

---

## 3. Instância Pequena e Resultado Esperado

A criação de uma instância pequena é exigida pelo Marco 1.

**Caso de Teste Escolhido (Ciclo de 4 Jogadores):**

    4 4
    1 2
    2 3
    3 4
    4 1

**Matriz de Adjacência Bipartida (Atiradores nas linhas, Alvos nas colunas):**

| -              | **Alvo 1** | **Alvo 2** | **Alvo 3** | **Alvo 4** |
|:---------------|:----------:|:----------:|:----------:|:----------:|
| **Atirador 1** |     0      |     1      |     0      |     1      |
| **Atirador 2** |     1      |     0      |     1      |     0      |
| **Atirador 3** |     0      |     1      |     0      |     1      |
| **Atirador 4** |     1      |     0      |     1      |     0      |

**Resultado Esperado:**

    2
    3
    4
    1

**Explicação (Rastreio manual básico):**
O jogador 1 atira no 2. O jogador 2 atira no 3. O jogador 3 atira no 4. O jogador 4 atira no 1. Todos os 4 atiraram exatamente uma vez e receberam exatamente um tiro, satisfazendo a condição sem que ninguém ficasse de fora.

---

## 4. Hipótese Inicial de Solução

O grupo deve indicar como a DFS/BFS participa da solução neste marco.

**Estratégia de Resolução:**

1. **Construção:** Ler as entradas e montar uma lista de adjacência modelando o grafo bipartido (cada atirador aponta para os alvos que consegue ver).
2. **Execução Principal (Busca de Caminhos Aumentantes):** O problema de emparelhamento em grafos bipartidos pode ser resolvido utilizando a DFS para encontrar caminhos aumentantes (ex: Algoritmo de Kuhn).
3. **Papel da Busca (DFS):** A DFS participa da solução iterando sobre cada atirador e tentando atribuir-lhe um alvo. Se o alvo desejado estiver livre, o emparelhamento é feito. Se o alvo já estiver atribuído a um atirador anterior, a DFS entra recursivamente para verificar se o atirador anterior pode ser realocado para um alvo diferente, liberando espaço para o atual.
4. **Validação e Retorno:**
   * Se o algoritmo conseguir emparelhar todos os **N** jogadores, imprimimos o alvo associado a cada um.
   * Se o loop terminar e o total de pares formados for menor que **N**, a saída é imediata: `Impossible`.

**Complexidade esperada da solução:** O Algoritmo de Kuhn utilizando DFS possui complexidade $O(V \cdot E)$. Como os vértices chegam a 2000 e arestas a 10000, o número de operações no pior caso fica na casa dos milhões, o que é processado rapidamente e garantirá o `Accepted` nas restrições de tempo padrão.