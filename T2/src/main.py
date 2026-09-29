"""
=================================================================
 main.py
 Ponto de entrada de DESENVOLVIMENTO - Kattis Paintball (T2).

 Executa: leitura da entrada, construcao do grafo bipartido,
 validacao estrutural (Sample 1, quando aplicavel) e resolucao
 via KuhnMatcher, com saida detalhada para conferencia manual.

 NAO usar este arquivo para submissao ao Kattis - use
 main_submissao.py, que nao imprime nada alem da resposta exigida.
=================================================================
"""

import sys

from grafo_base import (
    LeitorEntrada,
    construir_grafo_bipartido,
    validar_estrutura,
    N_SAMPLE_1,
    EDGES_SAMPLE_1,
)
from kuhn_matcher import KuhnMatcher


def main():
    sys.setrecursionlimit(10000)  # ver nota de recursao em kuhn_matcher.py

    n, edges = LeitorEntrada.ler()

    if n == 0:
        print("Entrada vazia.")
        return

    G = construir_grafo_bipartido(n, edges)

    # Validacao estrutural: so roda de forma significativa quando a
    # entrada e exatamente a instancia pequena do Marco 1.
    if n == N_SAMPLE_1 and set(edges) == set(EDGES_SAMPLE_1):
        validar_estrutura(G)
        print()

    matcher = KuhnMatcher(G, n)
    assign = matcher.resolver()

    if assign is None:
        print("Impossible")
        return

    print("=== Emparelhamento encontrado ===")
    for jogador in range(1, n + 1):
        alvo = assign[jogador - 1]
        print(f"atirador {jogador} -> alvo {alvo}")

    # Conferencia: todo alvo deve ser usado exatamente uma vez.
    alvos_usados = sorted(assign)
    assert alvos_usados == list(range(1, n + 1)), (
        "Inconsistencia: nem todo jogador foi usado como alvo "
        "exatamente uma vez."
    )
    print("\n[OK] Emparelhamento perfeito confirmado "
          f"({n} de {n} jogadores emparelhados).")


if __name__ == "__main__":
    main()
