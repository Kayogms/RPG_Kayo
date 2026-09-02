"""
=================================================================
 grafo_base.py
 Módulo comum reutilizado pelos Marcos 2, 3 e 4 - Ladder Takahashi.

 Reaproveita SEM ALTERAÇÃO NA LÓGICA:
   - algs4.graph.Graph   (representação do grafo, via array de Bag)
   - algs4.bag.Bag        (lista de adjacência, usada internamente
                            por Graph)
   - algs4.uf.UF          (Union-Find - oráculo de validação)
   - algs4.cc.CC          (Connected Components via DFS - segundo
                            oráculo, independente do UF)

 Reimplementa o CONCEITO de:
   - algs4.symbol_graph.SymbolGraph -> LadderSymbolGraph
     (mapeamento de chaves arbitrárias para índices via tabela de
     símbolos; aqui a fonte é um numpy.array em vez de um arquivo
     com delimitador, e a tabela de símbolos é um dict nativo do
     Python, já que algs4.st.ST não foi fornecido pelo grupo).

 Observação: BreadthFirstPaths (BFS) NÃO é importada neste módulo
 de propósito — ela só é introduzida em marco4_bfs.py, preservando
 a progressão pedagógica do trabalho (DFS no Marco 3, BFS no
 Marco 4).
=================================================================
"""

import sys
import numpy as np

from algs4.graph import Graph
from algs4.uf import UF
from algs4.cc import CC


# -----------------------------------------------------------------
# 1. LEITURA DA ENTRADA
# -----------------------------------------------------------------
class LeitorEntrada:
    """
    Lê a entrada padrão no formato definido no Marco 1:
        N
        A1 B1
        A2 B2
        ...
        AN BN
    """

    @staticmethod
    def ler(stream=None):
        """
        Retorna um numpy.array de shape (N, 2) e dtype=np.int64,
        onde edges[:, 0] = A_i e edges[:, 1] = B_i.
        """
        stream = stream or sys.stdin
        data = stream.read().split()
        n = int(data[0])

        valores = np.array(data[1:1 + 2 * n], dtype=np.int64)
        edges = valores.reshape(n, 2)

        return edges


# -----------------------------------------------------------------
# 2. COMPRESSÃO DE COORDENADAS + CONSTRUÇÃO DO Graph (algs4.graph)
#    (adaptação do conceito de algs4.symbol_graph.SymbolGraph)
# -----------------------------------------------------------------
class LadderSymbolGraph:
    """
    Adaptação de SymbolGraph (algs4/symbol_graph.py) para o problema
    Ladder Takahashi.

    Interface mantida idêntica à original:
      - contains(chave) -> bool
      - index(chave)    -> índice comprimido
      - name(índice)    -> chave original (andar)
      - graph()         -> instância de algs4.graph.Graph já construída
    """

    def __init__(self, edges, vertice_partida=1):
        self._st = {}  # equivalente a ST(): {andar_original: índice}

        for a, b in edges.tolist():
            if a not in self._st:
                self._st[a] = len(self._st)
            if b not in self._st:
                self._st[b] = len(self._st)

        # Garante a presença do vértice de partida, mesmo isolado
        if vertice_partida not in self._st:
            self._st[vertice_partida] = len(self._st)

        # Vetor inverso índice -> andar original
        self._keys = [0] * len(self._st)
        for andar, idx in self._st.items():
            self._keys[idx] = andar

        # Constrói o Graph de referência (algs4.graph.Graph), sem
        # nenhuma modificação em sua lógica interna
        self._G = Graph(len(self._st))
        for a, b in edges.tolist():
            self._G.add_edge(self._st[a], self._st[b])

    def contains(self, andar):
        return andar in self._st

    def index(self, andar):
        return self._st[andar]

    def name(self, v):
        return self._keys[v]

    def num_vertices(self):
        return len(self._keys)

    def graph(self):
        return self._G


# -----------------------------------------------------------------
# 3. ORÁCULOS DE VALIDAÇÃO — UF e CC (algs4, sem alteração)
# -----------------------------------------------------------------
def maior_andar_via_uf(edges, sg: LadderSymbolGraph, origem_idx):
    """
    Usa algs4.uf.UF (weighted quick-union com path compression) como
    oráculo independente de conectividade.
    """
    uf = UF(sg.num_vertices())
    for a, b in edges.tolist():
        uf.union(sg.index(a), sg.index(b))

    maior = sg.name(origem_idx)
    for v in range(sg.num_vertices()):
        if uf.connected(v, origem_idx):
            maior = max(maior, sg.name(v))
    return maior


def maior_andar_via_cc(G: Graph, sg: LadderSymbolGraph, origem_idx):
    """
    Usa algs4.cc.CC (componentes conexas via DFS recursiva) como um
    segundo oráculo independente de conectividade.
    """
    cc = CC(G)
    maior = sg.name(origem_idx)
    for v in range(G.V):
        if cc.connected(v, origem_idx):
            maior = max(maior, sg.name(v))
    return maior


# -----------------------------------------------------------------
# 4. VALIDAÇÃO ESTRUTURAL (Sample 1) — reutilizada nos Marcos 2, 3 e 4
# -----------------------------------------------------------------
ESPERADO_SAMPLE_1 = {
    1:  {4},
    3:  {4, 8},
    4:  {1, 3, 10},
    8:  {3},
    10: {4},
}


def validar_estrutura(sg: LadderSymbolGraph):
    """Confere a lista de adjacência (Graph/Bag) contra o Sample 1."""
    G = sg.graph()
    for andar, vizinhos_esperados in ESPERADO_SAMPLE_1.items():
        idx = sg.index(andar)
        vizinhos_obtidos = {sg.name(w) for w in G.adj[idx]}
        assert vizinhos_obtidos == vizinhos_esperados, (
            f"Falha na validação estrutural: andar {andar} - "
            f"esperado {vizinhos_esperados}, obtido {vizinhos_obtidos}"
        )
    print("[OK] Validação estrutural (lista de adjacência) - Sample 1")
