import sys
from edge_weighted_digraph import EdgeWeightedDigraph
from dijkstra_sp import DijkstraSP


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])

    graph = EdgeWeightedDigraph(n)
    idx = 2
    for _ in range(m):
        graph.add_edge(int(data[idx]), int(data[idx + 1]), int(data[idx + 2]))
        idx += 3

    sp = DijkstraSP(graph, 1)
    sys.stdout.write(" ".join(map(str, sp.dist_to[1:])) + "\n")


if __name__ == "__main__":
    main()