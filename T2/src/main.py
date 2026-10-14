"""
=================================================================
 main.py
 Ponto de entrada de DESENVOLVIMENTO - Kattis Paintball (T2).
=================================================================
"""

import sys

from grafo_base import (
    InputReader,
    build_bipartite_graph,
    validate_structure,
    N_SAMPLE_1,
    EDGES_SAMPLE_1,
)
from kuhn_matcher import KuhnMatcher


def main():
    sys.setrecursionlimit(10000)  # ver nota de recursao em kuhn_matcher.py

    n, edges = InputReader.read()

    if n == 0:
        print("Entrada vazia.")
        return

    G = build_bipartite_graph(n, edges)

    # Validacao estrutural: so roda de forma significativa quando a
    # entrada e exatamente a instancia pequena do Marco 1.
    if n == N_SAMPLE_1 and set(edges) == set(EDGES_SAMPLE_1):
        validate_structure(G)
        print()

    matcher = KuhnMatcher(G, n)
    assign = matcher.resolve()

    if assign is None:
        print("Impossible")
        return

    print("=== Emparelhamento encontrado ===")
    for player in range(1, n + 1):
        target = assign[player - 1]
        print(f"atirador {player} -> alvo {target}")

    # Conferencia: todo alvo deve ser usado exatamente uma vez.
    used_targets = sorted(assign)
    assert used_targets == list(range(1, n + 1)), (
        "Inconsistencia: nem todo jogador foi usado como alvo "
        "exatamente uma vez."
    )
    print("\n[OK] Emparelhamento perfeito confirmado "
          f"({n} de {n} jogadores emparelhados).")


if __name__ == "__main__":
    main()
