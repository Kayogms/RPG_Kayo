# Marco 3 — Aplicação básica de DFS: Ladder Takahashi (Problema I)

**Data de Criação:** 17 de Agosto de 2026  

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo   |
| :--- | :--- | :--- |:--------|
| 1.0 | 17/08/2026 | Criação do documento e estrutura inicial | F |
| 1.1 | 17/08/2026 | Inclusão da implementação iterativa da DFS e validação por DSU | F |

---

## 1. Execução Manual da DFS (Sample 1)

**Ponto de Partida:** Vértice 1 (Andar 1).

**Passo a Passo da Travessia:**

1. Partimos do vértice `1`, inserindo-o na pilha e marcando-o como visitado. O `maior_andar` inicializa com `1`.
2. O vértice `1` é desempilhado e seus vizinhos (`[4]`) são avaliados. O vértice `4` não foi visitado, logo entra na pilha e recebe `1` como predecessor.
3. Desempilhamos o vértice `4`. O `maior_andar` é atualizado para `max(1, 4) = 4`. Seus vizinhos são `[1, 3, 10]`. Como o `1` já foi visitado, empilhamos o `3` e o `10`.
4. A pilha explícita processa o topo (ex: `10`), atualizando o `maior_andar` para `10`. Como o `10` não tem outros vizinhos não visitados, a exploração desse ramo encerra.
5. Retornamos para processar o vértice `3`, que empilha seu vizinho não visitado `8`, atualizando os rastreios até esgotar todos os nós alcançáveis da componente.

---

## 2. Estados de Visita e Árvore de Busca

**Controle de Estados:**

O controle de visitados é feito utilizando um conjunto (`set()`), garantindo buscas em tempo $O(1)$ médio e evitando ciclos em loops infinitos, dado que o grafo não direcionado possui arestas de retorno.

**Estrutura da Árvore de Busca (DFS Tree):**

* **Raiz:** Andar 1
* **Arestas de Árvore (Geradoras):** (1, 4), (4, 3), (3, 8), (4, 10)
* **Predecessores mapeados:** `{1: None, 4: 1, 3: 4, 8: 3, 10: 4}`

---

## 3. Predecessores e Alcançabilidade

O rastreio gerado pelo método `dfs(origem)` da classe `Graph` na estrutura modularizada comprova os seguintes resultados para o Sample 1:

| Vértice (Andar) | Predecessor na DFS | Status de Alcançabilidade |
| :---: | :---: | :---: |
| 1 | `None` (Origem) | Visitado |
| 3 | 4 | Visitado |
| 4 | 1 | Visitado |
| 8 | 3 | Visitado |
| 10 | 4 | Visitado |

### 3.1 Validação Cruzada com DSU (Oráculo)

Para confirmar a corretude do resultado obtido pela DFS, o valor do `maior_andar` foi comparado com o resultado de uma estrutura Union-Find (DSU) independente, construída unindo todas as arestas do grafo (implementada na classe `DSU` de `grafo_base.py` e executada pelo `ValidadorDFS.validar()` em `marco3_dfs.py`):

| Método | Maior andar alcançável |
| :---: | :---: |
| DFS | 10 |
| DSU | 10 |

**Saída real da validação:**

```
=== Comparação DFS x DSU ===
DFS -> maior andar alcançável: 10
DSU -> maior andar alcançável: 10
[OK] DFS e DSU concordam: resposta = 10
```

Essa validação cruzada confirma que a árvore de busca gerada pela DFS alcança corretamente todos os vértices do componente conexo do andar 1, e que o valor máximo identificado (10) é consistente com um método de conectividade totalmente independente do algoritmo de busca em grafo.

---

## 4. Aplicabilidade ao Problema e Adaptação

**Estratégia de Adaptação:**

A DFS foi adaptada para carregar uma variável de controle (`maior_andar`), que acumula dinamicamente o maior valor inteiro de vértice encontrado a cada iteração de desempilhamento:

```python
maior_andar = max(maior_andar, atual)
```

Dessa forma, a busca garante não apenas a descoberta de toda a componente conexa, mas também resolve diretamente o objetivo de encontrar o maior andar alcançável.

**Trecho de Código Integrado (`grafo_base.py`):**

```python
    def dfs(self, origem):
        visitados = {origem}
        predecessor = {origem: None}
        ordem_visita = []
        pilha = [origem]
        maior_andar = origem
        while pilha:
            atual = pilha.pop()
            ordem_visita.append(atual)
            maior_andar = max(maior_andar, atual)
            for vizinho in self.adj[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    predecessor[vizinho] = atual
                    pilha.append(vizinho)
        return {
            "visitados": visitados,
            "predecessor": predecessor,
            "ordem_visita": ordem_visita,
            "maior_andar": maior_andar,
        }
```
