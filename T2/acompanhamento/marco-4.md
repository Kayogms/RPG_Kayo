# Marco 4 — Implementação Final e Conclusão: Kattis Paintball (Problema I)

**Data de Criação:** 07/10/2026

### Histórico de Versões

| Versão | Data | Descrição das Alterações | Grupo |
|:---|:---|:---|:---|
| 1.0 | 07/10/2026 | Consolidação da implementação final em `src/`, identificação das classes de referência do `algs4` (reutilizadas vs. modificadas), bateria de testes de estresse e registro oficial da evidência do veredito `Accepted` no Kattis (Submissão 20629089). | E |

---

## 1. Consolidação da Solução em `src/`

Para atender tanto às boas práticas de engenharia de software acadêmica quanto aos requisitos operacionais do juiz online **Kattis**, a solução final foi consolidada no diretório `T2/src/` com uma arquitetura de duas frentes:

```text
T2/
├── src/
│   ├── algs4/               # Pacote de referência do professor (Graph, Bag, etc.)
│   ├── grafo_base.py         # Leitor de entrada e montagem do grafo bipartido com algs4.graph.Graph
│   ├── kuhn_matcher.py       # Algoritmo de Kuhn baseado em busca por caminhos aumentantes
│   ├── main.py               # Ponto de entrada de desenvolvimento com validações e asserções
│   ├── main_submissao.py     # Solução unificada e autocontida para submissão no Kattis
│   └── gerador.py            # Gerador de testes para casos de borda e estresse
├── evidencias/
│   └── Captura de tela 2026-10-07 144512.png  # Evidência oficial do Accepted no Kattis
├── apresentacao/
│   ├── slides.html           # Código-fonte da apresentação nos padrões da UNIFOR
│   └── apresentacao_paintball.pdf  # Slides compilados em alta resolução
└── acompanhamento/
    ├── marco-1.md            # Modelagem do problema e grafo bipartido
    ├── marco-2.md            # Propriedade estrutural e caminhos aumentantes
    ├── marco-3.md            # Estratégia algorítmica e análise assintótica
    └── marco-4.md            # Implementação final, testes e conclusão (este documento)
```

---

## 2. Identificação das Classes do `algs4` (Reutilizadas vs. Modificadas)

