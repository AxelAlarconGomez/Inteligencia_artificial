from collections import deque, defaultdict
import heapq
from math import hypot

# ------------ Utilidades ------------
def _neighbors_unweighted(G, u):
    # G: dict[u] -> iterable[v]  ó  dict[u] -> iterable[(v,c)]
    for w in G[u]:
        if isinstance(w, tuple) and len(w) == 2:
            yield w[0]
        else:
            yield w

def _neighbors_weighted(G, u):
    # Devuelve (v,costo). Si no hay costos, asume 1.
    for w in G[u]:
        if isinstance(w, tuple) and len(w) == 2:
            yield w
        else:
            yield (w, 1)

def reconstruir_camino(padre, goal):
    if goal not in padre: 
        return None
    path = [goal]
    while padre[path[-1]] is not None:
        path.append(padre[path[-1]])
    path.reverse()
    return path

# ------------ 1) Búsqueda Primero en Anchura (BFS) ------------
def bfs(G, start, goal):
    """G: dict[u] -> [v] o [(v,c)]  (ignora costos, trata como no ponderado)."""
    q = deque([start])
    visitado = {start}
    padre = {start: None}
    while q:
        u = q.popleft()
        if u == goal: 
            return reconstruir_camino(padre, goal)
        for v in _neighbors_unweighted(G, u):
            if v not in visitado:
                visitado.add(v)
                padre[v] = u
                q.append(v)
    return None

# ------------ 2) Búsqueda Primero en Profundidad (DFS, iterativa) ------------
def dfs(G, start, goal):
    """No recursiva para evitar límites de recursión."""
    stack = [start]
    visitado = {start}
    padre = {start: None}
    while stack:
        u = stack.pop()
        if u == goal:
            return reconstruir_camino(padre, goal)
        for v in _neighbors_unweighted(G, u):
            if v not in visitado:
                visitado.add(v)
                padre[v] = u
                stack.append(v)
    return None

# ------------ 3) Búsqueda de Costo Uniforme (UCS) ------------
def ucs(G, start, goal):
    """G: dict[u] -> [(v, costo)] o [v] (si no hay costos, asume 1). Devuelve (camino, costo)."""
    pq = [(0, start)]
    costo = {start: 0}
    padre = {start: None}
    visitado = set()

    while pq:
        g_u, u = heapq.heappop(pq)
        if u in visitado:
            continue
        visitado.add(u)
        if u == goal:
            return reconstruir_camino(padre, goal), g_u
        for v, c in _neighbors_weighted(G, u):
            if v in visitado:
                continue
            nuevo = g_u + c
            if nuevo < costo.get(v, float('inf')):
                costo[v] = nuevo
                padre[v] = u
                heapq.heappush(pq, (nuevo, v))
    return None, float('inf')

# ------------ Opcionales ------------

# 3.a) Búsqueda Bidireccional para grafos no ponderados
def bidirectional_bfs(G, start, goal):
    if start == goal:
        return [start]
    frontA, frontB = {start}, {goal}
    padreA, padreB = {start: None}, {goal: None}
    qA, qB = deque([start]), deque([goal])

    while qA and qB:
        # Expande desde A
        for _ in range(len(qA)):
            u = qA.popleft()
            for v in _neighbors_unweighted(G, u):
                if v not in padreA:
                    padreA[v] = u
                    qA.append(v)
                    if v in padreB:
                        # Encuentro
                        meet = v
                        # Reconstruir
                        path1 = []
                        x = meet
                        while x is not None:
                            path1.append(x)
                            x = padreA[x]
                        path1.reverse()
                        path2 = []
                        y = padreB[meet]
                        while y is not None:
                            path2.append(y)
                            y = padreB[y]
                        return path1 + path2
        # Expande desde B
        for _ in range(len(qB)):
            u = qB.popleft()
            for v in _neighbors_unweighted(G, u):
                if v not in padreB:
                    padreB[v] = u
                    qB.append(v)
                    if v in padreA:
                        meet = v
                        path1 = []
                        x = padreA[meet]
                        while x is not None:
                            path1.append(x)
                            x = padreA[x]
                        path1.reverse()
                        path2 = []
                        y = meet
                        while y is not None:
                            path2.append(y)
                            y = padreB[y]
                        return path1 + path2
    return None

# 3.b) Profundidad Limitada (DLS)
def depth_limited_search(G, start, goal, limite):
    stack = [(start, 0)]
    padre = {start: None}
    visitado_en_nivel = set([start])
    while stack:
        u, d = stack.pop()
        if u == goal:
            return reconstruir_camino(padre, goal)
        if d < limite:
            for v in _neighbors_unweighted(G, u):
                # permitir revisitar si hay mejor nivel
                if (v, d+1) not in visitado_en_nivel:
                    if v not in padre:
                        padre[v] = u
                    stack.append((v, d+1))
                    visitado_en_nivel.add((v, d+1))
    return None  # o "cutoff" si quieres distinguir

# 3.c) Profundidad Iterativa (IDS)
def iterative_deepening_search(G, start, goal, limite_max=50):
    for L in range(limite_max + 1):
        res = depth_limited_search(G, start, goal, L)
        if res is not None:
            return res
    return None

# ------------ Heurística ------------
# Ejemplo de función heurística h(n) si tienes coordenadas de nodos.
# coords: dict[nodo] -> (x,y)
def h_euclidea(n, goal, coords):
    x1, y1 = coords[n]
    x2, y2 = coords[goal]
    return hypot(x1 - x2, y1 - y2)

# Plantilla de A* 
def a_star(G, start, goal, h, h_ctx=None):
    """h(n, goal, h_ctx) -> estimación al objetivo. h_ctx es tu contexto (ej. coords)."""
    pq = [(0, 0, start)]
    padre = {start: None}
    g = {start: 0}
    visitado = set()

    while pq:
        f_u, g_u, u = heapq.heappop(pq)
        if u in visitado:
            continue
        visitado.add(u)

        if u == goal:
            return reconstruir_camino(padre, goal), g_u

        for v, c in _neighbors_weighted(G, u):
            if v in visitado:
                continue
            tentative = g_u + c
            if tentative < g.get(v, float('inf')):
                g[v] = tentative
                padre[v] = u
                hv = h(v, goal, h_ctx) if h_ctx is not None else h(v, goal)
                heapq.heappush(pq, (tentative + hv, tentative, v))
    return None, float('inf')

if __name__ == "__main__":
    # Grafo simple no ponderado
    G = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    print("BFS A->F:", bfs(G, 'A', 'F'))
    print("DFS A->F:", dfs(G, 'A', 'F'))
    print("Bidireccional A->F:", bidirectional_bfs(G, 'A', 'F'))

    # Grafo ponderado
    Gw = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('D', 2), ('E', 5)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 2)],
        'E': [('B', 5), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }

    print("UCS A->F:", ucs(Gw, 'A', 'F'))
