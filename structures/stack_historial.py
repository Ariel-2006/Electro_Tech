# Registra transacciones de despacho para poder deshacerlas. Guarda solo RegistroTransaccional 
# [ID_Pedido, ID_Producto, Cantidad] para evitar duplicar objetos Producto completos en memoria.

from data.models import RegistroTransaccional


class NodoPila:
    """Nodo de la pila. Contiene un RegistroTransaccional y apunta al nodo inferior."""

    def __init__(self, registro: RegistroTransaccional):
        self.registro = registro
        self.inferior = None   # Nodo debajo en la pila


class Pila:
    """
    Pila LIFO (Last In, First Out) de registros transaccionales.

    Estructura interna:
        cima → [NodoN]         ← último en entrar / primero en salir
               [NodoN-1]
               [NodoN-2]
                  ...
               [Nodo1]

    Métodos:
        push(registro)              → Apila un registro        O(1)
        pop()  → RegistroTx | None  → Desapila el último       O(1)
        peek() → RegistroTx | None  → Ve la cima sin desapilar O(1)
        esta_vacia() → bool                                     O(1)
        tamanio()    → int                                      O(1)
        listar_todo() → list  → Para visualización GUI          O(n)
    """

    def __init__(self):
        self._cima     = None
        self._tamanio  = 0

    # Función para apilar un nuevo registro transaccional en la cima de la pila.
    def push(self, registro: RegistroTransaccional):
        """Apila un nuevo registro transaccional en la cima."""
        nuevo_nodo          = NodoPila(registro)
        nuevo_nodo.inferior = self._cima
        self._cima          = nuevo_nodo
        self._tamanio      += 1

    # Función para desapilar el registro de la cima de la pila y devolverlo.
    def pop(self) -> RegistroTransaccional | None:
        """
        Extrae y retorna el registro de la cima.
        Retorna None si la pila está vacía.
        Usar este valor para reintegrar el stock al BST.
        """
        if self._cima is None:
            return None

        registro_extraido = self._cima.registro
        self._cima        = self._cima.inferior
        self._tamanio    -= 1
        return registro_extraido

    # Función para ver el registro de la cima sin extraerlo.
    def peek(self) -> RegistroTransaccional | None:
        """
        Retorna el registro de la cima sin extraerlo.
        Retorna None si la pila está vacía.
        """
        if self._cima is None:
            return None
        return self._cima.registro

    # Funciones: esta_vacia, tamanio, listar_todo, limpiar
    def esta_vacia(self) -> bool:
        return self._cima is None

    def tamanio(self) -> int:
        return self._tamanio

    def listar_todo(self) -> list:
        """
        Recorre la pila de cima a base y retorna lista de registros.
        El índice 0 es el más reciente (cima).
        Usado por la GUI para mostrar historial de despachos.
        """
        resultado   = []
        nodo_actual = self._cima
        while nodo_actual is not None:
            resultado.append(nodo_actual.registro)
            nodo_actual = nodo_actual.inferior
        return resultado

    def limpiar(self):
        """Vacía completamente la pila."""
        self._cima    = None
        self._tamanio = 0

    def __str__(self):
        return f"Pila({self._tamanio} registros, cima={self.peek()})"

    def __repr__(self):
        return f"Pila(tamanio={self._tamanio})"