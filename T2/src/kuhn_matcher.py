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
 entre vizinhos nao visitados.

 O padrao recursivo com vetor de marcacao (visited) foi mantido
 como inspiracao estrutural da DFS classica, mas a logica de
 decisao dentro da recursao foi escrita integralmente para este
 problema (ver Marco 2, Secoes 2 e 3, para a fundamentacao teorica
 de caminhos aumentantes).

 ATENCAO - recursao e o limite do Python: com N ate 1000, uma
 cadeia de deslocamentos (ver Marco 2, Secao 5) pode, em tese,
 encostar no limite padrao de recursao do Python (1000 chamadas).
 Por seguranca, o limite e elevado explicitamente antes da
 execucao (ver main.py / main_submissao.py), registrando essa
 decisao de forma explicita, no mesmo espirito da licao aprendida
 no T1 sobre o RecursionError da DFS em componentes "em cadeia".
=================================================================
"""

from algs4.graph import Graph


class KuhnMatcher:
    """
    Encontra um emparelhamento maximo (e, se existir, perfeito) em
    um grafo bipartido representado por um algs4.graph.Graph, onde:
        - indices 0..N-1     sao os atiradores
        - indices N..2N-1    sao os alvos

    Uso:
        matcher = KuhnMatcher(G, n)
        assign = matcher.resolver()   # None se Impossible
    """

    def __init__(self, G: Graph, n: int):
        self.G = G
        self.n = n
        # match_para[idx_alvo] = idx_atirador atualmente emparelhado,
        # ou None se o alvo estiver livre. So os indices de alvo
        # (N..2N-1) sao efetivamente usados neste vetor.
        self.match_para = [None] * (2 * n)

    def _tentar_caminho_aumentante(self, atirador, visitado):
        """
        Tenta encontrar um caminho aumentante a partir de
        `atirador`, marcando os alvos considerados em `visitado`
        (reiniciado a cada novo atirador em `resolver`).

        Retorna True se um caminho aumentante foi encontrado e o
        emparelhamento foi atualizado ao longo dele; False caso
        contrario.
        """
        for alvo in self.G.adj[atirador]:
            if alvo in visitado:
                continue
            visitado.add(alvo)

            ocupante_atual = self.match_para[alvo]
            if ocupante_atual is None or self._tentar_caminho_aumentante(
                ocupante_atual, visitado
            ):
                self.match_para[alvo] = atirador
                return True

        return False

    def resolver(self):
        """
        Executa o Algoritmo de Kuhn para todos os N atiradores.

        Retorna:
            list[int] de tamanho N, onde a posicao i contem o alvo
            (1-indexado) escolhido pelo jogador i+1, SE existir
            emparelhamento perfeito.
            None, se nao existir (resposta = Impossible).
        """
        for atirador in range(self.n):
            visitado = set()
            sucesso = self._tentar_caminho_aumentante(atirador, visitado)
            if not sucesso:
                return None   # emparelhamento perfeito impossivel

        assign = [None] * self.n
        for idx_alvo in range(self.n, 2 * self.n):
            atirador = self.match_para[idx_alvo]
            if atirador is not None:
                jogador_atirador = atirador + 1
                jogador_alvo = idx_alvo - self.n + 1
                assign[atirador] = jogador_alvo

        return assign
