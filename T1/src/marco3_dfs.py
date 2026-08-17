# =================================================================
# marco3_dfs.py
# Marco 3 — Aplicação básica de DFS.
# Executa a DFS a partir do andar 1 e valida o resultado comparando
# com o DSU (oráculo). A BFS ainda não está disponível neste marco.
# =================================================================

from grafo_base import LeitorEntrada, Graph, DSU, validar_estrutura


class ValidadorDFS:
    """
    Validador do Marco 3:
      1. Valida a estrutura do grafo (Sample 1) — reaproveitado do Marco 2.
      2. Executa a DFS a partir da origem.
      3. Exibe estados de visita, predecessores, ordem de visita e o
         maior andar alcançado.
      4. Compara o resultado da DFS com o DSU (único método alternativo
         disponível até este marco).
    """

    @staticmethod
    def validar(grafo: Graph, edges, origem=1):
        resultado_dfs = grafo.dfs(origem)

        print("=== Execução da DFS ===")
        print(f"Origem:                 {origem}")
        print(f"Vértices visitados:     {sorted(resultado_dfs['visitados'])}")
        print(f"Ordem de visita:        {resultado_dfs['ordem_visita']}")
        print(f"Predecessores:          {resultado_dfs['predecessor']}")
        print(f"Maior andar (DFS):      {resultado_dfs['maior_andar']}")
        print()

        # --- Comparação com o DSU (oráculo) ---
        dsu = DSU.construir_de_arestas(edges, origem=origem)
        maior_dsu = dsu.maior_no_conjunto(origem)

        print("=== Comparação DFS x DSU ===")
        print(f"DFS -> maior andar alcançável: {resultado_dfs['maior_andar']}")
        print(f"DSU -> maior andar alcançável: {maior_dsu}")

        assert resultado_dfs["maior_andar"] == maior_dsu, (
            f"Divergência entre DFS ({resultado_dfs['maior_andar']}) "
            f"e DSU ({maior_dsu})!"
        )
        print(f"[OK] DFS e DSU concordam: resposta = {resultado_dfs['maior_andar']}")

        return resultado_dfs["maior_andar"]


def main():
    edges = LeitorEntrada.ler()
    grafo = Graph().construir(edges, vertice_partida=1)

    validar_estrutura(grafo)
    print()

    ValidadorDFS.validar(grafo, edges, origem=1)


if __name__ == "__main__":
    main()