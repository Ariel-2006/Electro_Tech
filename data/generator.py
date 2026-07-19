# Generador de datos sintéticos para la tienda ElectroTech.
import random
from data.models import Producto, Pedido

# Diccionarios de códigos para tipos y marcas de productos para generar códigos alfanuméricos únicos.

# Los códigos se forman con 3 letras para el tipo, 3 letras para la marca y un número secuencial de 4 dígitos.

# El _ en algunos códigos de marca (como LG_) se usa para mantener el formato de 3 caracteres en caso de que 
# la marca tenga menos de 3 letras cuando se ingresa por teclado o se generen de igual forma.
TIPOS: dict[str, str] = {
    "Laptop":      "LAP",
    "Monitor":     "MON",
    "Celular":     "CEL",
    "Tablet":      "TAB",
    "Teclado":     "TEC",
    "Mouse":       "MOU",
    "Audífonos":   "AUD",
    "Impresora":   "IMP",
    "Cámara":      "CAM",
    "Smart TV":    "SMT",
    "Disco Duro":  "DIS",
    "Memoria USB": "MEM",
    "Router":      "ROU",
    "Parlante":    "PAR",
    "Cargador":    "CAR",
}

MARCAS: dict[str, str] = {
    "Samsung": "SAM",
    "LG":      "LG_",
    "Xiaomi":  "XIA",
    "HP":      "HP_",
    "Logitech":"LOG",
    "Apple":   "APP",
    "Asus":    "ASU",
    "Sony":    "SON",
    "Lenovo":  "LEN",
    "Huawei":  "HUA",
    "Dell":    "DEL",
    "Acer":    "ACE",
    "JBL":     "JBL",
    "Epson":   "EPS",
    "TP-Link": "TPL",
}

# Rangos de precio por tipo de producto
RANGOS_PRECIO: dict[str, tuple] = {
    "Laptop":      (399.99, 1999.99),
    "Monitor":     (149.99,  899.99),
    "Celular":     ( 99.99, 1299.99),
    "Tablet":      (149.99,  899.99),
    "Teclado":     ( 19.99,  199.99),
    "Mouse":       (  9.99,  149.99),
    "Audífonos":   ( 19.99,  399.99),
    "Impresora":   ( 79.99,  599.99),
    "Cámara":      (149.99, 1499.99),
    "Smart TV":    (299.99, 1799.99),
    "Disco Duro":  ( 49.99,  399.99),
    "Memoria USB": (  9.99,   79.99),
    "Router":      ( 29.99,  249.99),
    "Parlante":    ( 19.99,  349.99),
    "Cargador":    (  9.99,   79.99),
}

# Funciones de generación de datos sintéticos
def generar_codigo(tipo: str, marca: str, secuencial: int) -> str:
    """Construye una cadena alfanumérica única bajo un patrón preestablecido."""
    cod_tipo = TIPOS[tipo]  # Mapea las iniciales identificativas del tipo
    cod_marca = MARCAS[marca]  # Mapea las iniciales identificativas de la marca
    return f"{cod_tipo}-{cod_marca}-{secuencial:04d}"

# Contador global de códigos que garantiza que dos tandas nunca repitan un código.
_ultimo_secuencial = 0

# Función para reiniciar el contador global de códigos
def reiniciar_secuencial():
    """Restablece el valor inicial del contador numérico de los registros."""
    global _ultimo_secuencial
    _ultimo_secuencial = 0

# Generadores de colecciones de datos sintéticos
def generar_productos(n: int = 1000) -> list:
    """Crea una colección aleatoria de artículos para simular el inventario."""
    global _ultimo_secuencial
    lista_tipos = list(TIPOS.keys())  # Obtiene el catálogo de familias válidas
    lista_marcas = list(MARCAS.keys())  # Obtiene el catálogo de fabricantes válidos
    productos = []

    for _ in range(n):  # Ejecuta iteraciones hasta alcanzar el tamaño solicitado
        tipo = random.choice(lista_tipos)  # Selecciona un tipo de producto al azar
        marca = random.choice(lista_marcas)  # Selecciona un fabricante al azar

        # El secuencial NO se reinicia: continúa donde quedó la tanda anterior
        _ultimo_secuencial += 1  # Incrementa el identificador global numérico
        codigo = generar_codigo(tipo, marca, _ultimo_secuencial)

        nombre = f"{tipo} {marca}"

        precio_min, precio_max = RANGOS_PRECIO[
            tipo
        ]  # Recupera el umbral económico del tipo de artículo
        precio = round(
            random.uniform(precio_min, precio_max), 2
        )  # Asigna un precio comercial flotante con dos decimales
        stock = random.randint(
            0, 50
        )  # Define un volumen inicial disponible en bodega

        productos.append(Producto(codigo, nombre, precio, stock))

    return productos

# Generador de pedidos
def generar_pedidos(productos: list, n: int = 500) -> list:
    """Crea un lote transaccional asociando códigos reales de productos."""
    pedidos = []
    for i in range(
        1, n + 1
    ):  # Genera pedidos con identificadores secuenciales desde 1 hasta n
        producto = random.choice(
            productos
        )  # Toma un artículo aleatorio del almacén de datos
        id_pedido = (
            f"PED-{i:05d}"  # Define el identificador con ceros a la izquierda
        )
        cantidad = random.randint(
            1, 10
        )  # Determina el número de unidades adquiridas
        pedido = Pedido(id_pedido, producto.codigo, producto.nombre, cantidad)
        pedidos.append(pedido)
    return pedidos

# Función para generar todo el conjunto de datos de manera consecutiva
def generar_todo(n_productos: int = 1000, n_pedidos: int = 500) -> tuple:
    """Dispara de manera consecutiva el aprovisionamiento de datos del sistema."""
    productos = generar_productos(n_productos) # Genera la colección de productos
    pedidos = generar_pedidos(productos, n_pedidos) # Genera la colección de pedidos
    return productos, pedidos