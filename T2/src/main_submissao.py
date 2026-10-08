"""
=================================================================
 Trabalho Prático 2 - Resolução de Problemas com Grafos
 Problema: Paintball (Kattis - paintball)
 
 Este arquivo unifica a representação do grafo bipartido
 e o Algoritmo de Kuhn (busca de caminhos aumentantes via DFS)
 em um script autossuficiente e otimizado para submissão no
 juiz online Kattis, sem dependências externas de pacotes.
=================================================================
"""

import sys

# Elevação segura do limite de chamadas recursivas para prevenir RecursionError
# em cadeias de realocação no pior caso (N <= 1000).
sys.setrecursionlimit(200000)


# =================================================================
# 1. CLASSES DE REFERÊNCIA (Substituindo o pacote algs4)
# =================================================================
class Graph:
    """Implementação minimalista equivalente ao algs4.graph.Graph."""

    def __init__(self, V: int):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(V)]

    def add_edge(self, v: int, w: int):
        self.adj[v].append(w)
        self.adj[w].append(v)
        self.E += 1


# =================================================================
# 2. LEITURA E REPRESENTAÇÃO COMPUTACIONAL (GRAFO BIPARTIDO)
# =================================================================
class InputReader:
    """Leitura de alta performance de toda a entrada padrão."""

    @staticmethod
    def read():
        data = sys.stdin.read().lstrip('\ufeff').split()
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


def build_bipartite_graph(n: int, edges: list):
    """
    Constrói o grafo bipartido de tamanho 2N:
        - Atiradores (jogadores 1..N): índices 0 .. N-1
        - Alvos      (jogadores 1..N): índices N .. 2N-1
    """
    G = Graph(2 * n)
    for u, v in edges:
        shooter_u, shooter_v = u - 1, v - 1
        target_u, target_v = n + (u - 1), n + (v - 1)
        G.add_edge(shooter_u, target_v)
        G.add_edge(shooter_v, target_u)
    return G


# =================================================================
# 3. ALGORITMO DE EMPARELHAMENTO BIPARTIDO (KUHN)
# =================================================================
class KuhnMatcher:
    """
    Algoritmo de Kuhn para Emparelhamento Máximo em Grafo Bipartido.
    Utiliza DFS para encontrar caminhos aumentantes alternados.
    """

    def __init__(self, G: Graph, n: int):
        self.G = G
        self.n = n
        # match_to[target_idx] = índice do shooter que está casando com esse alvo
        self.match_to = [None] * (2 * n)

    def _try_path(self, shooter: int, visited: set) -> bool:
        """
        Busca em profundidade para encontrar um caminho aumentante a partir de
        um atirador livre, desalocando e realocando em cascata se necessário.
        """
        for target in self.G.adj[shooter]:
            if target in visited:
                continue
            visited.add(target)

            owner = self.match_to[target]
            # Se o alvo está vago OU o ocupante atual puder ser deslocado:
            if owner is None or self._try_path(
                owner, visited
            ):
                self.match_to[target] = shooter
                return True

        return False

    def resolve(self):
        """
        Executa a busca para todos os N atiradores.
        Retorna:
            list[int] de tamanho N com os alvos atribuídos (1-indexados)
            ou None caso seja impossível atingir emparelhamento perfeito.
        """
        for shooter in range(self.n):
            visited = set()
            if not self._try_path(shooter, visited):
                return None  # Emparelhamento de tamanho N é impossível

        # Reconstrói a atribuição final: para cada atirador, quem ele acertou
        assign = [None] * self.n
        for target_idx in range(self.n, 2 * self.n):
            shooter = self.match_to[target_idx]
            if shooter is not None:
                target_player = target_idx - self.n + 1
                assign[shooter] = target_player

        return assign


# =================================================================
# 4. PONTO DE ENTRADA PARA O JUIZ ONLINE
# =================================================================
def main():
    n, edges = InputReader.read()
    if n == 0:
        print("Impossible")
        return

    G = build_bipartite_graph(n, edges)
    matcher = KuhnMatcher(G, n)
    assign = matcher.resolve()

    if assign is None:
        print("Impossible")
        return

    # Escrita rápida em stdout
    sys.stdout.write("\n".join(str(target) for target in assign) + "\n")


if __name__ == "__main__":
    main()
