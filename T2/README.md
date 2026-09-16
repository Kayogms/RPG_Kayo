# RPG_Kayo

📌 Objetivo do Repositório

Este repositório contém os artefatos e o código-fonte desenvolvidos para o **Trabalho Prático 1 (T1)** da disciplina de Resolução de Problemas com Grafos. O objetivo principal deste projeto é aplicar conceitos práticos de modelagem estrutural e algoritmos de busca em grafos para resolver o problema **"Ladder Takahashi" (AtCoder ABC277 C)**.

Todo o processo de desenvolvimento está documentado na pasta `acompanhamento/`, dividido em quatro marcos que demonstram a evolução da nossa solução:

* **Modelagem matemática** do problema delimitando vértices e arestas.
* **Representação computacional** eficiente utilizando compressão de coordenadas e listas de adjacência.
* Aplicação e testes com **Busca em Profundidade (DFS)** e validação cruzada.
* Escolha final da **Busca em Largura (BFS)** justificada por testes de estresse, culminando na submissão e no veredito `Accepted`.

---

## 🚀 Como Executar o Código

### Pré-requisitos

* Python 3.10+
* Biblioteca `numpy` instalada (`pip install numpy`)

O pacote `algs4/` (implementações de referência de Sedgewick & Wayne, adaptadas de nosso professor) já está incluído dentro de `src/algs4/`, então nenhuma instalação adicional é necessária além do `numpy`.

### Estrutura relevante para execução

```text
T1/
├── src/
│   ├── algs4/              # pacote de referência (Graph, Bag, UF, CC, BreadthFirstPaths)
│   ├── grafo_base.py        # leitura da entrada, compressão de coordenadas, oráculos de validação
│   ├── marco3_dfs.py        # DFS adaptada + validação cruzada (DFS x UF x CC)
│   └── marco4_bfs.py        # BFS (solução final) + validação cruzada + submissão
└── dados/
    ├── casos-de-teste.txt   # casos de exemplo (Sample 1, 2, 3 do enunciado)
    └── gerador.py           # gera casos de teste adicionais, incluindo estresse
```

Todos os scripts leem a entrada pelo **stdin** — nenhum deles abre arquivo sozinho. Isso significa que existem **duas formas** de fornecer a entrada, detalhadas abaixo.

---

### Opção 1 — Digitando a entrada diretamente no terminal

Útil para testar rapidamente sem precisar criar um arquivo.

1. A partir de `T1/src`, rode o script desejado, por exemplo:
   ```bash
   python marco4_bfs.py
   ```
2. O terminal vai ficar aguardando a entrada. Digite (ou cole) o caso de teste, linha por linha, seguindo o formato do problema:
   ```text
   N
   A1 B1
   A2 B2
   ...
   AN BN
   ```
   Exemplo (Sample 1 do enunciado):
   ```text
   4
   1 4
   4 3
   4 10
   8 3
   ```
3. Sinalize o **fim da entrada**:
   * **Windows / PowerShell:** pressione `Ctrl+Z` e depois `Enter`.
   * **Linux / macOS:** pressione `Ctrl+D`.
4. O programa processa tudo de uma vez e imprime o resultado.

---

### Opção 2 — Fornecendo um arquivo de dentro de `dados/`

Útil para reexecutar o mesmo caso várias vezes sem redigitar, e obrigatório para casos grandes (estresse), que seriam inviáveis de digitar manualmente.

1. Garanta que o arquivo de teste existe em `T1/dados/` (por exemplo, `casos-de-teste.txt`, já incluído com os Samples do enunciado).
2. A partir de `T1/src`, rode o script redirecionando o arquivo com o operador `<`:
   ```bash
   python marco4_bfs.py < ../dados/casos-de-teste.txt
   ```
   No Windows/PowerShell, o comando é o mesmo:
   ```powershell
   python marco4_bfs.py < ..\dados\casos-de-teste.txt
   ```
3. A saída aparece imediatamente, sem necessidade de digitar nada ou sinalizar fim de entrada — o arquivo já entrega o conteúdo completo ao programa.

**Scripts disponíveis para execução (ambas as opções acima funcionam para qualquer um deles):**

| Script | O que faz ao rodar |
|---|---|
| `marco3_dfs.py` | valida a estrutura do grafo, executa a DFS adaptada e compara o resultado com dois oráculos independentes (UF e CC) |
| `marco4_bfs.py` | executa a BFS (algoritmo de submissão), compara com DFS, UF e CC, e serve de base para a versão final entregue ao AtCoder |

`grafo_base.py` não deve ser executado diretamente — ele só define classes e funções reutilizadas pelos outros dois scripts.

---

### O papel do `gerador.py`

`dados/gerador.py` é uma **ferramenta de apoio ao desenvolvimento**, e não faz parte da solução do problema em si — por isso vive em `dados/`, ao lado dos casos de teste, e não em `src/`.

**O que ele faz:** gera arquivos `.txt` no mesmo formato de entrada esperado pelo problema (`N` seguido de `N` pares `Ai Bi`), permitindo criar casos que seriam impraticáveis de montar manualmente, como:

* **Casos de estresse**, com $N$ próximo do limite máximo ($N = 2\times10^5$), usados para medir tempo de execução e verificar se a solução respeita a complexidade $O(V+E)$ esperada.
* **Casos estruturais específicos**, como um grafo em formato de cadeia (`1-2, 2-3, 3-4, ...`), que foi o cenário usado para comprovar empiricamente o `RecursionError` da DFS recursiva e justificar a escolha da BFS para a submissão final (ver `acompanhamento/marco-3.md`, Seção 4).

**Como usar:** rode o gerador a partir de `T1/dados`, redirecionando a saída para um novo arquivo de teste:

```bash
python gerador.py > teste_estresse.txt
```

Em seguida, use esse arquivo gerado exatamente como qualquer outro caso de teste, seguindo a **Opção 2** acima:

```bash
python marco4_bfs.py < ../dados/teste_estresse.txt
```

---

## 🤖 Declaração de Uso de Inteligência Artificial

Em conformidade com as diretrizes da disciplina, declaramos o uso de ferramentas de Inteligência Artificial (como o Gemini) como assistentes de desenvolvimento durante este trabalho.

A IA foi utilizada para os seguintes fins:

* Refinamento e estruturação da documentação em Markdown.
* Discussão de conceitos teóricos de grafos (como a diferença prática de memória entre Matriz e Lista de Adjacência).
* Auxílio na formatação da apresentação e no detalhamento de casos de teste extremos (como o erro de recursão da DFS).
