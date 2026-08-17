# =================================================================
# grafo_base.py
# Módulo comum reutilizado pelos Marcos 2, 3 e 4.
# Contém: leitura da entrada, representação do grafo (com medidas
# estruturais e os métodos de busca DFS/BFS) e o DSU (oráculo).
# =================================================================

import sys
import numpy as np
from collections import defaultdict, deque


# -----------------------------------------------------------------
# 1. LEITURA DA ENTRADA
# -----------------------------------------------------------------
class LeitorEntrada:
    """
    Lê a entrada padrão no formato especificado no Marco 1:
        N
        A1 B1
        A2 B2
        ...
        AN BN
    """

    @staticmethod
    def ler(stream=None):
        """
        Retorna um numpy.array de shape (N, 2) e dtype=np.int64,
        onde edges[:, 0] = A_i e edges[:, 1] = B_i.
        """
        stream = stream or sys.stdin
        data = stream.read().split()
        n = int(data[0])

        valores = np.array(data[1:1 + 2 * n], dtype=np.int64)
        edges = valores.reshape(n, 2)

        return edges


# -----------------------------------------------------------------
# 2. GRAFO — REPRESENTAÇÃO, MEDIDAS ESTRUTURAIS E BUSCAS
# -----------------------------------------------------------------
class Graph:
    """
    Lista de adjacência (defaultdict(list)), usando o número
    original do andar como chave (ver justificativa no Marco 2).
    Grafo não direcionado, não ponderado, esparso e potencialmente
    desconexo (ver Marco 1, Seção 2).
    """

    def __init__(self):
        self.adj = defaultdict(list)

    # --- Construção (Marco 2) ------------------------------------
    def construir(self, edges, vertice_partida=1):
        for a, b in edges.tolist():  # conversão em lote (ver Marco 2)
            self.adj[a].append(b)
            self.adj[b].append(a)

        self.adj[vertice_partida]  # garante a chave, mesmo se isolado
        return self

    # --- Acesso básico ----------------------------------------------
    def vizinhos(self, v):
        return self.adj[v]

    def vertices(self):
        return list(self.adj.keys())

    def grau(self, v):
        return len(self.adj[v])

    def __len__(self):
        return len(self.adj)

    def __repr__(self):
        return repr(dict(self.adj))

    # --- Medidas estruturais (Marco 2 / Unidade I) -------------------
    def medidas_estruturais(self, num_arestas):
        graus = {v: self.grau(v) for v in self.adj}
        num_vertices = len(self.adj)

        andar_grau_maximo = max(graus, key=graus.get)
        andar_grau_minimo = min(graus, key=graus.get)
        vertices_isolados = [v for v, g in graus.items() if g == 0]

        densidade = (
            num_arestas / (num_vertices * (num_vertices - 1) / 2)
            if num_vertices > 1 else 0.0
        )

        return {
            "num_vertices": num_vertices,
            "num_arestas": num_arestas,
            "graus": graus,
            "grau_maximo": graus[andar_grau_maximo],
            "andar_grau_maximo": andar_grau_maximo,
            "grau_minimo": graus[andar_grau_minimo],
            "andar_grau_minimo": andar_grau_minimo,
            "vertices_isolados": vertices_isolados,
            "densidade": densidade,
        }

    # --- Marco 3: DFS -------------------------------------------------
    def dfs(self, origem):
        """
        DFS iterativa (pilha explícita) a partir de `origem`.
        Retorna: visitados, predecessor, ordem_visita, maior_andar.
        """
        visitados = {origem}
        predecessor = {origem: None}
        ordem_visita = []
        pilha = [origem]
        maior_andar = origem

        while pilha:
            atual = pilha.pop()
            ordem_visita.append(atual)
            maior_andar = max(maior_andar, atual)

            for vizinho in self.adj[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    predecessor[vizinho] = atual
                    pilha.append(vizinho)

        return {
            "visitados": visitados,
            "predecessor": predecessor,
            "ordem_visita": ordem_visita,
            "maior_andar": maior_andar,
        }

    # --- Marco 4: BFS -------------------------------------------------
    def bfs(self, origem):
        """
        BFS a partir de `origem`.
        Retorna: visitados, nivel, predecessor, maior_andar.
        """
        visitados = {origem}
        nivel = {origem: 0}
        predecessor = {origem: None}
        fila = deque([origem])
        maior_andar = origem

        while fila:
            atual = fila.popleft()
            maior_andar = max(maior_andar, atual)

            for vizinho in self.adj[atual]:
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    nivel[vizinho] = nivel[atual] + 1
                    predecessor[vizinho] = atual
                    fila.append(vizinho)

        return {
            "visitados": visitados,
            "nivel": nivel,
            "predecessor": predecessor,
            "maior_andar": maior_andar,
        }


# -----------------------------------------------------------------
# 3. UNION-FIND / DSU (oráculo de validação)
# -----------------------------------------------------------------
class DSU:
    """
    Conjuntos Disjuntos com compressão de caminho e união por rank.
    Usado exclusivamente como método alternativo de conectividade
    para validar DFS e BFS — não faz parte da solução final.
    """

    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, v):
        if v not in self.parent:
            self.parent[v] = v
            self.rank[v] = 0

    def find(self, v):
        self.make_set(v)
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]

    def union(self, a, b):
        self.make_set(a)
        self.make_set(b)
        raiz_a, raiz_b = self.find(a), self.find(b)
        if raiz_a == raiz_b:
            return
        if self.rank[raiz_a] < self.rank[raiz_b]:
            raiz_a, raiz_b = raiz_b, raiz_a
        self.parent[raiz_b] = raiz_a
        if self.rank[raiz_a] == self.rank[raiz_b]:
            self.rank[raiz_a] += 1

    def maior_no_conjunto(self, origem):
        raiz_origem = self.find(origem)
        return max(v for v in self.parent if self.find(v) == raiz_origem)

    @classmethod
    def construir_de_arestas(cls, edges, origem=1):
        """Constrói um DSU já unindo todas as arestas fornecidas."""
        dsu = cls()
        for a, b in edges.tolist():
            dsu.union(a, b)
        dsu.make_set(origem)
        return dsu


# -----------------------------------------------------------------
# 4. VALIDAÇÃO ESTRUTURAL (Sample 1) — reutilizada nos Marcos 2, 3 e 4
# -----------------------------------------------------------------
ESPERADO_SAMPLE_1 = {
    1:  {4},
    3:  {4, 8},
    4:  {1, 3, 10},
    8:  {3},
    10: {4},
}


def validar_estrutura(grafo: Graph):
    """Confere a lista de adjacência contra o Sample 1 (Marco 2)."""
    for andar, vizinhos_esperados in ESPERADO_SAMPLE_1.items():
        vizinhos_obtidos = set(grafo.vizinhos(andar))
        assert vizinhos_obtidos == vizinhos_esperados, (
            f"Falha na validação estrutural: andar {andar} — "
            f"esperado {vizinhos_esperados}, obtido {vizinhos_obtidos}"
        )
    print("[OK] Validação estrutural (lista de adjacência) — Sample 1")