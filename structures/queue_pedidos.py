#  Cola de pedidos implementada como una estructura FIFO (First In, First Out)
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
        # Función de encolado de pedidos
        """Inserta un nuevo elemento al final de la estructura FIFO."""
        nuevo_nodo = NodoPedido(pedido)  # Instancia el nuevo contenedor para el nodo
        # Si la estructura se encuentra completamente vacía
        if self._final is None:
            self._frente = nuevo_nodo  # Asigna el primer nodo como frente inicial
            self._final = nuevo_nodo  # Define el mismo nodo como extremo final
        # Caso contrario si ya existen elementos previos
        else:
            self._final.siguiente = nuevo_nodo  # Enlaza el nodo actual tras el último
            self._final = nuevo_nodo  # Desplaza el puntero final al nuevo extremo
        self._tamanio += 1  # Incrementa el contador global de elementos

    def dequeue(self) -> Pedido | None:
        # Función de desencolado de pedidos
        """Remueve y retorna el primer elemento de la estructura FIFO."""
        # Si no hay ningún elemento disponible en el frente
        if self._frente is None:
            return None # Retorna None para indicar que la estructura está vacía
        pedido_extraido = self._frente.pedido # Almacena el pedido que será removido 
        self._frente = self._frente.siguiente  # Avanza el frente al elemento posterior
        # Si la estructura quedó vacía tras el movimiento
        if self._frente is None:
            self._final = None  # Anula la referencia del extremo final
        self._tamanio -= 1  # Decrementa el contador global de elementos
        return pedido_extraido

    def peek(self) -> Pedido | None:
        # Función de inspección del frente
        """Devuelve el elemento del frente sin removerlo de la estructura."""
        # Si la estructura no contiene ningún elemento
        if self._frente is None:
            return None # Retorna None para indicar que la estructura está vacía
        return self._frente.pedido

    def esta_vacia(self) -> bool:
        # Función de verificación de vaciado
        """Indica si la estructura carece de elementos en espera."""
        return self._frente is None

    def tamanio(self) -> int:
        # Función de consulta de longitud
        """Retorna la cantidad total de elementos almacenados."""
        return self._tamanio

    def listar_todos(self) -> list:
        # Función de volcado de datos
        """Genera una lista con todos los elementos de la cola."""
        resultado = []  # Inicializa el contenedor dinámico vacío
        nodo_actual = self._frente  # Comienza la lectura desde el inicio
        # Mientras queden nodos por recorrer en el camino
        while nodo_actual is not None:
            resultado.append(nodo_actual.pedido)  # Agrega el elemento analizado
            nodo_actual = nodo_actual.siguiente  # Avanza hacia el nodo posterior
        return resultado

    def limpiar(self):
        # Función de vaciado total
        """Restablece los punteros de la estructura para vaciarla."""
        self._frente = None  # Elimina el enlace al primer nodo
        self._final = None  # Elimina el enlace al último nodo
        self._tamanio = 0

    def __str__(self):
        # Función de conversión a texto
        """Representa visualmente el estado actual de la cola."""
        return f"Cola({self._tamanio} pedidos en espera)"