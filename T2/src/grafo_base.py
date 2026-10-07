"""
=================================================================
 grafo_base.py
 Módulo comum reutilizado por main.py e main_submissao.py -
 Kattis Paintball (Problema I, T2).

 Reaproveita SEM ALTERAÇÃO NA LÓGICA:
   - algs4.graph.Graph   (representação do grafo, via array de Bag)
   - algs4.bag.Bag        (lista de adjacência, usada internamente
                            por Graph)

 Decisão de modelagem (ver Marco 1 e discussão de Graph x Digraph):
 optou-se por manter Graph (não direcionado) em vez de Digraph,
 pois a relação de visibilidade na entrada é reciproca por
 definicao (se u ve v, v ve u), e Graph.add_edge reflete
 fielmente essa reciprocidade, ainda que o Algoritmo de Kuhn
 nunca percorra o sentido "alvo -> atirador" registrado por
 Graph. Essa redundancia e inofensiva: nao compromete corretude
 nem desempenho assintotico, apenas registra no grafo uma
 informacao verdadeira que o algoritmo escolhe nao consultar.

 Modelagem do grafo bipartido:
   - indices 0..N-1         -> jogadores no papel de ATIRADOR
   - indices N..2N-1        -> jogadores no papel de ALVO
     (indice do alvo do jogador k, 1-indexado, e N + (k-1))
   - para cada par de visibilidade (u, v) da entrada, adicionam-se
     as DUAS arestas possiveis de tiro:
       atirador_u -> alvo_v
       atirador_v -> alvo_u
=================================================================
"""

import sys
from algs4.graph import Graph


# -----------------------------------------------------------------
# 1. LEITURA DA ENTRADA
# -----------------------------------------------------------------
class LeitorEntrada:
    """
    Le a entrada padrao no formato definido no Marco 1:
        N M
        u1 v1
        u2 v2
        ...
        uM vM
    """

    @staticmethod
    def ler(stream=None):
        """
        Retorna (N, edges), onde edges e uma lista de tuplas
        (u, v) com os jogadores 1-indexados, exatamente como
        aparecem na entrada.
        """
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
def construir_grafo_bipartido(n, edges):
    """
    Constroi o grafo bipartido atirador/alvo a partir da lista de
    arestas de visibilidade, usando algs4.graph.Graph sem nenhuma
    modificacao em sua logica interna.

    Convencao de indices (0-indexados internamente):
        atirador do jogador k (1-indexado) -> indice k - 1
        alvo     do jogador k (1-indexado) -> indice n + (k - 1)

    Parametros:
        n: numero de jogadores.
        edges: lista de tuplas (u, v), jogadores 1-indexados que
               se enxergam mutuamente.

    Retorna:
        G: instancia de Graph com 2*n vertices.
    """
    G = Graph(2 * n)

    for u, v in edges:
        atirador_u, atirador_v = u - 1, v - 1
        alvo_u, alvo_v = n + (u - 1), n + (v - 1)

        G.add_edge(atirador_u, alvo_v)   # u pode atirar em v
        G.add_edge(atirador_v, alvo_u)   # v pode atirar em u

    return G


# -----------------------------------------------------------------
# 3. VALIDACAO ESTRUTURAL (instancia pequena do Marco 1)
# -----------------------------------------------------------------
# Instancia do Marco 1: ciclo de 4 jogadores (1-2, 2-3, 3-4, 4-1)
N_SAMPLE_1 = 4
EDGES_SAMPLE_1 = [(1, 2), (2, 3), (3, 4), (4, 1)]

# Vizinhos esperados de cada ATIRADOR (jogador 1-indexado -> alvos
# alcancaveis, 1-indexados), derivados diretamente da entrada.
ESPERADO_SAMPLE_1 = {
    1: {2, 4},
    2: {1, 3},
    3: {2, 4},
    4: {3, 1},
}


def validar_estrutura(G, n=N_SAMPLE_1, esperado=None):
    """
    Confere a lista de adjacencia (Graph/Bag) de cada atirador
    contra os alvos esperados na instancia pequena do Marco 1.
    """
    esperado = esperado or ESPERADO_SAMPLE_1

    for jogador, alvos_esperados in esperado.items():
        idx_atirador = jogador - 1
        alvos_obtidos = {w - n + 1 for w in G.adj[idx_atirador]}
        assert alvos_obtidos == alvos_esperados, (
            f"Falha na validacao estrutural: atirador {jogador} - "
            f"esperado {alvos_esperados}, obtido {alvos_obtidos}"
        )

    print("[OK] Validacao estrutural (lista de adjacencia) - Sample 1")
