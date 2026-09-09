"""
=================================================================
 Trabalho Prático 1 - Resolução de Problemas com Grafos
 Problema I: Ladder Takahashi (AtCoder ABC277 C)
 
 Este arquivo unifica a representação do grafo (Lista de Adjacência
 com compressão de coordenadas) e a travessia escolhida (BFS iterativa)
 em um script autossuficiente para submissão em juízes online.
=================================================================
"""

import sys
import numpy as np
from collections import deque

# =================================================================
# 1. CLASSES DE REFERÊNCIA (Substituindo o pacote algs4)
# =================================================================
class Graph:
    """Implementação minimalista equivalente ao algs4.graph.Graph"""
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(V)]

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)
        self.E += 1


class BreadthFirstPaths:
    """Implementação minimalista equivalente ao algs4.breadth_first_paths"""
    def __init__(self, G, s):
        self.marked = [False] * G.V
        self.edge_to = [None] * G.V
        self.s = s
        self._bfs(G, s)

    def _bfs(self, G, s):
        queue = deque([s])
        self.marked[s] = True
        while queue:
            v = queue.popleft()
            for w in G.adj[v]:
                if not self.marked[w]:
                    self.edge_to[w] = v
                    self.marked[w] = True
                    queue.append(w)

    def has_path_to(self, v):
        return self.marked[v]


# =================================================================
# 2. LEITURA E REPRESENTAÇÃO COMPUTACIONAL
# =================================================================
class LeitorEntrada:
    @staticmethod
    def ler():
        # Leitura otimizada de toda a entrada padrão
        data = sys.stdin.read().split()
        if not data:
            return np.array([], dtype=np.int64).reshape(0, 2)
        n = int(data[0])
        valores = np.array(data[1:1 + 2 * n], dtype=np.int64)
        edges = valores.reshape(n, 2)
        return edges


class LadderSymbolGraph:
    """Compressão de coordenadas: mapeia andares reais para índices (0 a V-1)"""
    def __init__(self, edges, vertice_partida=1):
        self._st = {}
        
        # Iteração convertendo para lista nativa
        for a, b in edges.tolist():
            if a not in self._st:
                self._st[a] = len(self._st)
            if b not in self._st:
                self._st[b] = len(self._st)

        # Garante a presença do vértice de partida (Andar 1)
        if vertice_partida not in self._st:
            self._st[vertice_partida] = len(self._st)

        # Vetor inverso para consulta: índice -> andar original
        self._keys = [0] * len(self._st)
        for andar, idx in self._st.items():
            self._keys[idx] = andar

        # Constrói o Grafo
        self._G = Graph(len(self._st))
        for a, b in edges.tolist():
            self._G.add_edge(self._st[a], self._st[b])

    def index(self, andar):
        return self._st[andar]

    def name(self, v):
        return self._keys[v]

    def graph(self):
        return self._G


# =================================================================
# 3. ALGORITMO DE BUSCA E RESOLUÇÃO FINAL
# =================================================================
def maior_andar_via_bfs(G, sg, origem_idx):
    """Executa a BFS original e converte os índices alcançáveis no maior andar"""
    bfs = BreadthFirstPaths(G, origem_idx)
    maior = sg.name(origem_idx)
    
    for v in range(G.V):
        if bfs.has_path_to(v):
            maior = max(maior, sg.name(v))
            
    return maior


def main():
    edges = LeitorEntrada.ler()
    
    # Prevenção de segurança para entradas vazias
    if edges.size == 0:
        print(1)
        return

    # Integração das camadas (Modelagem -> Representação -> Busca)
    sg = LadderSymbolGraph(edges, vertice_partida=1)
    G = sg.graph()
    origem_idx = sg.index(1)
    
    maior = maior_andar_via_bfs(G, sg, origem_idx)
    
    # Imprime estritamente o valor do andar alcançado (Saída exigida)
    print(maior)


if __name__ == "__main__":
    main()