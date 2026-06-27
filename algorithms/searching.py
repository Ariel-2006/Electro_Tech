# =============================================================
#  ElectroTech Store — Algoritmos de búsqueda
#  Archivo: algorithms/searching.py
#  Descripción: Búsqueda binaria (sobre lista ordenada) y
#               búsqueda lineal (por nombre parcial).
# =============================================================

import time
from data.models import Producto


def busqueda_binaria(lista_ordenada: list, codigo: str) -> tuple:
    """
    Busca un producto por código exacto en una lista YA ORDENADA por código.
    Usa división binaria del espacio de búsqueda.

    Complejidad: O(log n)
    Requisito: la lista debe estar ordenada por campo 'codigo'.

    Args:
        lista_ordenada: lista de Producto ordenada por código
        codigo: código exacto a buscar. Ej: "LAP-SAM-0001"

    Returns:
        (producto_o_None, tiempo_ms, comparaciones)
    """
    inicio       = time.perf_counter()
    comparaciones = 0
    izquierda    = 0
    derecha      = len(lista_ordenada) - 1
    resultado    = None

    while izquierda <= derecha:
        comparaciones += 1
        medio = (izquierda + derecha) // 2 # La // sirve para que el resultado sea un entero
        codigo_medio = lista_ordenada[medio].codigo

        if codigo_medio == codigo:
            resultado = lista_ordenada[medio]
            break
        elif codigo < codigo_medio:
            derecha = medio - 1
        else:
            izquierda = medio + 1

    fin       = time.perf_counter()
    tiempo_ms = round((fin - inicio) * 1000, 4)
    return resultado, tiempo_ms, comparaciones


def busqueda_lineal(lista: list, termino: str) -> tuple:
    """
    Busca productos cuyo nombre contenga el término indicado.
    No requiere lista ordenada. Devuelve TODOS los coincidentes.

    Complejidad: O(n)

    Args:
        lista: lista de Producto (cualquier orden)
        termino: texto parcial a buscar en el nombre. Ej: "Samsung"

    Returns:
        (lista_resultados, tiempo_ms, comparaciones)
    """
    inicio        = time.perf_counter()
    comparaciones = 0
    resultados    = []
    termino_lower = termino.lower().strip()

    for producto in lista:
        comparaciones += 1
        if termino_lower in producto.nombre.lower():
            resultados.append(producto)

    fin       = time.perf_counter()
    tiempo_ms = round((fin - inicio) * 1000, 4)
    return resultados, tiempo_ms, comparaciones


def busqueda_por_rango_precio(lista: list,
                               precio_min: float,
                               precio_max: float) -> tuple:
    """
    Retorna todos los productos cuyo precio esté en el rango [min, max].
    Búsqueda lineal sobre cualquier lista.

    Complejidad: O(n)

    Returns:
        (lista_resultados, tiempo_ms, comparaciones)
    """
    inicio        = time.perf_counter()
    comparaciones = 0
    resultados    = []

    for producto in lista:
        comparaciones += 1
        if precio_min <= producto.precio <= precio_max:
            resultados.append(producto)

    fin       = time.perf_counter()
    tiempo_ms = round((fin - inicio) * 1000, 4)
    return resultados, tiempo_ms, comparaciones