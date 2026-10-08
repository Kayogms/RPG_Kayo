# RPG_Kayo - Trabalho Prático 2 (T2)

📌 **Objetivo do Repositório**

Este repositório contém os artefatos e o código-fonte desenvolvidos para o **Trabalho Prático 2 (T2)** da disciplina de Resolução de Problemas com Grafos. O objetivo principal deste projeto é aplicar conceitos avançados de modelagem estrutural e algoritmos de emparelhamento em grafos para resolver o problema **"Paintball" (Kattis - Problema I)**.

Todo o processo de desenvolvimento está documentado na pasta `acompanhamento/`, dividido em marcos que demonstram a evolução da solução:

* **Marco 1:** Modelagem matemática do problema, delimitando o grafo bipartido ($|V| = 2N$, $|E| = 2M$) e a redução ao problema de Emparelhamento Perfeito (*Bipartite Perfect Matching*).
* **Marco 2:** Caracterização da propriedade estrutural, caminhos aumentantes (Lema de Berge), estados adicionais da busca e análise do efeito cascata de desalocação/realocação.
* **Marco 3:** Aplicação do Algoritmo de Kuhn utilizando Busca em Profundidade (DFS) para encontrar caminhos aumentantes, controle de recursão e validação estrutural.
* **Marco 4:** Validação cruzada com oráculos independentes, testes de estresse em limites de restrição e conclusão com submissão ao juiz online.

---

## 🚀 Como Executar o Código

### Pré-requisitos

* Python 3.10+ (testado e homologado no Python 3.14)
* Não há dependências externas de pacotes (`numpy`, `scipy`, etc. são opcionais).

O pacote `algs4/` (implementações de referência de Sedgewick & Wayne adaptadas para a disciplina) já está incluído dentro de `src/algs4/`.

### Estrutura de Arquivos para Execução

```text
T2/
├── src/
│   ├── algs4/              # pacote de referência do professor (Graph, Bag, etc.)
│   ├── grafo_base.py        # leitura de stdin, construção do grafo bipartido e validação estrutural
│   ├── kuhn_matcher.py      # algoritmo de Kuhn (busca de caminhos aumentantes via DFS)
│   ├── main.py              # ponto de entrada de desenvolvimento com validações e prints detalhados
│   ├── main_submissao.py    # ponto de entrada para submissão no Kattis (saída estrita)
│   ├── gerador.py           # ferramenta de apoio: gera casos sample1, impossible e stress
│   └── validador.py         # bateria local: casos dirigidos, força bruta e estresse
├── acompanhamento/
│   ├── marco-1.md           # modelagem inicial e grafo bipartido
│   ├── marco-2.md           # propriedade estrutural e caminhos aumentantes
│   ├── marco-3.md           # implementação do Kuhn, DFS e testes
│   └── marco-4.md           # validação cruzada, estresse e submissão
└── Problema_Paintball.pdf   # especificação original do problema
```

Todos os scripts leem a entrada pelo **stdin** — nenhum deles abre arquivo diretamente no código.

---

### Opção 1 — Execução via Pipe com o `gerador.py`

A forma mais rápida e conveniente de testar no terminal:

```bash
# Testar o caso de exemplo válido (Sample 1)
python gerador.py sample1 | python main.py

# Testar o caso sem solução (Impossible)
python gerador.py impossible | python main.py

# Testar caso de estresse com limites máximos (N=1000 jogadores, M=5000 arestas)
python gerador.py stress --n 1000 --m 5000 --seed 42 | python main.py
```

*(No Windows, substitua `python` por `python3.14` ou seu executável Python configurado caso necessário).*

---

### Opção 2 — Digitando a entrada diretamente no terminal

1. A partir de `T2/src`, execute:
   ```bash
   python main.py
   ```
2. Digite ou cole a entrada no formato do problema:
   ```text
   N M
   u1 v1
   ...
   uM vM
   ```
3. Sinalize o fim da entrada:
   * **Windows / PowerShell:** `Ctrl+Z` e depois `Enter`.
   * **Linux / macOS:** `Ctrl+D`.

---

### Opção 3 — Redirecionando um arquivo de texto

Caso possua a entrada salva em um arquivo `.txt`:

```bash
python main.py < caminho/para/arquivo.txt
```

---

## 🛠️ Scripts Disponíveis

| Script | Finalidade |
|---|---|
| `main.py` | Executa a validação estrutural no Sample 1, roda o algoritmo de Kuhn e exibe detalhadamente a atribuição atirador $\to$ alvo, conferindo se todos os jogadores foram usados como alvo exatamente uma vez. |
| `main_submissao.py` | Versão estrita para o juiz Kattis: imprime apenas `Impossible` ou as $N$ linhas com os alvos atribuídos a cada jogador. |
| `gerador.py` | Ferramenta auxiliar de testes para gerar instâncias de teste (`sample1`, `impossible`, `stress`). |
| `validador.py` | Bateria de validação local: casos dirigidos, validação cruzada com força bruta (3.000 instâncias) e estresse $N=1000$, $M=5000$, conferindo a integridade de cada atribuição nas duas implementações. Uso: `python validador.py`. |
| `grafo_base.py` | Módulo de infraestrutura que constrói o grafo bipartido $2N$ usando `algs4.graph.Graph`. Não deve ser executado diretamente. |
| `kuhn_matcher.py` | Implementação do Algoritmo de Kuhn. |

---

## 🤖 Declaração de Uso de Inteligência Artificial

Em conformidade com as diretrizes da disciplina, declaramos o uso de ferramentas de Inteligência Artificial como assistentes de desenvolvimento durante este trabalho.

A IA foi utilizada para os seguintes fins:
* Refinamento conceitual e estruturação da documentação em Markdown dos Marcos.
* Discussão teórica comparativa entre algoritmos de emparelhamento bipartido (Kuhn vs. Hopcroft-Karp).
* Apoio na análise de complexidade e simulação de teste de mesa das chamadas recursivas com inversão de arestas.
