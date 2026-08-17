# Marco 1 — Modelagem: Ladder Takahashi (Problema I)

**Data de Criação:** 14/08/2026  

### Histórico de Versões

| Versão | Data       | Descrição das Alterações                                                        | Grupo   |
|:-------|:-----------|:--------------------------------------------------------------------------------|:--------|
| 1.0    | 14/08/2026 | Criação do documento e estrutura inicial                                        | F |
| 1.1    | 15/08/2026 | Ajuste da hipótese: Inclusão do DSU como validador exclusivo das buscas BFS/DFS | F |
| 1.2    | 17/08/2026 | Simplificação                                                                   | F |
---

## 1. Enunciado, Entrada, Saída e Restrições

# Resumo do Problema

## Enunciado

Existe um prédio com $10^9$ andares e $N$ escadas.
Takahashi está no 1º andar (o mais baixo) e quer alcançar o andar mais alto possível usando escadas (possivelmente nenhuma).

As escadas são numeradas de 1 a $N$, e a escada $i$ conecta o andar $A_i$ ao andar $B_i$. É possível usar a escada $i$ em qualquer direção, para ir do andar $A_i$ ao andar $B_i$ ou vice-versa, mas não é possível se mover entre outros andares através dela.

Takahashi pode se mover livremente dentro do mesmo andar, mas não pode se mover entre andares sem usar uma escada.

**Qual é o andar mais alto que Takahashi consegue alcançar?**

## Entrada

Alcançar o andar mais alto possível a partir do andar 1, usando $N$ escadas bidirecionais.Entrada: A entrada consiste em um número inteiro $N$ que indica a quantidade de escadas, seguido por $N$ linhas, onde cada uma contém dois números inteiros representando os andares conectados por uma escada ($A_i$ e $B_i$). Para fins de processamento, esses pares são organizados em uma estrutura de matriz com duas colunas, permitindo o armazenamento eficiente de todas as conexões do grafo. É essencial utilizar tipos de dados de 64 bits para representar os andares, uma vez que o valor pode atingir $10^9$, evitando erros de estouro de memória (overflow).

## Saída

Um único inteiro representando o andar mais alto alcançável.

## Restrições

- $1 \le N \le 2\times10^5$
- $1 \le A_i, B_i \le 10^9$
- $A_i \ne B_i$  o sentido lógico, confirmado pelos exemplos, é que os extremos de cada escada são sempre diferentes
- Todos os valores de entrada são inteiros

## Observações Importantes

O problema é de **conectividade em grafo**: cada andar é um vértice, cada escada é uma aresta não direcionada. É preciso encontrar o **maior andar alcançável** a partir do andar 1.

*   O prédio tem até 10^9 andares — muito grande para representar um grafo explícito por andar; é necessário usar **compressão de coordenadas** (mapear apenas os andares presentes no `numpy.array` de entrada, mais o andar 1).
*   $N$ pode chegar a 2 $\times$ 10^5, exigindo uma travessia eficiente (BFS/DFS). Adicionalmente, a estrutura **Union-Find (DSU)** será empregada com o objetivo único de validar a corretude das buscas (oráculo de testes), garantindo que a componente conexa encontrada pelos algoritmos principais seja exata.
*   Operações vetorizadas do `numpy` (como `np.unique` para compressão de coordenadas) podem acelerar o pré-processamento.
*   Se o andar 1 não aparecer em nenhuma escada, a resposta é **1** (não é possível se mover — ver Exemplo 3).
*   A resposta é o **maior valor de andar** entre todos os andares conectados (direta ou indiretamente) ao andar 1.

## 2. Vértices, Arestas e Tipo do Grafo

## Vértices (V)

Cada **vértice** representa um **andar do prédio** que aparece em pelo menos uma escada (mais o andar 1, ponto de partida).

- Como os andares vão até $10^9$, mas só existem no máximo $2N \le 4\times10^5$ andares distintos mencionados na entrada, o conjunto de vértices é definido por:

$$V = \{1\} \cup \{A_i : 1 \le i \le N\} \cup \{B_i : 1 \le i \le N\}$$

- Logo, $|V| \le 2N + 1 \le 4\times10^5 + 1$.
- Andares que **não aparecem** em nenhuma escada não precisam ser vértices — eles nunca poderão ser alcançados nem usados como intermediários, então são irrelevantes para o problema.
- É por isso que se usa **compressão de coordenadas**: os valores reais dos andares (até $10^9$) são mapeados para índices pequenos ($0$ a $|V|-1$), permitindo representar o grafo de forma compacta em memória.

