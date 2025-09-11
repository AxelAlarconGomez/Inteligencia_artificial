package Tarea_1;

public class Main {
    public static void main(String[] args) {
        Arbol arbol = new Arbol();
        arbol.insertar("axel");
        arbol.insertar("jimena");
        arbol.insertar("legolas");
        arbol.insertar("arturito");
        arbol.insertar("homero");
        arbol.insertar("rick");

        System.out.println("¿Árbol vacío?: " + arbol.vacio());

        Nodo nodo = arbol.buscarNodo("legolas");
        if (nodo != null) {
            System.out.println("Nodo encontrado: " + nodo.nombre);
        } else {
            System.out.println("Nodo no encontrado");
        }

        System.out.print("Inorden:   "); arbol.inorden();
        System.out.print("Preorden:  "); arbol.preorden();
        System.out.print("Postorden: "); arbol.postorden();
    }
}