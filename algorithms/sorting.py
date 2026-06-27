# =============================================================
#  ElectroTech Store — Algoritmos de ordenación
#  Archivo: algorithms/sorting.py
#  Descripción: BubbleSort, QuickSort y MergeSort implementados
#               desde cero. Cada función retorna (lista_ordenada, tiempo_ms).
#  PROHIBIDO: usar .sort(), sorted() o cualquier método nativo.
# =============================================================

import time
from data.models import Producto


def _obtener_valor(producto: Producto, clave: str):
    """
    Extrae el valor de comparación del producto según la clave.
    Claves disponibles: 'precio', 'codigo', 'nombre', 'stock'
    """
    if clave == "precio":
        return producto.precio
    elif clave == "codigo":
        return producto.codigo
    elif clave == "nombre":
        return producto.nombre
    elif clave == "stock":
        return producto.stock
    return producto.precio  # default


# ==================================================================
# BUBBLE SORT  — O(n²) tiempo | O(1) espacio
# ==================================================================

def bubble_sort(lista: list, clave: str = "precio") -> tuple:
    """
    Ordena la lista de productos por la clave indicada usando BubbleSort.

    Algoritmo: compara pares adyacentes y los intercambia si están
    en el orden incorrecto. Repite hasta que no haya intercambios.

    Args:
        lista: lista de objetos Producto
        clave: campo de comparación ('precio', 'codigo', 'nombre', 'stock')

    Returns:
        (lista_ordenada, tiempo_ms): tupla con la lista ordenada
        y el tiempo de ejecución en milisegundos.
    """
    datos   = lista[:]          # Copia para no modificar el original
    n       = len(datos)
    inicio  = time.perf_counter()

    for i in range(n - 1):
        intercambio = False
        for j in range(n - 1 - i):
            if _obtener_valor(datos[j], clave) > _obtener_valor(datos[j + 1], clave):
                # Intercambio
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                intercambio = True
        # Optimización: si no hubo intercambios, ya está ordenado
        if not intercambio:
            break

    fin        = time.perf_counter()
    tiempo_ms  = (fin - inicio) * 1000
    return datos, round(tiempo_ms, 4)


# ==================================================================
# QUICK SORT  — O(n log n) promedio | O(n²) peor caso | O(log n) espacio
# ==================================================================

def quick_sort(lista: list, clave: str = "precio") -> tuple:
    """
    Ordena la lista de productos usando QuickSort recursivo.

    Algoritmo: elige un pivote (elemento central), separa en
    menores, iguales y mayores, y ordena recursivamente.

    Args:
        lista: lista de objetos Producto
        clave: campo de comparación

    Returns:
        (lista_ordenada, tiempo_ms)
    """
    datos  = lista[:]
    inicio = time.perf_counter()

    datos = _quick_sort_rec(datos, clave)

    fin       = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000
    return datos, round(tiempo_ms, 4)


def _quick_sort_rec(datos: list, clave: str) -> list:
    """Implementación recursiva interna de QuickSort."""
    if len(datos) <= 1:
        return datos

    # Pivote: elemento del centro
    pivote     = datos[len(datos) // 2]
    val_pivote = _obtener_valor(pivote, clave)

    menores  = [x for x in datos if _obtener_valor(x, clave) <  val_pivote]
    iguales  = [x for x in datos if _obtener_valor(x, clave) == val_pivote]
    mayores  = [x for x in datos if _obtener_valor(x, clave) >  val_pivote]

    return _quick_sort_rec(menores, clave) + iguales + _quick_sort_rec(mayores, clave)


# ==================================================================
# MERGE SORT  — O(n log n) siempre | O(n) espacio
# ==================================================================
# Ver si se necesita un merge_sort_inplace para ahorrar memoria, aunque es más complejo.
def merge_sort(lista: list, clave: str = "precio") -> tuple:
    """
    Ordena la lista de productos usando MergeSort.

    Algoritmo: divide la lista a la mitad recursivamente hasta
    tener sublistas de 1 elemento, luego fusiona ordenadamente.

    Args:
        lista: lista de objetos Producto
        clave: campo de comparación

    Returns:
        (lista_ordenada, tiempo_ms)
    """
    datos  = lista[:]
    inicio = time.perf_counter()

    datos = _merge_sort_rec(datos, clave)

    fin       = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000
    return datos, round(tiempo_ms, 4)


def _merge_sort_rec(datos: list, clave: str) -> list:
    """Implementación recursiva interna de MergeSort."""
    if len(datos) <= 1:
        return datos

    medio    = len(datos) // 2
    izquierda = _merge_sort_rec(datos[:medio], clave)
    derecha   = _merge_sort_rec(datos[medio:], clave)

    return _merge(izquierda, derecha, clave)


def _merge(izq: list, der: list, clave: str) -> list:
    """Fusiona dos listas ordenadas en una sola lista ordenada."""
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        if _obtener_valor(izq[i], clave) <= _obtener_valor(der[j], clave):
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    # Agregar los elementos restantes
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


# ==================================================================
# COMPARATIVA — ejecuta los 3 algoritmos y retorna resumen
# ==================================================================

def comparar_algoritmos(lista: list, clave: str = "precio") -> dict:
    """
    Ejecuta BubbleSort, QuickSort y MergeSort sobre la misma lista
    y retorna un diccionario con los tiempos de cada uno.

    Returns:
        {
          'bubble':  {'lista': [...], 'tiempo_ms': 123.45},
          'quick':   {'lista': [...], 'tiempo_ms':   0.87},
          'merge':   {'lista': [...], 'tiempo_ms':   1.12},
        }
    """
    lista_b, t_b = bubble_sort(lista, clave)
    lista_q, t_q = quick_sort(lista, clave)
    lista_m, t_m = merge_sort(lista, clave)

    return {
        "bubble": {"lista": lista_b, "tiempo_ms": t_b},
        "quick":  {"lista": lista_q, "tiempo_ms": t_q},
        "merge":  {"lista": lista_m, "tiempo_ms": t_m},
    }
