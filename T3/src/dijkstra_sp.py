import heapq

INF = 10**18


class DijkstraSP:
    def __init__(self, graph, source: int):
        self.dist_to = [INF] * (graph.V + 1)
        self.dist_to[source] = 0
        self._run(graph, source)

    def _run(self, graph, source: int) -> None:
        dist = self.dist_to
        adj = graph.adj
        pq = [(0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))