## Arestas (E)

Cada **aresta** representa uma **escada**, conectando dois andares:

$$E = \{(A_i, B_i) : 1 \le i \le N\}$$

- $|E| = N \le 2\times10^5$
- Cada aresta tem **peso unitário** (não há custo ou distância associada — usar uma escada custa "1 movimento", mas na prática o problema só pergunta por *alcançabilidade*, não pelo caminho mais curto).
- Não há aresta "explícita" do andar 1 para si mesmo, nem laços (*self-loops*), já que $A_i \ne B_i$.

## Tipo de Grafo

O grafo é:

- **Não direcionado**: a escada $i$ pode ser usada em ambos os sentidos ($A_i \to B_i$ ou $B_i \to A_i$), então cada aresta é bidirecional.
- **Não ponderado**: não há custo diferenciado entre as escadas; o que importa é apenas se existe conexão ou não.
- **Simples** (na prática): apesar de poderem existir múltiplas escadas entre o mesmo par de andares (arestas paralelas), isso não afeta o resultado, pois o problema trata apenas de **conectividade**, não de contagem de caminhos.
- **Potencialmente desconexo**: o grafo pode ter vários **componentes conexos** — só interessa o componente que contém o vértice 1.

## Relação com o Problema

Como o objetivo é encontrar o **maior andar alcançável a partir do andar 1**, o problema se resume a:

1.  Construir o grafo $G = (V, E)$ como definido acima.
2.  Encontrar o **componente conexo** que contém o vértice 1 usando a estratégia principal estipulada (BFS/DFS).
3.  Confirmar a integridade estrutural dessa componente validando o agrupamento contra um DSU executado paralelamente.
4.  Retornar o **maior valor de andar** (valor original, não o índice comprimido) entre os vértices desse componente.

Se o vértice 1 estiver isolado (não aparecer em nenhuma aresta), seu componente conexo contém apenas ele mesmo, e a resposta é **1**.
---

## 3. Instância Pequena e Resultado Esperado

**Caso de Teste Escolhido (Sample 1):**
4
1 4
4 3
4 10
8 3

**Representação como `numpy.array` (formato de entrada especificado):**

```python
import numpy as np

edges = np.array([
    [1,  4],
    [4,  3],
    [4, 10],
    [8,  3]
], dtype=np.int64)
```

**Matriz de Incidência:**

| -      | **e0** | **e1** | **e2** | **e3** |
|--------|:------:|:------:|:------:|:------:|
| **1**  |   1    |   0    |   0    |   0    |
| **3**  |   0    |   1    |   0    |   1    |
| **4**  |   1    |   1    |   1    |   0    |
| **8**  |   0    |   0    |   0    |   1    |
| **10** |   0    |   0    |   1    |   0    |


**Resultado Esperado:**
10

**Explicação (Rastreio manual básico):**
Ele pode alcançar o 10º andar usando a escada 1 para chegar ao 4º andar e, em seguida, a escada 3 para chegar ao 10º andar.

---

## 4. Hipótese Inicial de Solução

**Estratégia de Resolução:**

Como o problema envolve andares de até 10^9, mas apenas $|V| \le 2N+1 \le 4 \times 10^5+1$ andares distintos são relevantes, a hipótese de solução consiste em:

1.  **Comprimir as coordenadas** dos andares presentes em "edges" (incluindo o andar 1) para índices pequenos, viabilizando a representação do grafo em memória.
2.  **Construir a lista de adjacência** a partir das arestas comprimidas.
3.  **Execução Principal (Alcançabilidade):** Executar uma travessia (preferencialmente DFS para exploração direta ou BFS) a partir do vértice correspondente ao andar 1, identificando e registrando o maior andar encontrado nessa componente conexa.
4.  **Validação Estrutural (Oráculo):** Executar uma estrutura de conjuntos disjuntos (Union-Find / DSU) unindo todos os andares conectados pelas arestas $E$. O maior valor pertencente ao conjunto do vértice 1 deve ser estritamente igual ao resultado apontado pela busca DFS/BFS, garantindo a corretude antes da submissão.
5.  **Retorno:** Retornar o maior andar validado (valor original) — ou **1**, caso o andar 1 esteja isolado.

**Complexidade esperada da solução principal:** $O(V + E)$, perfeitamente compatível com $N \le 2 \times 10^5$. A validação com DSU adiciona uma etapa que gira em torno de $O(E \cdot \alpha(V))$, que é praticamente linear na prática.