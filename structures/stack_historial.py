# Registra transacciones de despacho para poder deshacerlas. Guarda solo RegistroTransaccional
# [ID_Pedido, ID_Producto, Cantidad] para evitar duplicar objetos Producto completos en memoria.

from data.models import RegistroTransaccional

class NodoPila:
    """Nodo de la pila. Contiene un RegistroTransaccional y apunta al nodo inferior."""

    def __init__(self, registro: RegistroTransaccional):
        self.registro = registro
        self.inferior = None  # Nodo debajo en la pila

class Pila:
    """
    Estructura de datos tipo pila (LIFO) para almacenar registros transaccionales.
    Permite apilar, desapilar, inspeccionar la cima, verificar si está vacía, obtener el tamaño, listar todos los registros y limpiar la pila.
    Cada nodo de la pila contiene un objeto RegistroTransaccional y un puntero al nodo inferior.
    Esta estructura es útil para implementar funcionalidades de deshacer en sistemas de despacho.
    """

    def __init__(self):
        self._cima = None
        self._tamanio = 0

    # Función para apilar un nuevo registro transaccional en la cima de la pila.
    def push(self, registro: RegistroTransaccional):
        # Función de apilamiento en historial
        """Apila un nuevo registro transaccional en la cima."""
        nuevo_nodo = NodoPila(registro)  # Instancia el nuevo contenedor de transacciones
        nuevo_nodo.inferior = self._cima  # Enlaza la antigua cima abajo de la nueva
        self._cima = nuevo_nodo  # Desplaza la cima hacia el nodo entrante
        self._tamanio += 1  # Incrementa la cantidad de elementos registrados

    # Función para desapilar el registro de la cima de la pila y devolverlo.
    def pop(self) -> RegistroTransaccional | None:
        # Función de desapilamiento de registros
        """
        Extrae y retorna el registro de la cima.
        Retorna None si la pila está vacía.
        Usar este valor para reintegrar el stock al BST.
        """
        # Si la cima no contiene ningún nodo válido
        if self._cima is None:
            return None

        registro_extraido = self._cima.registro
        self._cima = self._cima.inferior  # Baja el puntero al elemento inferior
        self._tamanio -= 1  # Decrementa la cantidad de elementos registrados
        return registro_extraido

    # Función para ver el registro de la cima sin extraerlo.
    def peek(self) -> RegistroTransaccional | None:
        # Función de lectura de la cima
        """
        Retorna el registro de la cima sin extraerlo.
        Retorna None si la pila está vacía.
        """
        # Si no existen transacciones guardadas en la memoria
        if self._cima is None:
            return None
        return self._cima.registro

    # Funciones: esta_vacia, tamanio, listar_todo, limpiar
    def esta_vacia(self) -> bool:
        # Función de diagnóstico de vaciado
        """Determina si el almacenamiento carece de registros transaccionales."""
        return self._cima is None

    def tamanio(self) -> int:
        # Función de conteo de historial
        """Devuelve el número total de movimientos apilados."""
        return self._tamanio

    def listar_todo(self) -> list:
        # Función de exportación de registros
        """
        Recorre la pila de cima a base y retorna lista de registros.
        El índice 0 es el más reciente (cima).
        Usado por la GUI para mostrar historial de despachos.
        """
        resultado = []  # Crea el contenedor dinámico para la salida
        nodo_actual = self._cima  # Inicia el recorrido en el extremo superior
        # Mientras queden operaciones almacenadas en los niveles inferiores
        while nodo_actual is not None:
            resultado.append(nodo_actual.registro)  # Integra la información al listado externo
            nodo_actual = nodo_actual.inferior  # Desciende un nivel en la estructura jerárquica
        return resultado

    def limpiar(self):
        # Función de reinicio de almacenamiento
        """Vacía completamente la pila."""
        self._cima = None  # Corta la referencia al nodo superior
        self._tamanio = 0