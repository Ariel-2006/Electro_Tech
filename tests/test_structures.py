# Aquí se encuentran las pruebas unitarias para las estructuras de datos y algoritmos implementados 
# en el proyecto ElectroTech Store.
# Funciona como un "runner" manual que ejecuta cada prueba y reporta los resultados.
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.models              import Producto, Pedido, RegistroTransaccional
from structures.bst_productos  import ArbolBST
from structures.queue_pedidos  import Cola
from structures.stack_historial import Pila
from algorithms.sorting        import bubble_sort, quick_sort, merge_sort
from algorithms.searching      import busqueda_binaria, busqueda_lineal


# Datos de prueba: lista de productos
def crear_productos_prueba():
    return [
        Producto("LAP-SAM-0001", "Laptop Samsung",   899.99, 10),
        Producto("CEL-XIA-0002", "Celular Xiaomi",   312.50, 87),
        Producto("MON-LG_-0003", "Monitor LG",       349.00,  3),   # stock crítico
        Producto("AUD-SON-0004", "Audífonos Sony",   145.00, 25),
        Producto("SMT-HP_-0005", "Smart TV HP",      654.00, 50),
    ]


# Test: Árbol Binario de Búsqueda (BST) para productos
def test_bst_insertar_y_buscar():
    arbol = ArbolBST()
    productos = crear_productos_prueba()
    for p in productos:
        arbol.insertar(p)

    assert arbol.total() == 5, f"Esperaba 5, obtuvo {arbol.total()}"

    p = arbol.buscar("CEL-XIA-0002")
    assert p is not None, "Producto CEL-XIA-0002 no encontrado"
    assert p.nombre == "Celular Xiaomi"
    print("✅ BST insertar y buscar: OK")


def test_bst_inorden_ordenado():
    arbol = ArbolBST()
    for p in crear_productos_prueba():
        arbol.insertar(p)

    lista = arbol.inorden()
    codigos = [p.codigo for p in lista]
    assert codigos == sorted(codigos), "El recorrido inorden no está ordenado"
    print("✅ BST inorden ordenado: OK")


def test_bst_eliminar():
    arbol = ArbolBST()
    for p in crear_productos_prueba():
        arbol.insertar(p)

    ok = arbol.eliminar("MON-LG_-0003")
    assert ok == True
    assert arbol.total() == 4
    assert arbol.buscar("MON-LG_-0003") is None
    print("✅ BST eliminar: OK")


def test_bst_eliminar_no_existente():
    arbol = ArbolBST()
    arbol.insertar(Producto("LAP-SAM-0001", "Laptop Samsung", 899.99, 10))
    ok = arbol.eliminar("XXX-XXX-9999")
    assert ok == False
    print("✅ BST eliminar no existente: OK")


# Test: Cola FIFO para pedidos
def test_cola_enqueue_dequeue():
    cola = Cola()
    p1 = Pedido("PED-00001", "LAP-SAM-0001", "Laptop Samsung", 2)
    p2 = Pedido("PED-00002", "CEL-XIA-0002", "Celular Xiaomi", 1)

    cola.enqueue(p1)
    cola.enqueue(p2)

    assert cola.tamanio() == 2
    extraido = cola.dequeue()
    assert extraido.id_pedido == "PED-00001", "FIFO: debe salir primero el primero"
    assert cola.tamanio() == 1
    print("✅ Cola FIFO enqueue/dequeue: OK")


def test_cola_peek():
    cola = Cola()
    assert cola.peek() is None

    cola.enqueue(Pedido("PED-00001", "LAP-SAM-0001", "Laptop Samsung", 1))
    frente = cola.peek()
    assert frente.id_pedido == "PED-00001"
    assert cola.tamanio() == 1  # peek no extrae
    print("✅ Cola peek: OK")


def test_cola_vacia():
    cola = Cola()
    assert cola.esta_vacia() == True
    cola.enqueue(Pedido("PED-00001", "LAP-SAM-0001", "Laptop Samsung", 1))
    assert cola.esta_vacia() == False
    cola.dequeue()
    assert cola.esta_vacia() == True
    print("✅ Cola vacía: OK")


# Test: Pila LIFO para historial de transacciones
def test_pila_push_pop():
    pila = Pila()
    r1   = RegistroTransaccional("PED-00001", "LAP-SAM-0001", 2)
    r2   = RegistroTransaccional("PED-00002", "CEL-XIA-0002", 1)

    pila.push(r1)
    pila.push(r2)

    assert pila.tamanio() == 2
    tope = pila.pop()
    assert tope.id_pedido == "PED-00002", "LIFO: debe salir el último en entrar"
    assert pila.tamanio() == 1
    print("✅ Pila LIFO push/pop: OK")


