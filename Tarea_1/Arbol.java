package Tarea_1;

public class Arbol {
    private Nodo raiz;

    public Arbol() {
        this.raiz = null;
    }

    //Verifica si el árbol está vacío. 
    public boolean vacio() {
        return this.raiz == null;
    }
    //Inserta un nuevo nodo en el árbol.
    public void insertar(String nombre) {
        Nodo nuevo = new Nodo(nombre);
        if (raiz == null) {
            raiz = nuevo;
        } else {
            insertarRec(raiz, nuevo);
        }
    }	

    private void insertarRec(Nodo actual, Nodo nuevo) {
        // Comparación case-insensitive
        int cmp = nuevo.nombre.compareToIgnoreCase(actual.nombre);

        if (cmp < 0) { // nuevo < actual -> va a la izquierda
            if (actual.izquierdo == null) {
                actual.izquierdo = nuevo;
            } else {
                insertarRec(actual.izquierdo, nuevo);
            }
        } else {
            // Por convención, los duplicados (cmp == 0) los mandamos a la derecha
            if (actual.derecho == null) {
                actual.derecho = nuevo;
            } else {
                insertarRec(actual.derecho, nuevo);
            }
        }
    }

    //Busca un nodo por nombre utilizando el ABB (devuelve el Nodo o null).
    public Nodo buscarNodo(String nombre) {
        return buscarRec(raiz, nombre);
    }

    private Nodo buscarRec(Nodo actual, String nombre) {
        if (actual == null) return null;

        int cmp = nombre.compareToIgnoreCase(actual.nombre);
        if (cmp == 0) {
            return actual;
        } else if (cmp < 0) {
            return buscarRec(actual.izquierdo, nombre);
        } else {
            return buscarRec(actual.derecho, nombre);
        }
    }

    // Recorridos para visualizar el árbol 
    public void inorden() { inordenRec(raiz); System.out.println(); }
    private void inordenRec(Nodo n) {
        if (n == null) return;
        inordenRec(n.izquierdo);
        System.out.print(n.nombre + " ");
        inordenRec(n.derecho);
    }

    public void preorden() { preordenRec(raiz); System.out.println(); }
    private void preordenRec(Nodo n) {
        if (n == null) return;
        System.out.print(n.nombre + " ");
        preordenRec(n.izquierdo);
        preordenRec(n.derecho);
    }

    public void postorden() { postordenRec(raiz); System.out.println(); }
    private void postordenRec(Nodo n) {
        if (n == null) return;
        postordenRec(n.izquierdo);
        postordenRec(n.derecho);
        System.out.print(n.nombre + " ");
    }
    
  
}


