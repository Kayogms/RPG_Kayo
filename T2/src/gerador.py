"""
=================================================================
 gerador.py
 Ferramenta de apoio ao desenvolvimento - gera casos de teste
 para o Kattis Paintball (T2), no formato de entrada esperado:
     N M
     u1 v1
     ...
     uM vM

 Ferramenta auxiliar de apoio aos testes, localizada em src/ juntamente
 com os demais scripts de desenvolvimento.

 Uso:
     python gerador.py sample1        > sample1.txt
     python gerador.py impossible     > impossible.txt
     python gerador.py stress       > stress.txt
     python gerador.py stress --seed 42 --n 1000 --m 5000 > stress2.txt
=================================================================
"""

import argparse
import random
import sys


def generate_sample1():
    """Instancia do Marco 1: ciclo de 4 jogadores (garante Accepted)."""
    n = 4
    edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    return n, edges


def generate_impossible():
    """
    Caso proposital sem emparelhamento perfeito: os jogadores 2 e 3
    so enxergam o jogador 1, entao ambos disputariam o mesmo (unico)
    alvo possivel.
    """
    n = 3
    edges = [(1, 2), (1, 3)]
    return n, edges


def generate_stress(n=1000, m=5000, seed=None):
    """
    Gera um caso de estresse com N e M proximos do limite maximo
    das restricoes do problema (N <= 1000, M <= 5000).

    Garante que existe emparelhamento perfeito: comeca com um ciclo
    hamiltoniano (1-2, 2-3, ..., N-1), que sozinho ja garante uma
    solucao valida (M = N arestas), e completa o restante das
    arestas (ate M) com pares aleatorios distintos, sem repetir
    pares ja usados.
    """
    if seed is not None:
        random.seed(seed)

    if m < n:
        raise ValueError(
            f"M={m} precisa ser >= N={n} para garantir emparelhamento "
            f"perfeito com este gerador (o ciclo base usa N arestas)."
        )
    if m > n * (n - 1) // 2:
        raise ValueError(
            f"M={m} excede o numero maximo de pares distintos para N={n}."
        )

    edges = set()

    # Ciclo base: garante que 1..N e um componente conexo com
    # emparelhamento perfeito trivial (vizinho seguinte no ciclo).
    for i in range(1, n + 1):
        j = i + 1 if i < n else 1
        pair = (min(i, j), max(i, j))
        edges.add(pair)

    # Completa ate M arestas com pares aleatorios adicionais.
    while len(edges) < m:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u == v:
            continue
        pair = (min(u, v), max(u, v))
        edges.add(pair)

    return n, sorted(edges)


def print_case(n, edges, stream=None):
    stream = stream or sys.stdout
    print(f"{n} {len(edges)}", file=stream)
    for u, v in edges:
        print(f"{u} {v}", file=stream)


def main():
    parser = argparse.ArgumentParser(
        description="Gerador de casos de teste - Kattis Paintball (T2)"
    )
    parser.add_argument(
        "kind",
        choices=["sample1", "impossible", "stress"],
        help="tipo de caso de teste a gerar",
    )
    parser.add_argument("--n", type=int, default=1000, help="numero de jogadores (so para 'stress')")
    parser.add_argument("--m", type=int, default=5000, help="numero de arestas (so para 'stress')")
    parser.add_argument("--seed", type=int, default=None, help="semente aleatoria (so para 'stress')")
    args = parser.parse_args()

    if args.kind == "sample1":
        n, edges = generate_sample1()
    elif args.kind == "impossible":
        n, edges = generate_impossible()
    else:
        n, edges = generate_stress(n=args.n, m=args.m, seed=args.seed)

    print_case(n, edges)


if __name__ == "__main__":
    main()
