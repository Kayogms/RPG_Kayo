# 🚀 Roteiro de Comandos para a Apresentação (Versão PowerShell)

**Aviso importante:** Certifique-se de que o terminal do seu computador esteja aberto na raiz do projeto (na pasta `T1`) antes de executar os comandos.

---

## 0. Preparação

Este comando cria todos os arquivos de teste estruturados na pasta `dados`.

```powershell
python gerador.py
```

---

## 1. Exemplo Base

**Executando na DFS (Marco 3):**
```powershell
cat dados/teste_sample1.txt | python src/marco3_dfs.py
```

**Executando na BFS (Marco 4):**
```powershell
cat dados/teste_sample1.txt | python src/marco4_bfs.py
```

---

## 2. Testes Extremos

**Grafo Desconexo:**
```powershell
cat dados/teste_desconexo.txt | python src/marco4_bfs.py
```

**Andar 1 Isolado:**
```powershell
cat dados/teste_isolado.txt | python src/marco4_bfs.py
```

---

## 3. O Problema da DFS

Rode a sua Busca em Profundidade (`marco3_dfs.py`) com o arquivo gigante para causar o erro.

```powershell
cat dados/teste_gigante.txt | python src/marco3_dfs.py
```

---

## 4. Conclusão - A Solução com BFS Limpa

```powershell
cat dados/teste_gigante.txt | python src/main_submissao.py
```