def test_pila_vacia():
    pila = Pila()
    assert pila.esta_vacia() == True
    assert pila.pop() is None
    print("✅ Pila vacía: OK")


# Test: Algoritmos de ordenamiento (Sorting)
def test_bubble_sort():
    productos = crear_productos_prueba()
    ordenados, ms = bubble_sort(productos, "precio")
    precios = [p.precio for p in ordenados]
    assert precios == sorted(precios), "BubbleSort no ordena correctamente"
    assert ms >= 0
    print(f"✅ BubbleSort: OK ({ms} ms)")


def test_quick_sort():
    productos = crear_productos_prueba()
    ordenados, ms = quick_sort(productos, "precio")
    precios = [p.precio for p in ordenados]
    assert precios == sorted(precios), "QuickSort no ordena correctamente"
    print(f"✅ QuickSort: OK ({ms} ms)")


def test_merge_sort():
    productos = crear_productos_prueba()
    ordenados, ms = merge_sort(productos, "precio")
    precios = [p.precio for p in ordenados]
    assert precios == sorted(precios), "MergeSort no ordena correctamente"
    print(f"✅ MergeSort: OK ({ms} ms)")


def test_sort_no_modifica_original():
    productos = crear_productos_prueba()
    original_codigos = [p.codigo for p in productos]
    _, _ = bubble_sort(productos, "precio")
    assert [p.codigo for p in productos] == original_codigos, \
        "El sort modificó la lista original (debe trabajar sobre copia)"
    print("✅ Sort no modifica original: OK")


# Test: Algoritmos de búsqueda (Searching)
def test_busqueda_binaria_encontrado():
    productos = crear_productos_prueba()
    # Ordenar por código primero (requisito de búsqueda binaria)
    lista_ord, _ = quick_sort(productos, "codigo")
    resultado, ms, comparaciones = busqueda_binaria(lista_ord, "MON-LG_-0003")
    assert resultado is not None
    assert resultado.nombre == "Monitor LG"
    print(f"✅ Búsqueda binaria encontrado: OK ({comparaciones} comparaciones, {ms} ms)")


def test_busqueda_binaria_no_encontrado():
    productos = crear_productos_prueba()
    lista_ord, _ = quick_sort(productos, "codigo")
    resultado, ms, comparaciones = busqueda_binaria(lista_ord, "XXX-XXX-9999")
    assert resultado is None
    print(f"✅ Búsqueda binaria no encontrado: OK ({comparaciones} comparaciones)")


def test_busqueda_lineal():
    productos = crear_productos_prueba()
    resultados, ms, comparaciones = busqueda_lineal(productos, "Samsung")
    assert len(resultados) == 1
    assert resultados[0].codigo == "LAP-SAM-0001"
    print(f"✅ Búsqueda lineal: OK ({comparaciones} comparaciones, {ms} ms)")


def test_stock_critico():
    p = Producto("MON-LG_-0003", "Monitor LG", 349.00, 3)
    assert p.tiene_stock_critico() == True
    p2 = Producto("LAP-SAM-0001", "Laptop Samsung", 899.99, 10)
    assert p2.tiene_stock_critico() == False
    print("✅ Stock crítico: OK")


# Permite ejecutar este archivo directamente para correr todas las pruebas
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  PRUEBAS UNITARIAS — ElectroTech Store")
    print("=" * 50)

    pruebas = [
        # BST
        test_bst_insertar_y_buscar,
        test_bst_inorden_ordenado,
        test_bst_eliminar,
        test_bst_eliminar_no_existente,
        # Cola
        test_cola_enqueue_dequeue,
        test_cola_peek,
        test_cola_vacia,
        # Pila
        test_pila_push_pop,
        test_pila_vacia,
        # Sort
        test_bubble_sort,
        test_quick_sort,
        test_merge_sort,
        test_sort_no_modifica_original,
        # Search
        test_busqueda_binaria_encontrado,
        test_busqueda_binaria_no_encontrado,
        test_busqueda_lineal,
        test_stock_critico,
    ]

    errores = 0
    for prueba in pruebas:
        try:
            prueba()
        except AssertionError as e:
            print(f"❌ {prueba.__name__}: FALLÓ — {e}")
            errores += 1
        except Exception as e:
            print(f"💥 {prueba.__name__}: ERROR — {e}")
            errores += 1

    print("\n" + "=" * 50)
    total = len(pruebas)
    ok    = total - errores
    print(f"  Resultado: {ok}/{total} pruebas pasaron")
    if errores == 0:
        print("  🎉 TODAS LAS PRUEBAS PASARON")
    else:
        print(f"  ⚠️  {errores} prueba(s) fallaron")
    print("=" * 50)