# =============================================================
#  ElectroTech Store — Cola FIFO de despacho de pedidos
#  Archivo: structures/queue_pedidos.py
#  Descripción: Gestiona el flujo de pedidos en orden de llegada.
#               Primero en entrar = primero en ser despachado.
#  PROHIBIDO: usar collections.deque o listas como cola.
# =============================================================

from data.models import Pedido


class NodoPedido:
    """Nodo de la cola. Contiene un Pedido y apunta al siguiente nodo."""

    def __init__(self, pedido: Pedido):
        self.pedido    = pedido
        self.siguiente = None   # Puntero al próximo nodo en la cola


class Cola:
    """
    Cola FIFO (First In, First Out) de pedidos.

    Estructura interna:
        frente → [Nodo1] → [Nodo2] → [Nodo3] → None
                                          ↑
                                        final

    Métodos:
        enqueue(pedido)     → Agrega al final          O(1)
        dequeue() → Pedido  → Extrae del frente        O(1)
        peek()    → Pedido  → Ve el frente sin extraer O(1)
        esta_vacia() → bool                            O(1)
        tamanio()    → int                             O(1)
        listar_todos() → list  → Para visualización GUI O(n)
    """

    def __init__(self):
        self._frente = None   # Primer nodo (próximo a despachar)
        self._final  = None   # Último nodo (último en llegar)
        self._tamanio = 0

    # ------------------------------------------------------------------
    # ENQUEUE — Insertar al final
    # ------------------------------------------------------------------

    def enqueue(self, pedido: Pedido):
        """Agrega un pedido al final de la cola."""
        nuevo_nodo = NodoPedido(pedido)
        if self._final is None:
            # Cola vacía: frente y final apuntan al mismo nodo
            self._frente = nuevo_nodo
            self._final  = nuevo_nodo
        else:
            self._final.siguiente = nuevo_nodo
            self._final           = nuevo_nodo
        self._tamanio += 1

    # ------------------------------------------------------------------
    # DEQUEUE — Extraer del frente
    # ------------------------------------------------------------------

    def dequeue(self) -> Pedido | None:
        """
        Extrae y retorna el pedido del frente de la cola.
        Retorna None si la cola está vacía.
        """
        if self._frente is None:
            return None

        pedido_extraido  = self._frente.pedido
        self._frente     = self._frente.siguiente

        # Si la cola quedó vacía, limpiar también el final
        if self._frente is None:
            self._final = None

        self._tamanio -= 1
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
