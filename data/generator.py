# =============================================================
#  ElectroTech Store — Generador de datos sintéticos
#  Archivo: data/generator.py
#  Descripción: Genera 1,000+ productos y pedidos aleatorios
#               usando solo el módulo random (sin faker).
#               Los IDs son secuenciales: LAP-SAM-0001, CEL-XIA-0002...
# =============================================================

import random
from data.models import Producto, Pedido

# ------------------------------------------------------------------
# Diccionarios de tipos y marcas con sus abreviaciones de 3 letras
# Regla: si tiene menos de 3 letras → rellenar con guion bajo (_)
# ------------------------------------------------------------------

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

# Rangos de precio por tipo de producto (realistas)
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


def generar_codigo(tipo: str, marca: str, secuencial: int) -> str:
    """
    Genera el código alfanumérico del producto.
    Formato: [3-TIPO]-[3-MARCA]-[0001]
    Ejemplo: LAP-SAM-0001, MON-LG_-0002, SMT-HP_-0015
    """
    cod_tipo  = TIPOS[tipo]
    cod_marca = MARCAS[marca]
    return f"{cod_tipo}-{cod_marca}-{secuencial:04d}"


def generar_productos(n: int = 1000) -> list:
    """
    Genera una lista de n objetos Producto con datos sintéticos.
    Los códigos son secuenciales (0001, 0002, ...).
    Los nombres combinan tipo + marca aleatoriamente.
    """
    lista_tipos  = list(TIPOS.keys())
    lista_marcas = list(MARCAS.keys())
    productos    = []

    for i in range(1, n + 1):
        tipo  = random.choice(lista_tipos)
        marca = random.choice(lista_marcas)

        codigo = generar_codigo(tipo, marca, i)
        nombre = f"{tipo} {marca}"

        precio_min, precio_max = RANGOS_PRECIO[tipo]
        precio = round(random.uniform(precio_min, precio_max), 2)
        stock  = random.randint(0, 200)

        productos.append(Producto(codigo, nombre, precio, stock))

    return productos


def generar_pedidos(productos: list, n: int = 500) -> list:
    """
    Genera n objetos Pedido sobre productos existentes.
    Requiere que se le pase la lista de productos ya generados.
    """
    pedidos = []
    for i in range(1, n + 1):
        producto  = random.choice(productos)
        id_pedido = f"PED-{i:05d}"
        cantidad  = random.randint(1, 10)
        pedido    = Pedido(id_pedido, producto.codigo, producto.nombre, cantidad)
        pedidos.append(pedido)
    return pedidos


def generar_todo(n_productos: int = 1000, n_pedidos: int = 500) -> tuple:
    """
    Punto de entrada principal del generador.
    Retorna: (lista_productos, lista_pedidos)

    Uso desde la GUI:
        productos, pedidos = generar_todo(1000, 500)
    """
    productos = generar_productos(n_productos)
    pedidos   = generar_pedidos(productos, n_pedidos)
    return productos, pedidos
