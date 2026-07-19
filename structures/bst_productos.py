# Almacena el catálogo de productos ordenado lexicográficamente por código alfanumérico.
# Ejemplo de orden: AUD-ACE-0001 < LAP-SAM-0001
from data.models import Producto


class NodoBST:
    """Nodo interno del árbol. Contiene un Producto y punteros izq/der."""

    def __init__(self, producto: Producto):
        self.producto  = producto
        self.izquierdo = None   # Nodo con código menor
        self.derecho   = None   # Nodo con código mayor


class ArbolBST:
    """
    Árbol Binario de Búsqueda para el catálogo de ElectroTech Store.

    Regla de orden (por código alfanumérico):
        nodo.izquierdo.codigo < nodo.codigo < nodo.derecho.codigo

    Métodos públicos:
        insertar(producto)          → O(log n) promedio
        buscar(codigo) → Producto   → O(log n) promedio
        eliminar(codigo)            → O(log n) promedio
        inorden()  → list           → O(n) — lista ordenada por código
        preorden() → list           → O(n)
        postorden()→ list           → O(n)
        altura()   → int            → O(n)
        total()    → int            → cantidad de nodos
    """

    def __init__(self):
        self._raiz  = None
        self._total = 0

    # Función de inserción: agrega un producto al árbol, manteniendo el orden por código.
    def insertar(self, producto: Producto):
        """Inserta un producto en el árbol. Si el código ya existe, actualiza."""
        self._raiz = self._insertar_rec(self._raiz, producto)

    def _insertar_rec(self, nodo: NodoBST, producto: Producto) -> NodoBST:
        if nodo is None:
            self._total += 1
            return NodoBST(producto)
        if producto.codigo < nodo.producto.codigo:
            nodo.izquierdo = self._insertar_rec(nodo.izquierdo, producto)
        elif producto.codigo > nodo.producto.codigo:
            nodo.derecho = self._insertar_rec(nodo.derecho, producto)
        else:
            # Código duplicado → actualizar datos del producto
            nodo.producto = producto
        return nodo

    # Función de búsqueda: retorna el producto con el código dado, o None si no existe.
    def buscar(self, codigo: str) -> Producto | None:
        """
        Busca un producto por su código alfanumérico.
        Retorna el objeto Producto si existe, None si no.
        """
        nodo = self._buscar_rec(self._raiz, codigo)
        return nodo.producto if nodo else None

    def _buscar_rec(self, nodo: NodoBST, codigo: str) -> NodoBST | None:
        if nodo is None:
            return None
        if codigo == nodo.producto.codigo:
            return nodo
        if codigo < nodo.producto.codigo:
            return self._buscar_rec(nodo.izquierdo, codigo)
        return self._buscar_rec(nodo.derecho, codigo)

    # Función de eliminación: elimina un producto por su código, si existe.
    def eliminar(self, codigo: str) -> bool:
        """
        Elimina el nodo con ese código.
        Retorna True si lo eliminó, False si no existía.
        Maneja los 3 casos clásicos de eliminación en BST.
        """
        self._raiz, eliminado = self._eliminar_rec(self._raiz, codigo)
        if eliminado:
            self._total -= 1
        return eliminado

    def _eliminar_rec(self, nodo: NodoBST, codigo: str) -> tuple:
        """Retorna (nodo_actualizado, fue_eliminado)."""
        if nodo is None:
            return None, False

        eliminado = False

        if codigo < nodo.producto.codigo:
            nodo.izquierdo, eliminado = self._eliminar_rec(nodo.izquierdo, codigo)

        elif codigo > nodo.producto.codigo:
            nodo.derecho, eliminado = self._eliminar_rec(nodo.derecho, codigo)

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

            # Caso 3: dos hijos → reemplazar con el sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._minimo(nodo.derecho)
            nodo.producto = sucesor.producto
            nodo.derecho, _ = self._eliminar_rec(nodo.derecho, sucesor.producto.codigo)

        return nodo, eliminado

    def _minimo(self, nodo: NodoBST) -> NodoBST:
        """Retorna el nodo con el código más pequeño en el subárbol."""
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo

    # Funciones de recorrido: inorden, preorden, postorden. Retornan listas de productos.
    def inorden(self) -> list:
        """Recorrido izquierda → raíz → derecha. Retorna lista ordenada por código."""
        resultado = []
        self._inorden_rec(self._raiz, resultado)
        return resultado

    def _inorden_rec(self, nodo: NodoBST, resultado: list):
        if nodo is None:
            return
        self._inorden_rec(nodo.izquierdo, resultado)
        resultado.append(nodo.producto)
        self._inorden_rec(nodo.derecho, resultado)

    # Funciones: altura, total, esta_vacio
    def altura(self) -> int:
        """Retorna la altura del árbol (número de niveles)."""
        return self._altura_rec(self._raiz)

    def _altura_rec(self, nodo: NodoBST) -> int:
        if nodo is None:
            return 0
        return 1 + max(self._altura_rec(nodo.izquierdo),
                       self._altura_rec(nodo.derecho))

    def total(self) -> int:
        """Retorna el número total de productos en el árbol."""
        return self._total

    def limpiar(self):
        """Vacía el árbol por completo """
        self._raiz  = None
        self._total = 0

    def esta_vacio(self) -> bool:
        return self._raiz is None

    def __str__(self):
        return f"ArbolBST({self._total} productos, altura={self.altura()})"