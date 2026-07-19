# Clases base que usan todos los módulos del proyecto. No se modifican, solo se instancian y se usan.
# Clase Producto: representa un producto en el catálogo de ElectroTech Store.
class Producto:
    """Clase base que define la estructura y control de existencias de un artículo."""

    STOCK_CRITICO = 5  # Umbral para alerta de Telegram

    def __init__(self, codigo: str, nombre: str, precio: float, stock: int):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = round(precio, 2)
        self.stock = stock

    def tiene_stock_critico(self) -> bool:
        # Función de comprobación de stock crítico
        """Verifica si las existencias se encuentran por debajo del límite."""
        return self.stock <= self.STOCK_CRITICO

    def reducir_stock(self, cantidad: int) -> bool:
        # Función de reducción de inventario
        """Disminuye las unidades disponibles al procesar una venta."""
        # Evalúa si la cantidad solicitada para el egreso es inválida o negativa
        if cantidad <= 0:
            return False
        # Evalúa si el inventario actual es insuficiente para cubrir la solicitud
        if self.stock < cantidad:
            return False
        self.stock -= cantidad  # Aplica la reducción de unidades en bodega central
        return True

    def reponer_stock(self, cantidad: int):
        # Función de reposición de inventario
        """Suma unidades de vuelta al almacén por transacciones revertidas."""
        # Controla si el incremento propuesto es superior a cero unidades
        if cantidad > 0:
            self.stock += cantidad  # Suma las unidades devueltas a la bodega central

# Clase Pedido: representa un pedido en la Cola de despacho.
class Pedido:
    """Clase base que modela una solicitud de compra dentro del sistema logístico."""

    ESTADOS = ("PENDIENTE", "EN_PROCESO", "COMPLETADO", "CANCELADO")

    def __init__(
        self,
        id_pedido: str,
        codigo_producto: str,
        nombre_producto: str,
        cantidad: int,
    ):
        self.id_pedido = id_pedido
        self.codigo_producto = codigo_producto
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad
        self.estado = "PENDIENTE"

    def cambiar_estado(self, nuevo_estado: str):
        # Función de actualización de estado
        """Modifica la fase actual del pedido dentro del flujo."""
        # Valida que la nueva etapa propuesta pertenezca a las fases permitidas
        if nuevo_estado in self.ESTADOS:
            self.estado = nuevo_estado

# Clase RegistroTransaccional: representa un registro mínimo para la Pila de historial.
# Función: almacenar solo lo necesario para deshacer un despacho, evitando duplicar objetos Producto completos en memoria.
class RegistroTransaccional:
    """Estructura optimizada para el almacenamiento cronológico del historial en la Pila."""

    def __init__(self, id_pedido: str, codigo_producto: str, cantidad: int):
        self.id_pedido = id_pedido
        self.codigo_producto = codigo_producto
        self.cantidad = cantidad