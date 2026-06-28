from data.models import Pedido
from telegram.bot import enviar_pedido_recibido, enviar_alerta_stock

class NodoPedido:
    def __init__(self, pedido: Pedido):
        self.pedido = pedido
        self.siguiente = None

class Cola:
    def __init__(self, arbol_referencia): # Recibimos el arbol para buscar el producto
        self._frente = None
        self._final = None
        self._tamanio = 0
        self.arbol = arbol_referencia # Guardamos la referencia

    def enqueue(self, pedido: Pedido):
        nuevo_nodo = NodoPedido(pedido)
        if self._final is None:
            self._frente = nuevo_nodo
            self._final = nuevo_nodo
        else:
            self._final.siguiente = nuevo_nodo
            self._final = nuevo_nodo
        self._tamanio += 1
        enviar_pedido_recibido(pedido.id_pedido, pedido.nombre_producto, pedido.cantidad, self._tamanio)

    def dequeue(self) -> Pedido | None:
        if self._frente is None:
            return None

        pedido_extraido = self._frente.pedido
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tamanio -= 1

        # AHORA SÍ: Buscamos el producto en el árbol usando la referencia
        producto = self.arbol.buscar(pedido_extraido.codigo_producto)
        if producto and producto.tiene_stock_critico():
             enviar_alerta_stock(producto.nombre, producto.codigo, producto.stock)
             
        return pedido_extraido

    # ------------------------------------------------------------------
    # PEEK — Ver sin extraer
    # ------------------------------------------------------------------

    def peek(self) -> Pedido | None:
        """
        Retorna el pedido del frente sin extraerlo.
        Retorna None si la cola está vacía.
        """
        if self._frente is None:
            return None
        return self._frente.pedido

    # ------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------

    def esta_vacia(self) -> bool:
        return self._frente is None

    def tamanio(self) -> int:
        return self._tamanio

    def listar_todos(self) -> list:
        """
        Recorre la cola y retorna una lista con todos los pedidos
        en orden de despacho (frente → final).
        Usado por la GUI para mostrar el estado de la cola.
        """
        resultado = []
        nodo_actual = self._frente
        while nodo_actual is not None:
            resultado.append(nodo_actual.pedido)
            nodo_actual = nodo_actual.siguiente
        return resultado

    def limpiar(self):
        """Vacía completamente la cola."""
        self._frente  = None
        self._final   = None
        self._tamanio = 0

    def __str__(self):
        return f"Cola({self._tamanio} pedidos en espera)"

    def __repr__(self):
        return f"Cola(tamanio={self._tamanio})"
