# Almacena el catálogo de productos ordenado lexicográficamente por código alfanumérico.
# Ejemplo de orden: AUD-ACE-0001 < LAP-SAM-0001
from data.models import Producto


class NodoBST:
    """Nodo interno del árbol. Contiene un Producto, y punteros izq, der."""

    def __init__(self, producto: Producto):
        self.producto = producto
        self.izquierdo = None  # Nodo con código menor
        self.derecho = None  # Nodo con código mayor


class ArbolBST:
    """
    Árbol binario de búsqueda BST para almacenar productos.
    Permite inserción, búsqueda, eliminación y recorridos inorden.
    """
    def __init__(self):
        self._raiz = None
        self._total = 0

    # Función de inserción: agrega un producto al árbol, manteniendo el orden por código.
    def insertar(self, producto: Producto):
        # Función de inserción en catálogo
        """Inserta un producto en el árbol. Si el código ya existe, actualiza."""
        self._raiz = self._insertar_rec(self._raiz, producto)

    def _insertar_rec(self, nodo: NodoBST, producto: Producto) -> NodoBST:
        # Función recursiva de inserción
        """Determina la posición adecuada e inyecta el nodo de forma ordenada."""
        # Si el subárbol actual se encuentra vacío
        if nodo is None:
            self._total += 1  # Incrementa la cuenta global de artículos
            return NodoBST(producto)
        # Si el código entrante es menor al del nodo actual
        if producto.codigo < nodo.producto.codigo:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, producto)  # Desplaza la inserción a la rama izquierda
        # Si el código entrante es mayor al del nodo actual
        elif producto.codigo > nodo.producto.codigo:
            nodo.derecho = self._insertar_rec(nodo.derecho, producto)  # Desplaza la inserción a la rama derecha
        # Caso contrario si el código ya se encuentra registrado
        else:
            # Código duplicado → actualizar datos del producto
            nodo.producto = producto
        return nodo

    # Función de búsqueda: retorna el producto con el código dado, o None si no existe.
    def buscar(self, codigo: str) -> Producto | None:
        # Función de búsqueda de productos
        """Busca un producto por su código alfanumérico."""
        nodo = self._buscar_rec(self._raiz, codigo)
        return nodo.producto if nodo else None

    def _buscar_rec(self, nodo: NodoBST, codigo: str) -> NodoBST | None:
        # Función recursiva de búsqueda
        """Rastrea el árbol de manera descendente comparando los códigos."""
        # Si el camino recorrido finaliza sin hallar coincidencias
        if nodo is None:
            return None
        # Si el código coincide exactamente con el nodo actual
        if codigo == nodo.producto.codigo:
            return nodo
        # Si el código buscado es menor al del nodo actual
        if codigo < nodo.producto.codigo:
            return self._buscar_rec(nodo.izquierdo, codigo)  # Continúa el rastreo en la rama izquierda
        return self._buscar_rec(nodo.derecho, codigo)  # Continúa el rastreo en la rama derecha

    # Función de eliminación: elimina un producto por su código, si existe.
    def eliminar(self, codigo: str) -> bool:
        # Función de remoción de registros
        """Elimina el nodo con ese código de forma controlada."""
        self._raiz, eliminado = self._eliminar_rec(self._raiz, codigo)
        # Si la operación de remoción fue exitosa
        if eliminado:
            self._total -= 1  # Decrementa la cuenta global de artículos
        return eliminado

    def _eliminar_rec(self, nodo: NodoBST, codigo: str) -> tuple:
        # Función recursiva de remoción
        """Ubica y reestructura los enlaces para remover el código."""
        # Si el código a remover no existe en este subárbol
        if nodo is None:
            return None, False

        eliminado = False

        # Si el código es menor al del nodo evaluado
        if codigo < nodo.producto.codigo:
            nodo.izquierdo, eliminado = self._eliminar_rec(nodo.izquierdo, codigo)  # Desplaza la remoción a la izquierda

        # Si el código es mayor al del nodo evaluado
        elif codigo > nodo.producto.codigo:
            nodo.derecho, eliminado = self._eliminar_rec(nodo.derecho, codigo)  # Desplaza la remoción a la derecha

        # Caso contrario si se localiza el nodo específico
        else:
            # Nodo encontrado — 3 casos:
            eliminado = True

            # Caso 1: hoja (sin hijos)
            if nodo.izquierdo is None and nodo.derecho is None:
                return None, True

            # Caso 2: un solo hijo
            if nodo.izquierdo is None:
                return nodo.derecho, True
            if nodo.derecho is None:
                return nodo.izquierdo, True

            # Caso 3: dos hijos reemplazar con el sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._minimo(nodo.derecho)  # Localiza el elemento más pequeño a la derecha
            nodo.producto = sucesor.producto
            nodo.derecho, _ = self._eliminar_rec(nodo.derecho, sucesor.producto.codigo)  # Elimina el nodo duplicado

        return nodo, eliminado

    def _minimo(self, nodo: NodoBST) -> NodoBST:
        # Función de localización mínima
        """Busca el extremo izquierdo inferior de un subárbol."""
        # Mientras sigan existiendo subdivisiones a la izquierda
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo  # Avanza de forma secuencial por la rama izquierda
        return nodo

    # Funciones de recorrido: inorden, preorden, postorden. Retornan listas de productos.
    def inorden(self) -> list:
        # Función de recorrido inorden
        """Genera una recopilación ordenada secuencialmente por código."""
        resultado = []  # Inicializa el contenedor dinámico para almacenar
        self._inorden_rec(self._raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo: NodoBST, resultado: list):
        # Función recursiva inorden
        """Transfiere los datos al listado usando izquierda-raíz-derecha."""
        # Si el extremo del camino actual es nulo
        if nodo is None:
            return
        self._inorden_rec(nodo.izquierdo, resultado)  # Ejecuta la lectura de la rama izquierda
        resultado.append(nodo.producto)
        self._inorden_rec(nodo.derecho, resultado)  # Ejecuta la lectura de la rama derecha

    # Funciones: altura, total, esta_vacio
    def altura(self) -> int:
        # Función de cálculo de altura
        """Mide la cantidad máxima de niveles que posee la estructura."""
        return self._altura_rec(self._raiz)

    def _altura_rec(self, nodo: NodoBST) -> int:
        # Función recursiva de altura
        """Compara la profundidad de las ramas de forma ascendente."""
        # Si se alcanza el límite inferior de la estructura
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierdo), self._altura_rec(nodo.derecho))  # Elige el camino de mayor profundidad

    def total(self) -> int:
        # Función de consulta de volumen
        """Retorna el número total de productos en el árbol."""
        return self._total

    def limpiar(self):
        # Función de reinicio de catálogo
        """Vacía el árbol por completo """
        self._raiz = None  # Anula la referencia del nodo raíz
        self._total = 0

    def esta_vacio(self) -> bool:
        # Función de verificación de catálogo
        """Evalúa si la raíz carece de nodos vinculados."""
        return self._raiz is None

    def __str__(self):
        # Función de formato legible
        """Muestra de forma compacta el estado del catálogo."""
        return f"ArbolBST({self._total} productos, altura={self.altura()})"