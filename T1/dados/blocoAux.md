# 🚀 Roteiro de Comandos para a Apresentação

**Aviso importante:** Certifique-se de que o terminal do seu computador esteja aberto na raiz do projeto (na pasta `T1` ou `RPG_Kayo`) antes de executar os comandos.

---

## 0. Preparação (Rodar ANTES da aula)

Este comando roda o seu script `gerador.py` e cria o arquivo de texto gigante com a corrente de 200.000 andares na pasta `dados`.

```bash
python gerador.py
```

---

## 1. Testes Simples (Aqueça a apresentação)

Use um destes para mostrar que a lógica base do programa funciona perfeitamente antes de ir para o teste de estresse.

**Opção A: Grafo Desconexo (Andar inalcançável)**
```bash
python src/main.py < dados/teste_desconexo.txt
```
> **Legenda (O que falar):** *"Neste teste rápido, existem andares muito altos (como 50 e 100), mas eles estão desconectados do andar 1. Nossa BFS identifica corretamente que o caminho acaba no andar 12."*

**Opção B: Andar 1 Isolado (Sem escadas)**
```bash
python src/main.py < dados/teste_isolado.txt
```
> **Legenda (O que falar):** *"Aqui temos escadas, mas nenhuma se conecta ao andar 1. O código lida com isso perfeitamente e devolve 1, o próprio andar de origem."*

---

## 2. O Clímax - O Problema da DFS (Teste de Estresse)

Rode a sua busca em profundidade com o arquivo gigante para demonstrar fisicamente a limitação do Python.

```bash
python src/marco3_dfs_2.py < dados/teste_gigante.txt
```
> **O que acontece:** O terminal vai travar rapidamente e imprimir uma tela cheia de erros terminando em `RecursionError`.
> 
> **Legenda (O que falar):** *"Como podem ver, se usarmos a DFS recursiva em um prédio onde as 200 mil escadas formam uma linha reta, o interpretador do Python estoura a pilha de chamadas e gera um `RecursionError`."*

---

## 3. A Conclusão - A Solução com BFS

Rode imediatamente a sua solução final (Busca em Largura) com o mesmo arquivo gigante para mostrar a diferença de arquitetura.

```bash
python src/main.py < dados/teste_gigante.txt
```
> **O que acontece:** O programa roda silenciosamente e imprime `200001` na tela em menos de 1 segundo.
> 
> **Legenda (O que falar):** *"Por esse motivo técnico, nós optamos pela BFS iterativa controlada por fila para a submissão final. O mesmo cenário de 200 mil andares é resolvido em frações de segundo, validando o nosso Accepted."*