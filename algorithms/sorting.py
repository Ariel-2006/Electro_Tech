# Módulo de algoritmos de ordenamiento para objetos Producto.
import time
from data.models import Producto

# Función de extracción de atributos
def _obtener_valor(producto: Producto, clave: str):
    """Retorna el atributo específico del producto para las comparaciones."""
    # Controla si se debe ordenar tomando como base el precio
    if clave == "precio":
        return producto.precio
    # Controla si la ordenación utilizará el identificador único
    elif clave == "codigo":
        return producto.codigo
    # Controla si el criterio de ordenamiento será el nombre
    elif clave == "nombre":
        return producto.nombre
    # Controla si se ordenará según las existencias en almacén
    elif clave == "stock":
        return producto.stock
    return producto.precio  # default

# BUBBLE SORT
# Funciona comparando pares adyacentes y moviendo el mayor al final en cada pasada.
# Función de ordenamiento burbuja
def bubble_sort(lista: list, clave: str = "precio") -> tuple:
    """Ordena productos mediante intercambios de elementos contiguos."""
    datos = lista[:]  # Copia para no modificar el original
    n = len(datos)  # Obtiene la cantidad total de elementos
    inicio = time.perf_counter()  # Toma el tiempo antes de iniciar las pasadas

    for i in range(n - 1):  # Controla el número de pasadas sobre la lista
        intercambio = False
        for j in range(
            n - 1 - i
        ):  # Recorre los elementos que aún no están en su lugar fijo
            # Compara si el elemento de la izquierda es mayor que el de la derecha
            if _obtener_valor(datos[j], clave) > _obtener_valor(
                datos[j + 1], clave
            ):
                datos[j], datos[j + 1] = (
                    datos[j + 1],
                    datos[j],
                )  # Intercambia las posiciones de ambos productos
                intercambio = True
        # Optimización: si no hubo intercambios, ya está ordenado
        if not intercambio:
            break

    fin = time.perf_counter()  # Toma el tiempo al finalizar el algoritmo
    tiempo_ms = (fin - inicio) * 1000
    return datos, round(tiempo_ms, 4)

# QUICK SORT
# Funciona eligiendo un pivote, separando en menores y mayores, y ordenando recursivamente.
# Función de ordenamiento rápido
def quick_sort(lista: list, clave: str = "precio") -> tuple:
    """Ordena productos usando división por pivote y recursividad."""
    datos = lista[:]  # Duplica la lista original para proteger sus datos
    inicio = time.perf_counter()  # Registra el tiempo previo a la segmentación

    datos = _quick_sort_rec(datos, clave)

    fin = time.perf_counter()  # Registra el tiempo posterior a la ordenación
    tiempo_ms = (fin - inicio) * 1000
    return datos, round(tiempo_ms, 4)

# Función de segmentación recursiva QuickSort
def _quick_sort_rec(datos: list, clave: str) -> list:
    """Filtra y divide la lista en tres sublistas de forma recursiva."""
    if len(datos) <= 1:
        return datos

    indice_medio = len(datos) // 2  # Calcula la posición del elemento central
    pivote = datos[indice_medio]  # Selecciona el producto del centro como guía
    valor_pivote = _obtener_valor(
        pivote, clave
    )  # Extrae la métrica del producto tomado como pivote

    # Separar en tres grupos recorriendo la lista una sola vez
    menores = []
    iguales = []
    mayores = []
    for producto in datos:  # Clasifica cada artículo de la lista bajo estudio
        valor_actual = _obtener_valor(
            producto, clave
        )  # Extrae la propiedad del producto en evaluación
        # Agrupa los productos que tienen un valor inferior al pivote
        if valor_actual < valor_pivote:
            menores.append(producto)
        # Agrupa los productos que tienen un valor superior al pivote
        elif valor_actual > valor_pivote:
            mayores.append(producto)
        # Agrupa los productos que tienen el mismo valor que el pivote
        else:
            iguales.append(producto)

    # Ordenar recursivamente los extremos y unir: menores + iguales + mayores
    izquierda_ordenada = _quick_sort_rec(menores, clave)
    derecha_ordenada = _quick_sort_rec(mayores, clave)
    return izquierda_ordenada + iguales + derecha_ordenada

# MERGE SORT
# Funciona dividiendo la lista en mitades, ordenando cada mitad y fusionando.
# Función de ordenamiento por mezcla
def merge_sort(lista: list, clave: str = "precio") -> tuple:
    """Ordena productos dividiendo en mitades y fusionándolas."""
    datos = lista[:]  # Crea una copia local de la estructura recibida
    inicio = time.perf_counter()  # Inicia el cronómetro para esta ordenación

    datos = _merge_sort_rec(datos, clave)

    fin = time.perf_counter()  # Detiene el cronómetro al terminar la fusión
    tiempo_ms = (fin - inicio) * 1000
    return datos, round(tiempo_ms, 4)


# Función de división recursiva MergeSort
def _merge_sort_rec(datos: list, clave: str) -> list:
    """Divide las listas consecutivamente a la mitad de forma recursiva."""
    if len(datos) <= 1:
        return datos

    medio = len(datos) // 2  # Localiza el punto medio exacto de los datos
    izquierda = _merge_sort_rec(
        datos[:medio], clave
    )  # Procesa recursivamente la primera mitad de la lista
    derecha = _merge_sort_rec(
        datos[medio:], clave
    )  # Procesa recursivamente la segunda mitad de la lista

    return _merge(izquierda, derecha, clave)


# Función de combinación ordenada
def _merge(izq: list, der: list, clave: str) -> list:
    """Fusiona dos listas ordenadas en una sola lista ordenada."""
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):  # Compara elementos mientras ambas listas tengan contenido
        # Verifica si el artículo izquierdo debe ir antes que el derecho
        if _obtener_valor(izq[i], clave) <= _obtener_valor(der[j], clave):
            resultado.append(izq[i])
            i += 1
        # Se ejecuta si el artículo derecho es menor que el izquierdo
        else:
            resultado.append(der[j])
            j += 1

    # Agregar los elementos restantes
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

# Comparativa de algoritmos
# Función de comparación de rendimiento
def comparar_algoritmos(lista: list, clave: str = "precio") -> dict:
    """Ejecuta los tres métodos de ordenamiento y recopila sus tiempos."""
    lista_b, t_b = bubble_sort(lista, clave)
    lista_q, t_q = quick_sort(lista, clave)
    lista_m, t_m = merge_sort(lista, clave)

    return {
        "bubble": {"lista": lista_b, "tiempo_ms": t_b},
        "quick": {"lista": lista_q, "tiempo_ms": t_q},
        "merge": {"lista": lista_m, "tiempo_ms": t_m},
    }
