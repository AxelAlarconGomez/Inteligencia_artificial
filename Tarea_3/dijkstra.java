package Tarea_3;
import java.util.*;

public class dijkstra {
    // Arista: destino y peso
    static class Edge { 
        int to, w; 
        Edge(int to, int w){ this.to = to; this.w = w; } 
    }

    // Nodo para la cola de prioridad 
    static class Node implements Comparable<Node> {
        int v, d;
        Node(int v, int d){ this.v = v; this.d = d; }
        public int compareTo(Node o){ return Integer.compare(this.d, o.d); }
    }

    static final int INF = 1_000_000_000;

    // Dijkstra: devuelve distancias y llena parent para reconstruir camino
    static int[] dijkstra(List<List<Edge>> g, int src, int[] parent){
        int n = g.size();
        int[] dist = new int[n];
        boolean[] done = new boolean[n];
        Arrays.fill(dist, INF);
        Arrays.fill(parent, -1);

        PriorityQueue<Node> pq = new PriorityQueue<>();
        dist[src] = 0;
        pq.add(new Node(src, 0));

        while(!pq.isEmpty()){
            Node cur = pq.poll();
            int u = cur.v;
            if(done[u]) continue;     // ya quedo con distancia mnima
            done[u] = true;

            for(Edge e : g.get(u)){
                int v = e.to;
                int nd = dist[u] + e.w;  // pesos no negativos
                if(nd < dist[v]){
                    dist[v] = nd;
                    parent[v] = u;
                    pq.add(new Node(v, nd));
                }
            }
        }
        return dist;
    }

    // Reconstruye camino src->t 
    static List<Integer> path(int t, int[] parent, int[] dist){
        if(t < 0 || t >= parent.length || dist[t] >= INF) return Collections.emptyList();
        LinkedList<Integer> p = new LinkedList<>();
        for(int cur = t; cur != -1; cur = parent[cur]) p.addFirst(cur);
        return p;
    }

    public static void main(String[] args){
        int n = 5; 
        List<List<Edge>> g = new ArrayList<>();
        for(int i = 0; i < n; i++) g.add(new ArrayList<>());

        g.get(0).add(new Edge(1, 2));
        g.get(0).add(new Edge(2, 9));
        g.get(1).add(new Edge(2, 2));
        g.get(1).add(new Edge(3, 9));
        g.get(2).add(new Edge(3, 2));
        g.get(3).add(new Edge(4, 2));

        int src = 0, target = 4;
        int[] parent = new int[n];
        int[] dist = dijkstra(g, src, parent);

        System.out.println("Distancias desde " + src + ": " + Arrays.toString(dist));
        List<Integer> p = path(target, parent, dist);
        if(p.isEmpty()) System.out.println("No hay camino " + src + "->" + target);
        else            System.out.println("Camino " + src + "->" + target + ": " + p);
    }
}
