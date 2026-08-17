# =================================================================
# marco4_bfs.py
# Marco 4 — Aplicação básica de BFS e conclusão.
# Executa a BFS a partir do andar 1, valida o resultado comparando
# com o DSU e com a DFS do Marco 3, e imprime a resposta final
# (pronta para integração/submissão ao AtCoder).
# =================================================================

from grafo_base import LeitorEntrada, Graph, DSU, validar_estrutura
from marco3_dfs import ValidadorDFS


class ValidadorBFS:
    """
    Validador do Marco 4:
      1. Executa a BFS a partir da origem.
      2. Exibe níveis (distâncias), predecessores e o maior andar
         alcançado.
      3. Compara o resultado da BFS com o DSU (oráculo) e com a DFS
         (já validada no Marco 3), fechando a comparação tripla.
    """

    @staticmethod
    def validar(grafo: Graph, edges, origem=1, maior_dfs=None):
        resultado_bfs = grafo.bfs(origem)

        print("=== Execução da BFS ===")
        print(f"Origem:                 {origem}")
        print(f"Vértices visitados:     {sorted(resultado_bfs['visitados'])}")
        print(f"Níveis (distâncias):    {resultado_bfs['nivel']}")
        print(f"Predecessores:          {resultado_bfs['predecessor']}")
        print(f"Maior andar (BFS):      {resultado_bfs['maior_andar']}")
        print()

        # --- Comparação com o DSU (oráculo) ---
        dsu = DSU.construir_de_arestas(edges, origem=origem)
        maior_dsu = dsu.maior_no_conjunto(origem)

        print("=== Comparação BFS x DSU x DFS ===")
        print(f"BFS -> maior andar alcançável: {resultado_bfs['maior_andar']}")
        print(f"DSU -> maior andar alcançável: {maior_dsu}")
        if maior_dfs is not None:
            print(f"DFS -> maior andar alcançável: {maior_dfs}")

        valores = [resultado_bfs["maior_andar"], maior_dsu]
        if maior_dfs is not None:
            valores.append(maior_dfs)

        assert len(set(valores)) == 1, (
            f"Divergência entre métodos! Valores obtidos: {valores}"
        )
        print(f"[OK] Todos os métodos concordam: resposta = {resultado_bfs['maior_andar']}")

        return resultado_bfs["maior_andar"]


def resolver_para_submissao(origem=1):
    """
    Pipeline final de resolução, adequado para submissão ao
    AtCoder (sem prints de depuração/validação): usa BFS como
    método escolhido (justificativa a ser registrada no Marco 4),
    e imprime apenas o resultado.
    """
    edges = LeitorEntrada.ler()
    grafo = Graph().construir(edges, vertice_partida=origem)
    resultado = grafo.bfs(origem)
    print(resultado["maior_andar"])


def main_desenvolvimento():
    """
    Pipeline de desenvolvimento/testes (Sample 1), com validação
    estrutural, DFS, BFS e DSU, todos comparados entre si.
    """
    edges = LeitorEntrada.ler()
    grafo = Graph().construir(edges, vertice_partida=1)

    validar_estrutura(grafo)
    print()

    maior_dfs = ValidadorDFS.validar(grafo, edges, origem=1)
    print()

    ValidadorBFS.validar(grafo, edges, origem=1, maior_dfs=maior_dfs)


if __name__ == "__main__":
    # Durante o desenvolvimento/testes, usar main_desenvolvimento().
    # Para submissão real ao AtCoder, comentar a linha abaixo e usar
    # resolver_para_submissao() no lugar (sem prints de validação).
    main_desenvolvimento()