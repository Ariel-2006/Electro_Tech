# Búsquedas sobre listas de productos. Algoritmos de búsqueda lineal y binaria.
# Búsqueda lineal para encontrar todos los productos cuyo nombre contenga un término.
# Búsqueda binaria para encontrar un producto por código exacto en una lista ordenada.
import time


# Función de búsqueda binaria
def busqueda_binaria(lista_ordenada: list, codigo: str) -> tuple:
    """Busca un producto por código en una lista previamente ordenada."""
    inicio = time.perf_counter()  # Captura el tiempo de inicio de la búsqueda
    comparaciones = 0  # Inicializa el contador para métricas de rendimiento
    izquierda = 0  # Define el extremo inferior del espacio de búsqueda
    derecha = (
        len(lista_ordenada) - 1
    )  # Define el extremo superior del espacio de búsqueda
    resultado = None

    while izquierda <= derecha:  # Mantiene el bucle activo mientras el rango de búsqueda sea válido
        comparaciones += 1  # Registra cada evaluación del elemento central
        medio = (
            izquierda + derecha
        ) // 2  # La // sirve para que el resultado sea un entero
        codigo_medio = lista_ordenada[
            medio
        ].codigo  # Extrae el identificador del elemento central para comparar

        # Cuando el código buscado coincide exactamente con la posición central
        if codigo_medio == codigo:
            resultado = lista_ordenada[medio]
            break
        # Cuando el código buscado es alfabéticamente menor al central
        elif codigo < codigo_medio:
            derecha = (
                medio - 1
            )  # Reduce el espacio limitando el extremo superior
        # Cuando el código buscado es alfabéticamente mayor al central
        else:
            izquierda = (
                medio + 1
            )  # Reduce el espacio limitando el extremo inferior

    fin = time.perf_counter()  # Registra el tiempo exacto de finalización
    tiempo_ms = round(
        (fin - inicio) * 1000, 4
    )  # Calcula la duración total del proceso en milisegundos
    return resultado, tiempo_ms, comparaciones


# Función de búsqueda lineal
def busqueda_lineal(lista: list, termino: str) -> tuple:
    """Busca productos que contengan un texto parcial en su nombre."""
    inicio = time.perf_counter()  # Captura el tiempo inicial antes del recorrido
    comparaciones = 0  # Inicializa el contador para medir los accesos a la lista
    resultados = []  # Estructura para almacenar las coincidencias encontradas
    termino_lower = (
        termino.lower().strip()
    )  # Remueve espacios y convierte a minúsculas la búsqueda

    for producto in lista:  # Recorre la lista de inicio a fin de forma secuencial
        comparaciones += 1  # Incrementa por cada producto evaluado en la secuencia
        # Compara el término normalizado con el nombre del producto actual en minúsculas
        if termino_lower in producto.nombre.lower():
            resultados.append(producto)

    fin = time.perf_counter()  # Captura el instante final del ciclo completo
    tiempo_ms = round(
        (fin - inicio) * 1000, 4
    )  # Obtiene el tiempo final de procesamiento de la lista
    return resultados, tiempo_ms, comparaciones