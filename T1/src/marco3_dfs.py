"""
=================================================================
 marco3_dfs.py
 Marco 3 - Aplicação básica de DFS: Ladder Takahashi (Problema I)

 Adapta algs4.depth_first_paths.DepthFirstPaths (classe LadderDFS),
 mantendo a lógica original de marcação (marked[]) e predecessor
 (edge_to[]) intacta, acrescentando apenas o acúmulo do maior andar
 alcançado durante a recursão.

 Valida o resultado contra dois oráculos independentes já
 disponíveis neste marco: UF (Union-Find) e CC (Connected
 Components). A BFS ainda não está disponível neste marco
 (reservada ao Marco 4).
=================================================================
"""

from grafo_base import (
    LeitorEntrada,
    LadderSymbolGraph,
    validar_estrutura,
    maior_andar_via_uf,
    maior_andar_via_cc,
)
from algs4.graph import Graph


# -----------------------------------------------------------------
# 1. DFS ADAPTADA — baseada em algs4.depth_first_paths.DepthFirstPaths
# -----------------------------------------------------------------
class LadderDFS:
    """
    Adaptação de algs4.depth_first_paths.DepthFirstPaths.

    A implementação de referência apenas marca alcançabilidade
    (marked[]) e registra o predecessor (edge_to[]) para reconstrução
    de caminhos. A lógica de marcação/recursão foi mantida idêntica;
    a única adição é a variável acumuladora `maior_andar`, que
    converte cada índice visitado de volta ao andar original (via
    LadderSymbolGraph.name) e mantém o maior valor encontrado.

    ATENÇÃO — limitação herdada da implementação de referência: por
    ser RECURSIVA, esta classe está sujeita ao limite de recursão do
    Python (padrão: 1000 chamadas). Em componentes conexos muito
    "compridos" (efeito corrente, ex.: 1-2-3-...-N), a recursão pode
    ultrapassar esse limite antes de alcançar $N = 2\\times10^5$ nós.
    Essa limitação foi confirmada empiricamente (ver Marco 3, Seção 4)
    e é o principal motivo pelo qual a BFS (iterativa) foi escolhida
    como método de submissão final no Marco 4.
    """

    def __init__(self, G: Graph, sg: LadderSymbolGraph, origem_idx):
        self.marked = [False for _ in range(G.V)]
        self.edge_to = [None for _ in range(G.V)]
        self.s = origem_idx
        self._sg = sg
        self.maior_andar = sg.name(origem_idx)
        self._dfs(G, origem_idx)

    def _dfs(self, G, v):
        self.marked[v] = True
        self.maior_andar = max(self.maior_andar, self._sg.name(v))
        for w in G.adj[v]:
            if not self.marked[w]:
                self.edge_to[w] = v
                self._dfs(G, w)

    def has_path_to(self, v):
        return self.marked[v]


# -----------------------------------------------------------------
# 2. VALIDADOR DO MARCO 3 — compara DFS x UF x CC
# -----------------------------------------------------------------
class ValidadorDFS:
    """
    Validador do Marco 3:
      1. Executa a DFS a partir da origem.
      2. Exibe o maior andar alcançado.
      3. Compara o resultado da DFS com os dois oráculos disponíveis
         até este marco: UF e CC.
    """

    @staticmethod
    def validar(sg: LadderSymbolGraph, edges, origem=1):
        G = sg.graph()
        origem_idx = sg.index(origem)

        dfs = LadderDFS(G, sg, origem_idx)
        maior_dfs = dfs.maior_andar

        print("=== Execução da DFS ===")
        print(f"Origem:                 {origem}")
        print(f"Maior andar (DFS):      {maior_dfs}")
        print()

        maior_uf = maior_andar_via_uf(edges, sg, origem_idx)
        maior_cc = maior_andar_via_cc(G, sg, origem_idx)

        print("=== Comparação DFS x UF x CC ===")
        print(f"DFS -> maior andar alcançável: {maior_dfs}")
        print(f"UF  -> maior andar alcançável: {maior_uf}")
        print(f"CC  -> maior andar alcançável: {maior_cc}")

        assert maior_dfs == maior_uf == maior_cc, (
            f"Divergência entre métodos! "
            f"DFS={maior_dfs}, UF={maior_uf}, CC={maior_cc}"
        )
        print(f"[OK] DFS, UF e CC concordam: resposta = {maior_dfs}")

        return maior_dfs


def main():
    edges = LeitorEntrada.ler()
    sg = LadderSymbolGraph(edges, vertice_partida=1)

    validar_estrutura(sg)
    print()

    ValidadorDFS.validar(sg, edges, origem=1)


if __name__ == "__main__":
    main()
