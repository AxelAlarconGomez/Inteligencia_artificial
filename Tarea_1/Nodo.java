package Tarea_1;

public class Nodo {
    String nombre;
    Nodo izquierdo;
    Nodo derecho;

    public Nodo(String nombre) {
        this.nombre = nombre;
        this.izquierdo = null;
        this.derecho = null;
    }

    @Override
    public String toString() {
        return nombre;
    }
}
