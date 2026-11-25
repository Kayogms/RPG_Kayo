class EdgeWeightedDigraph:
    def __init__(self, n: int):
        self.V = n
        self.E = 0
        self.adj = [[] for _ in range(n + 1)]

    def add_edge(self, u: int, v: int, weight: int) -> None:
        self.adj[u].append((v, weight))
        self.E += 1