Em conformidade com as diretrizes da disciplina e o repositório de referência do orientador ([carubbi/RPG](https://github.com/carubbi/RPG/tree/main/algs4-py/algs4)), mapeou-se a relação entre o código de referência e a solução implementada:

| Módulo / Classe de Referência | Status no Projeto | Justificativa Técnica da Decisão |
|:---|:---:|:---|
| **`algs4.graph.Graph`** | **Reutilizada sem modificação** | Utilizada diretamente em `grafo_base.py` para instanciar a estrutura do grafo bipartido com $2N$ vértices (0 a $N-1$ para atiradores; $N$ a $2N-1$ para alvos). Cada par de visibilidade $(u, v)$ insere as arestas $A_u \to B_v$ e $A_v \to B_u$. |
| **`algs4.bag.Bag`** | **Reutilizada sem modificação** | Estrutura encadeada usada internamente pelo `Graph`. Sua inserção em $O(1)$ no topo da lista encadeada (comportamento LIFO) define a ordem concreta de exploração dos alvos pela DFS. |
| **`algs4.depth_first_paths.DepthFirstPaths`** | **Substituída / Não utilizada diretamente** | Embora o algoritmo de Kuhn utilize uma Busca em Profundidade (DFS), a classe `DepthFirstPaths` foi desconsiderada como base direta porque: (1) possui vetor de marcação `marked` permanente para toda a vida do objeto, enquanto o emparelhamento exige marcação temporária (`visited`) reiniciada a cada novo atirador; e (2) realiza busca estática de alcance, sem implementar a lógica de **desalocação e realocação recursiva** exigida para caminhos aumentantes. |
| **`KuhnMatcher` (Classe Autônoma)** | **Implementação Própria** | Desenvolvida para orquestrar o Algoritmo de Kuhn sobre o `Graph`, gerenciando o vetor global `match_to` de alocação de alvos e o mecanismo recursivo `_try_path(shooter, visited)`. |
| **`main_submissao.py` (Versão Standalone)** | **Adaptação para o Juiz Online** | Juízes como o Kattis aceitam a submissão de um único arquivo `.py` e não possuem o pacote `algs4` instalado. Por isso, adaptou-se a classe `Graph` para utilizar listas nativas do Python (`adj = [[] for _ in range(V)]`), mantendo a mesma semântica e sem depender de módulos externos. |

---

## 3. Resultados dos Testes Executados e Validação Local

Antes da submissão na plataforma, a solução foi submetida a uma bateria completa de testes locais:

### 3.1 Testes Funcionais e Casos de Borda

1. **Sample 1 do Kattis ($N=3, M=3$):** Triângulo de visibilidade completa. O algoritmo retornou a permutação válida `3, 1, 2` (Jogador 1 atira no 3; Jogador 2 no 1; Jogador 3 no 2).
2. **Sample 2 do Kattis ($N=3, M=2$):** Jogador 1 enxerga 2 e 3, mas 2 e 3 só enxergam o 1. O algoritmo identificou o déficit de alvos e retornou `Impossible`.
3. **Instância Didática $C_4$ ($N=4, M=4$):** Ciclo de 4 jogadores. O rastreamento validou o efeito cascata com realocação do Jogador 1 de $B_4$ para $B_2$, concluindo a atribuição `2, 3, 4, 1`.
4. **Grafos Desconexos ($N=4, M=2$):** Dois pares isolados $(1-2)$ e $(3-4)$. O algoritmo resolveu ambos os componentes de forma independente, obtendo `2, 1, 4, 3`.
5. **Grafo sem Arestas ($M=0$):** Resposta imediata `Impossible`.

### 3.2 Teste de Estresse e Desempenho

Utilizou-se o script `gerador.py` para gerar uma instância com os limites máximos especificados pelo problema:
* $N = 1.000$ jogadores
* $M = 5.000$ pares de visibilidade mútua

**Resultados do Estresse:**
* **Tempo de Execução:** Menos de **0,02 segundos** em ambiente local (Python 3.14).
* **Consumo de Memória:** Inferior a 2 MB para o grafo e estruturas auxiliares.
* **Validação Algorítmica de Integridade:** Um oráculo automatizado conferiu formalmente que:
  1. Todos os 1.000 jogadores atiraram em alvos pertencentes à sua lista real de visibilidade;
  2. Todos os 1.000 jogadores foram atingidos exatamente uma vez (permutação bijetora perfeita de $1 \dots 1000$).

### 3.3 Mitigação de `RecursionError`

Herdando a lição aprendida no Trabalho 1 (onde a recursão estourou o limite padrão de 1.000 chamadas em grafos em cadeia), incluiu-se preventivamente a instrução:
```python
import sys
sys.setrecursionlimit(200000)
```
Essa configuração garantiu que mesmo no pior caso teórico de uma cadeia contínua de 1.000 desalocações consecutivas, o interpretador executasse sem falha de pilha.

---

## 4. Evidência Oficial de `Accepted` no Kattis 🏆

A solução consolidada em `main_submissao.py` foi submetida oficialmente ao juiz online internacional **Kattis** ([open.kattis.com/problems/paintball](https://open.kattis.com/problems/paintball)).

### Dados Oficiais da Submissão:
* **ID da Submissão:** `20629089`
* **Problema:** `Paintball`
* **Autor / Submissor:** `RAFAEL DA SILVA LEITES`
* **Linguagem:** `Python 3`
* **Data / Hora:** `07/10/2026 - 19:44:14`
* **Tempo de CPU (Runtime):** **`0.14 s`** (limite da plataforma: 1.00 s)
* **Bateria de Casos de Teste:** **`29 / 29 aprovados`** (100% dos casos verdes)
* **Veredito Oficial:** **`Accepted`** ✅

A evidência visual capturada da plataforma encontra-se arquivada em:
📁 [**evidencias/Captura de tela 2026-10-07 144512.png**](file:///D:/dev/Unifor/RPG_Kayo/T2/evidencias/Captura%20de%20tela%202026-10-07%20144512.png)

---

## 5. Preparação da Apresentação

Para a apresentação final do Trabalho 2, desenvolveu-se uma apresentação completa em formato Widescreen 16:9, estruturada estritamente nos padrões visuais da **Universidade de Fortaleza (UNIFOR)**:

* **Arquivos Gerados:**
  * [**apresentacao/slides.html**](file:///D:/dev/Unifor/RPG_Kayo/T2/apresentacao/slides.html): Apresentação em HTML5/CSS3 moderno com design responsivo e tipografia otimizada.
  * [**apresentacao/apresentacao_paintball.pdf**](file:///D:/dev/Unifor/RPG_Kayo/T2/apresentacao/apresentacao_paintball.pdf): Documento PDF final compilado em alta resolução vetorial.
* **Estrutura dos Slides:**
  1. **Capa Oficial:** Identidade visual e logo institucional da Unifor.
  2. **Identificação da Equipe:** Título do trabalho, integrantes (Rafael Da Silva, Kayo Nicholas, Gustavo Viana), orientador e disciplina.
  3. **Problema e Modelagem Bipartida:** Dualidade de papéis (Atirador $A_k$ vs. Alvo $B_k$) e redução ao emparelhamento perfeito de $2N$ vértices.
  4. **Aderência ao `algs4`:** Relação detalhada de reutilização de `Graph`/`Bag` e criação da classe `KuhnMatcher`.
  5. **Algoritmo de Kuhn e Rastreamento Didático:** Tabela passo a passo do exemplo $C_4$ ilustrando a mecânica do efeito cascata.
  6. **Complexidade e Testes:** Limite assintótico $O(NM)$, controle de recursão e bateria de testes locais.
  7. **Conclusão e Evidência:** Integração do comprovante oficial de `Accepted` da submissão 20629089 no Kattis.

---

## 6. Conclusão Geral

O Trabalho Prático 2 cumpriu com êxito todas as etapas estabelecidas na ementa da disciplina:
1. **Modelagem:** A transformação de um problema de visibilidade de paintball em um problema de emparelhamento perfeito bipartido provou-se conceitualmente sólida.
2. **Algoritmo:** A escolha do Algoritmo de Kuhn via Busca em Profundidade aliou simplicidade de código a alto desempenho prático, superando com folga os limites temporais e espaciais.
3. **Engenharia de Software:** A integração entre as classes de referência do `algs4` e a versão otimizada para o juiz online demonstrou capacidade de adaptação prática.
4. **Validação:** A aprovação unânime nos 29 testes do juiz internacional Kattis com tempo de 0.14s ratifica a corretude e a robustez da solução entregue.
