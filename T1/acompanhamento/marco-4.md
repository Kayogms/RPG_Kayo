# Marco 4 — Aplicação básica de BFS e conclusão: Ladder Takahashi (Problema I)

**Data de Criação:** 18 de Agosto de 2026  

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo   |
| :--- | :--- | :--- |:--------|
| 1.0 | 18/08/2026 | Criação do documento e estrutura inicial | F |

---

## 1. Execução Manual da BFS (Sample 1)

**Ponto de Partida:** Vértice 1 (Andar 1).

**Passo a Passo da Travessia:**

A fila inicia com `[1]`. Desenfileira `1`, enfileira `4`. Desenfileira `4`, enfileira `3` e `10`. Desenfileira `3`, enfileira `8`. Desenfileira `10`. Desenfileira `8`. Fila vazia — fim da exploração.

---

## 2. Níveis, Distâncias e Predecessores

| Andar | Nível (Distância) | Predecessor |
| :---: | :---: | :---: |
| 1 | 0 | `None` |
| 4 | 1 | 1 |
| 3 | 2 | 4 |
| 10 | 2 | 4 |
| 8 | 3 | 3 |

### 2.1 Validação Cruzada com DFS e DSU (Oráculo)

O valor de `maior_andar` obtido pela BFS foi comparado com os resultados já validados no Marco 3 (DFS) e com o oráculo estrutural (DSU), confirmando a convergência dos três métodos:

| Método | Maior andar alcançável |
| :---: | :---: |
| BFS | 10 |
| DFS | 10 |
| DSU | 10 |

**Saída real da validação (`ValidadorBFS.validar`):**

```
=== Comparação BFS x DSU x DFS ===
BFS -> maior andar alcançável: 10
DSU -> maior andar alcançável: 10
DFS -> maior andar alcançável: 10
[OK] Todos os métodos concordam: resposta = 10
```

---

## 3. Comparação entre DFS e BFS

A DFS explora o grafo mergulhando no ramo mais profundo antes de retroceder (*backtracking*), o que é ideal para buscar caminhos longos. A BFS explora o grafo em camadas (níveis), processando todos os vizinhos imediatos antes de avançar, sendo ideal para encontrar distâncias mínimas em grafos não ponderados.

---

## 4. Escolha Justificada

Ambas resolvem o problema de conectividade, mas a **BFS foi escolhida para a submissão final**. O processamento em camadas em uma fila iterativa (`collections.deque`) é altamente eficiente e garante segurança contra limites de recursão profunda que poderiam ocorrer em uma DFS não iterativa, além de ser perfeitamente compatível com o limite de $N = 2\times10^5$.

---

## 5. Adaptação e Integração

A BFS padrão foi adaptada com a introdução da variável acumuladora `maior_andar`, atualizada a cada remoção da fila:

```python
maior_andar = max(maior_andar, atual)
```

A solução foi integrada usando a mesma representação de lista de adjacência (hash) dos marcos anteriores.

**Trecho de Código Integrado (`grafo_base.py`):**

```python
    def bfs(self, origem):
        visitados = {origem}
        nivel = {origem: 0}
        predecessor = {origem: None}
        fila = deque([origem])
        maior_andar = origem

        while fila:
            atual = fila.popleft()
            maior_andar = max(maior_andar, atual)

            for vizinho in self.adj[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    nivel[vizinho] = nivel[atual] + 1
                    predecessor[vizinho] = atual
                    fila.append(vizinho)

        return {
            "visitados": visitados,
            "nivel": nivel,
            "predecessor": predecessor,
            "maior_andar": maior_andar,
        }
```

---

## 6. Testes e Complexidade

O resultado da BFS foi validado cruzando-o simultaneamente com a DFS e com o oráculo estrutural (DSU), conforme demonstrado na Seção 2.1. A complexidade final de tempo e espaço manteve-se em $O(V + E)$, garantindo eficiência ótima para o problema, com $|V| \le 2N+1$ e $|E| = N \le 2\times10^5$.

---

## 7. Submissão

O código integrado com a BFS foi submetido na plataforma **AtCoder** e recebeu o veredito **`Accepted`** (evidência salva na pasta `evidencias/accepted.png`).

**Código de submissão final (`marco4_bfs.py` — `resolver_para_submissao`):**

```python
def resolver_para_submissao(origem=1):
    edges = LeitorEntrada.ler()
    grafo = Graph().construir(edges, vertice_partida=origem)
    resultado = grafo.bfs(origem)
    print(resultado["maior_andar"])
```

---

## 8. Ensaio da Apresentação

Registro do ensaio da exposição oral (até 5 minutos), conforme roteiro do trabalho:

| Slide | Conteúdo | Tempo alvo |
| :---: | :--- | :---: |
| Capa | Identificação do grupo e do problema | — |
| 1 | Problema (Ladder Takahashi) | 1 min |
| 2 | Modelagem (Marco 1) | 1 min |
| 3 | Representação computacional (Marco 2) | 1 min |
| 4 | DFS/BFS (Marcos 3 e 4) | 1 min |
| 5 | Validação (`Accepted`) | 1 min |

*Observação: preencher com data do ensaio e ajustes identificados após a prática cronometrada.*
