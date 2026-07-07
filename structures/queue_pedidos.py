#  La Cola SOLO administra el orden FIFO. No conoce el árbol
#  ni envía notificaciones: esas tareas viven en la interfaz.
from data.models import Pedido


class NodoPedido:
    def __init__(self, pedido: Pedido):
        self.pedido = pedido
        self.siguiente = None


class Cola:
    def __init__(self):
        self._frente = None
        self._final = None
        self._tamanio = 0

    def enqueue(self, pedido: Pedido):
        nuevo_nodo = NodoPedido(pedido)
        if self._final is None:
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo
        self._tamanio += 1

    def dequeue(self) -> Pedido | None:
        if self._frente is None:
            return None
        pedido_extraido = self._frente.pedido
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tamanio -= 1
        return pedido_extraido

    def peek(self) -> Pedido | None:
        if self._frente is None:
            return None
        return self._frente.pedido

    def esta_vacia(self) -> bool:
        return self._frente is None

    def tamanio(self) -> int:
        return self._tamanio

    def listar_todos(self) -> list:
        resultado = []
        nodo_actual = self._frente
        while nodo_actual is not None:
            resultado.append(nodo_actual.pedido)
            nodo_actual = nodo_actual.siguiente
        return resultado

    def limpiar(self):
        self._frente = None
        self._final = None
        self._tamanio = 0

    def __str__(self):
        return f"Cola({self._tamanio} pedidos en espera)"