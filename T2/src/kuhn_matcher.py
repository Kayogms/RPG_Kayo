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

 ORDEM DE LEITURA (= ordem de execucao):
   1. __init__                    prepara o estado (roda 1 vez)
   2. resolve                    laco das rodadas, 1 por atirador
   3. _try_path  busca recursiva chamada pelo
                                  resolve a cada rodada
 Quem dispara tudo e o main.py:
     matcher = KuhnMatcher(G, n)   -> __init__
     assign = matcher.resolve()   -> resolve -> _try_path
=================================================================
"""

from algs4.graph import Graph


class KuhnMatcher:
    """
    Encontra um emparelhamento maximo (e, se existir, perfeito) em
    um grafo bipartido representado por um algs4.graph.Graph, onde:
        - indices 0..N-1     sao os atiradores (A1..AN)
        - indices N..2N-1    sao os alvos      (B1..BN)
    O jogador k (1-indexado) e o atirador k-1 e o alvo N+(k-1).

    Uso:
        matcher = KuhnMatcher(G, n)
        assign = matcher.resolve()   # None se Impossible
    """

    # -------------------------------------------------------------
    # 1. ESTADO INICIAL
    # -------------------------------------------------------------
    def __init__(self, G: Graph, n: int):
        self.G = G
        self.n = n
        # match_to[target_idx] = shooter que atira nesse alvo,
        # ou None se o alvo estiver livre. Comeca tudo livre.
        #
        # Este vetor PERSISTE entre as rodadas: o que um atirador
        # conquistou continua valendo para os proximos, e so muda
        # quando um caminho aumentante e concluido.
        #
        # Tem tamanho 2N para ser indexado direto pelo indice do
        # alvo no grafo; so as posicoes N..2N-1 sao usadas.
        self.match_to = [None] * (2 * n)

    # -------------------------------------------------------------
    # 2. LACO PRINCIPAL: UMA RODADA POR ATIRADOR
    # -------------------------------------------------------------
    def resolve(self):
        """
        Executa o Algoritmo de Kuhn para todos os N atiradores.

        Retorna:
            list[int] de tamanho N, onde a posicao i contem o alvo
            (1-indexado) escolhido pelo jogador i+1, SE existir
            emparelhamento perfeito.
            None, se nao existir (resposta = Impossible).
        """
        for shooter in range(self.n):
            # visited e ZERADO a cada rodada: dentro de uma rodada,
            # cada alvo e tentado no maximo uma vez (evita ciclos);
            # mas o match_to mudou desde a rodada anterior, entao
            # alvos ja explorados antes podem levar a novos caminhos.
            # Por isso o custo total e N rodadas x O(V+E) = O(V.E).
            visited = set()

            success = self._try_path(shooter, visited)

            # Se um unico atirador nao consegue alvo, nenhum
            # emparelhamento perfeito existe: nao adianta continuar.
            if not success:
                return None   # emparelhamento perfeito impossivel

        # Todos os N atiradores foram emparelhados. O match_to
        # esta no sentido "alvo -> quem atira nele"; a saida pede
        # "jogador -> em quem ele atira", entao invertemos.
        assign = [None] * self.n
        for target_idx in range(self.n, 2 * self.n):
            shooter = self.match_to[target_idx]
            if shooter is not None:
                target_player = target_idx - self.n + 1   # indice -> jogador
                assign[shooter] = target_player

        return assign

    # -------------------------------------------------------------
    # 3. BUSCA RECURSIVA DO CAMINHO AUMENTANTE
    # -------------------------------------------------------------
    def _try_path(self, shooter, visited):
        """
        Tenta arranjar um alvo para `shooter`, nem que para isso
        precise deslocar o dono atual de um alvo para outro alvo
        (e assim por diante, em cascata).

        `visited` e o MESMO conjunto em todas as chamadas recursivas
        de uma rodada (criado em `resolve`).

        Retorna True se um caminho aumentante foi encontrado e o
        emparelhamento foi atualizado ao longo dele; False caso
        contrario.
        """
        # Percorre os alvos que o atirador enxerga, na ordem da
        # lista de adjacencia (Bag do algs4: a ultima aresta inserida
        # e a primeira consultada).
        for target in self.G.adj[shooter]:

            # Alvo ja tentado nesta rodada (por este atirador ou por
            # alguem acima na pilha de recursao): pula. Sem isso, dois
            # atiradores poderiam "tomar" o alvo um do outro para sempre.
            if target in visited:
                continue
            visited.add(target)

            owner = self.match_to[target]

            # Duas formas de ficar com o alvo:
            #   - ele esta livre (None); por curto-circuito do `or`,
            #     a recursao nem e chamada; ou
            #   - ele esta ocupado, mas o dono atual consegue trocar
            #     de alvo: chamada recursiva para o owner,
            #     reaproveitando o mesmo `visited`.
            if owner is None or self._try_path(
                owner, visited
            ):
                # Executado na VOLTA da recursao: cada nivel assume o
                # alvo que o nivel de baixo acabou de liberar. Isso
                # inverte as arestas do caminho aumentante e aumenta
                # o emparelhamento em exatamente 1.
                self.match_to[target] = shooter
                return True

            # O dono atual nao conseguiu trocar: tenta o proximo alvo.

        # Nenhum alvo da lista funcionou: quem chamou (o resolve ou
        # o nivel de cima da recursao) recebe False e segue adiante.
        return False
