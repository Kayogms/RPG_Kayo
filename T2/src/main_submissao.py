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
class LeitorEntrada:
    """Leitura de alta performance de toda a entrada padrão."""

    @staticmethod
    def ler():
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


def construir_grafo_bipartido(n: int, edges: list):
    """
    Constrói o grafo bipartido de tamanho 2N:
        - Atiradores (jogadores 1..N): índices 0 .. N-1
        - Alvos      (jogadores 1..N): índices N .. 2N-1
    """
    G = Graph(2 * n)
    for u, v in edges:
        atirador_u, atirador_v = u - 1, v - 1
        alvo_u, alvo_v = n + (u - 1), n + (v - 1)
        G.add_edge(atirador_u, alvo_v)
        G.add_edge(atirador_v, alvo_u)
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
        # match_para[alvo] = índice do atirador que está casando com esse alvo
        self.match_para = [None] * (2 * n)

    def _tentar_caminho_aumentante(self, atirador: int, visitado: set) -> bool:
        """
        Busca em profundidade para encontrar um caminho aumentante a partir de
        um atirador livre, desalocando e realocando em cascata se necessário.
        """
        for alvo in self.G.adj[atirador]:
            if alvo in visitado:
                continue
            visitado.add(alvo)

            ocupante_atual = self.match_para[alvo]
            # Se o alvo está vago OU o ocupante atual puder ser deslocado:
            if ocupante_atual is None or self._tentar_caminho_aumentante(
                ocupante_atual, visitado
            ):
                self.match_para[alvo] = atirador
                return True

        return False

    def resolver(self):
        """
        Executa a busca para todos os N atiradores.
        Retorna:
            list[int] de tamanho N com os alvos atribuídos (1-indexados)
            ou None caso seja impossível atingir emparelhamento perfeito.
        """
        for atirador in range(self.n):
            visitado = set()
            if not self._tentar_caminho_aumentante(atirador, visitado):
                return None  # Emparelhamento de tamanho N é impossível

        # Reconstrói a atribuição final: para cada atirador, quem ele acertou
        assign = [None] * self.n
        for idx_alvo in range(self.n, 2 * self.n):
            atirador = self.match_para[idx_alvo]
            if atirador is not None:
                jogador_alvo = idx_alvo - self.n + 1
                assign[atirador] = jogador_alvo

        return assign


# =================================================================
# 4. PONTO DE ENTRADA PARA O JUIZ ONLINE
# =================================================================
def main():
    n, edges = LeitorEntrada.ler()
    if n == 0:
        print("Impossible")
        return

    G = construir_grafo_bipartido(n, edges)
    matcher = KuhnMatcher(G, n)
    assign = matcher.resolver()

    if assign is None:
        print("Impossible")
        return

    # Escrita rápida em stdout
    sys.stdout.write("\n".join(str(alvo) for alvo in assign) + "\n")


if __name__ == "__main__":
    main()
