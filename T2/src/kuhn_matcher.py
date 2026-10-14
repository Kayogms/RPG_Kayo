"""
=================================================================
 kuhn_matcher.py
 Algoritmo de Kuhn (busca de caminhos aumentantes) para
 emparelhamento perfeito bipartido - Kattis Paintball (T2).

 Esta classe NAO e uma adaptacao de nenhuma classe do professor:
 conforme avaliado no Marco 1 (Secao "Avaliacao do reaproveitamento
 das classes de referencia"), DepthFirstPaths nao serve como base
 direta, pois exige (1) marcacao reiniciada a cada tentativa de
 atirador, e (2) uma recursao que decide desalocar o emparelhamento
 atual de um alvo ocupado, em vez de apenas decidir "para onde ir"
 entre vizinhos nao targets.
=================================================================
"""

from algs4.graph import Graph


class KuhnMatcher:


    # -------------------------------------------------------------
    # 1. ESTADO INICIAL
    # -------------------------------------------------------------
    def __init__(self, G: Graph, n: int):
        self.G = G
        self.n = n

        self.match_para = [None] * (2 * n)

    # -------------------------------------------------------------
    # 2. LACO PRINCIPAL: UMA RODADA POR ATIRADOR
    # -------------------------------------------------------------
    def resolve(self):

        for atirador in range(self.n):

            target = set()

            sucesso = self._try_path(atirador, target)

            if not sucesso:
                return None

        assign = [None] * self.n
        for idx_alvo in range(self.n, 2 * self.n):
            atirador = self.match_para[idx_alvo]
            if atirador is not None:
                jogador_alvo = idx_alvo - self.n + 1   # indice -> jogador
                assign[s] = jogador_alvo

        return assign

    # -------------------------------------------------------------
    # 3. BUSCA RECURSIVA DO CAMINHO AUMENTANTE
    # -------------------------------------------------------------
    def _try_path(self, atirador, target):

        for alvo in self.G.adj[s]:

            if alvo in target:
                continue
            target.add(alvo)

            shooter = self.match_para[t]

            if shooter is None or self._try_path(
                shooter, target
            ):

                self.match_para[t] = shooter
                return True

        return False
