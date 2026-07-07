#Clases base que usan TODOS los módulos del proyecto. No se modifican, solo se instancian y se usan.

# Clase Producto: representa un producto en el catálogo de ElectroTech Store.
class Producto:
    """
    Representa un producto en el catálogo de ElectroTech Store.

    Atributos:
        codigo  (str): Clave única. Formato: LAP-SAM-0001
        nombre  (str): Nombre compuesto. Ejemplo: "Laptop Samsung"
        precio  (float): Precio en dólares. Ej: 899.99
        stock   (int): Unidades disponibles en bodega.
    """

    STOCK_CRITICO = 5  # Umbral para alerta de Telegram

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = round(precio, 2)
        self.stock  = stock

    def tiene_stock_critico(self) -> bool:
        """Retorna True si el stock está en nivel crítico."""
        return self.stock <= self.STOCK_CRITICO

    def reducir_stock(self, cantidad: int) -> bool:
        """
        Reduce el stock en la cantidad indicada.
        Retorna True si la operación fue exitosa, False si no hay suficiente stock.
        """
        if cantidad <= 0:
            return False
        if self.stock < cantidad:
            return False
        self.stock -= cantidad
        return True

    def reponer_stock(self, cantidad: int):
        """Reintegra stock (usado por la Pila al deshacer un despacho)."""
        if cantidad > 0:
            self.stock += cantidad

    def __str__(self):
        return (f"[{self.codigo}] {self.nombre:<25} "
                f"${self.precio:>8.2f}  Stock: {self.stock:>4}")

    def __repr__(self):
        return f"Producto(codigo='{self.codigo}', nombre='{self.nombre}', precio={self.precio}, stock={self.stock})"

# Clase Pedido: representa un pedido en la Cola de despacho.
class Pedido:
    """
    Representa un pedido en la Cola de despacho.

    Atributos:
        id_pedido       (str): Identificador único del pedido. Ej: "PED-00042"
        codigo_producto (str): Código del producto solicitado. Ej: "LAP-SAM-0001"
        nombre_producto (str): Nombre del producto (copia para trazabilidad).
        cantidad        (int): Unidades solicitadas.
        estado          (str): PENDIENTE | EN_PROCESO | COMPLETADO | CANCELADO
    """

    ESTADOS = ("PENDIENTE", "EN_PROCESO", "COMPLETADO", "CANCELADO")

    def __init__(self, id_pedido: str, codigo_producto: str,
                 nombre_producto: str, cantidad: int):
        self.id_pedido        = id_pedido
        self.codigo_producto  = codigo_producto
        self.nombre_producto  = nombre_producto
        self.cantidad         = cantidad
        self.estado           = "PENDIENTE"

    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado del pedido si el nuevo estado es válido."""
        if nuevo_estado in self.ESTADOS:
            self.estado = nuevo_estado

    def __str__(self):
        return (f"Pedido {self.id_pedido} | {self.nombre_producto:<25} "
                f"x{self.cantidad:>3} | {self.estado}")

    def __repr__(self):
        return (f"Pedido(id='{self.id_pedido}', producto='{self.codigo_producto}', "
                f"cantidad={self.cantidad}, estado='{self.estado}')")

# Clase RegistroTransaccional: representa un registro mínimo para la Pila de historial.
# Función: almacenar solo lo necesario para deshacer un despacho, evitando duplicar objetos Producto completos en memoria.
class RegistroTransaccional:
    """
    Registro mínimo que guarda la Pila de historial.
    Solo almacena lo necesario para deshacer un despacho:
    el código del producto y la cantidad despachada.
    Esto evita duplicar objetos Producto completos en memoria.
    """

    def __init__(self, id_pedido: str, codigo_producto: str, cantidad: int):
        self.id_pedido       = id_pedido
        self.codigo_producto = codigo_producto
        self.cantidad        = cantidad

    def __str__(self):
        return (f"TX[{self.id_pedido}] → {self.codigo_producto} "
                f"x{self.cantidad} (deshacer reintegra stock)")

    def __repr__(self):
        return (f"RegistroTransaccional(id='{self.id_pedido}', "
                f"codigo='{self.codigo_producto}', cantidad={self.cantidad})")