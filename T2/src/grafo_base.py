"""
=================================================================
 grafo_base.py
 Módulo comum reutilizado por main.py e main_submissao.py -
 Kattis Paintball (Problema I, T2).

 Reaproveita SEM ALTERAÇÃO NA LÓGICA:
   - algs4.graph.Graph   (representação do grafo, via array de Bag)
   - algs4.bag.Bag        (lista de adjacência, usada internamente
                            por Graph)
=================================================================
"""

import sys
from algs4.graph import Graph


# -----------------------------------------------------------------
# 1. LEITURA DA ENTRADA
# -----------------------------------------------------------------
class InputReader:


    @staticmethod
    def read(stream=None):

        stream = stream or sys.stdin
        data = stream.read().lstrip('\ufeff').split()

        if not data:
            return 0, []

        n = int(data[0])
        m = int(data[1])

        edges = []
        idx = 2
        for _ in range(m):
            u = int(data[idx])
            v = int(data[idx + 1])
            edges.append((u, v))
            idx += 2

        return n, edges


# -----------------------------------------------------------------
# 2. CONSTRUCAO DO GRAFO BIPARTIDO (algs4.graph.Graph)
# -----------------------------------------------------------------
def build_bipartite_graph(n, edges):

    G = Graph(2 * n)

    for u, v in edges:
        shooter_u, shooter_v = u - 1, v - 1
        target_u, target_v = n + (u - 1), n + (v - 1)

        G.add_edge(shooter_u, target_v)   # u pode atirar em v
        G.add_edge(shooter_v, target_u)   # v pode atirar em u

    return G


# -----------------------------------------------------------------
# 3. VALIDACAO ESTRUTURAL (instancia pequena do Marco 1)
# -----------------------------------------------------------------
# Instancia do Marco 1: ciclo de 4 jogadores (1-2, 2-3, 3-4, 4-1)
N_SAMPLE_1 = 4
EDGES_SAMPLE_1 = [(1, 2), (2, 3), (3, 4), (4, 1)]

# Vizinhos esperados de cada ATIRADOR (jogador 1-indexado -> alvos
# alcancaveis, 1-indexados), derivados diretamente da entrada.
EXPECTED_SAMPLE_1 = {
    1: {2, 4},
    2: {1, 3},
    3: {2, 4},
    4: {3, 1},
}


def validate_structure(G, n=N_SAMPLE_1, expected=None):
    """
    Confere a lista de adjacencia (Graph/Bag) de cada atirador
    contra os alvos esperados na instancia pequena do Marco 1.
    """
    expected = expected or EXPECTED_SAMPLE_1

    for player, expected_targets in expected.items():
        shooter_idx = player - 1
        obtained_targets = {w - n + 1 for w in G.adj[shooter_idx]}
        assert obtained_targets == expected_targets, (
            f"Falha na validacao estrutural: atirador {player} - "
            f"esperado {expected_targets}, obtido {obtained_targets}"
        )

    print("[OK] Validacao estrutural (lista de adjacencia) - Sample 1")
