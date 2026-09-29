"""
=================================================================
 main_submissao.py
 Ponto de entrada para SUBMISSAO no Kattis - Paintball (T2).

 Sem prints de depuracao ou validacao: le a entrada, resolve via
 KuhnMatcher e imprime exatamente o formato de saida exigido:
   - "Impossible", se nao houver emparelhamento perfeito;
   - N linhas, a i-esima com o alvo do jogador i, caso contrario.
=================================================================
"""

import sys

from grafo_base import LeitorEntrada, construir_grafo_bipartido
from kuhn_matcher import KuhnMatcher


def main():
    sys.setrecursionlimit(10000)  # ver nota de recursao em kuhn_matcher.py

    n, edges = LeitorEntrada.ler()
    G = construir_grafo_bipartido(n, edges)

    matcher = KuhnMatcher(G, n)
    assign = matcher.resolver()

    if assign is None:
        print("Impossible")
        return

    saida = "\n".join(str(alvo) for alvo in assign)
    print(saida)


if __name__ == "__main__":
    main()
