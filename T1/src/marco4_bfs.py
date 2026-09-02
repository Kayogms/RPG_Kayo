"""
=================================================================
 marco4_bfs.py
 Marco 4 - Aplicação básica de BFS e conclusão: Ladder Takahashi
 (Problema I)

 Reaproveita algs4.breadth_first_paths.BreadthFirstPaths SEM
 NENHUMA modificação em sua lógica interna, comparando o resultado
 com DFS (Marco 3), UF e CC (oráculos independentes), e definindo
 a BFS como método de submissão final ao AtCoder.
=================================================================
"""

from grafo_base import (
    LeitorEntrada,
    LadderSymbolGraph,
    validar_estrutura,
    maior_andar_via_uf,
    maior_andar_via_cc,
)
from marco3_dfs import ValidadorDFS
from algs4.graph import Graph
from algs4.breadth_first_paths import BreadthFirstPaths


# -----------------------------------------------------------------
# 1. BFS — reaproveitando BreadthFirstPaths sem alterações
# -----------------------------------------------------------------
def maior_andar_via_bfs(G: Graph, sg: LadderSymbolGraph, origem_idx):
    """
    Executa a BFS de referência (algs4.breadth_first_paths.
    BreadthFirstPaths) SEM NENHUMA modificação em sua lógica interna
    (marked[], edge_to[]), e obtém o maior andar alcançável
    pós-processando o vetor de alcançabilidade já calculado por ela
    (has_path_to), em vez de alterar o algoritmo de busca em si.
    """
    bfs = BreadthFirstPaths(G, origem_idx)
    maior = sg.name(origem_idx)
    for v in range(G.V):
        if bfs.has_path_to(v):
            maior = max(maior, sg.name(v))
    return maior, bfs


# -----------------------------------------------------------------
# 2. VALIDADOR DO MARCO 4 — compara BFS x DFS x UF x CC
# -----------------------------------------------------------------
class ValidadorBFS:
    """
    Validador do Marco 4:
      1. Executa a BFS a partir da origem.
      2. Exibe o maior andar alcançado.
      3. Compara o resultado com DFS (já validada no Marco 3), UF e
         CC, fechando a comparação entre os quatro métodos.
    """

    @staticmethod
    def validar(sg: LadderSymbolGraph, edges, origem=1, maior_dfs=None):
        G = sg.graph()
        origem_idx = sg.index(origem)

        maior_bfs, _ = maior_andar_via_bfs(G, sg, origem_idx)

        print("=== Execução da BFS ===")
        print(f"Origem:                 {origem}")
        print(f"Maior andar (BFS):      {maior_bfs}")
        print()

        maior_uf = maior_andar_via_uf(edges, sg, origem_idx)
        maior_cc = maior_andar_via_cc(G, sg, origem_idx)

        print("=== Comparação BFS x DFS x UF x CC ===")
        print(f"BFS -> maior andar alcançável: {maior_bfs}")
        if maior_dfs is not None:
            print(f"DFS -> maior andar alcançável: {maior_dfs}")
        print(f"UF  -> maior andar alcançável: {maior_uf}")
        print(f"CC  -> maior andar alcançável: {maior_cc}")

        valores = {maior_bfs, maior_uf, maior_cc}
        if maior_dfs is not None:
            valores.add(maior_dfs)

        assert len(valores) == 1, f"Divergência entre métodos! Valores: {valores}"
        print(f"[OK] Todos os métodos concordam: resposta = {maior_bfs}")

        return maior_bfs


# -----------------------------------------------------------------
# 3. SUBMISSÃO FINAL (AtCoder)
# -----------------------------------------------------------------
def resolver_para_submissao(origem=1):
    """
    Pipeline final de resolução, adequado para submissão ao
    AtCoder (sem prints de depuração/validação): usa a BFS de
    referência (BreadthFirstPaths) como método escolhido — ver
    justificativa no Marco 4, Seção 4 — e imprime apenas o resultado.
    """
    edges = LeitorEntrada.ler()
    sg = LadderSymbolGraph(edges, vertice_partida=origem)
    G = sg.graph()
    origem_idx = sg.index(origem)
    maior, _ = maior_andar_via_bfs(G, sg, origem_idx)
    print(maior)


def main_desenvolvimento():
    """
    Pipeline de desenvolvimento/testes (Sample 1), com validação
    estrutural, DFS, BFS, UF e CC, todos comparados entre si.
    """
    edges = LeitorEntrada.ler()
    sg = LadderSymbolGraph(edges, vertice_partida=1)

    validar_estrutura(sg)
    print()

    maior_dfs = ValidadorDFS.validar(sg, edges, origem=1)
    print()

    ValidadorBFS.validar(sg, edges, origem=1, maior_dfs=maior_dfs)


if __name__ == "__main__":
    # Durante o desenvolvimento/testes, usar main_desenvolvimento().
    # Para submissão real ao AtCoder, comentar a linha abaixo e usar
    # resolver_para_submissao() no lugar (sem prints de validação).
    main_desenvolvimento()
