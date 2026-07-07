# Módulo de notificaciones vía Telegram para ElectroTech Store
from datetime import datetime
import os
import urllib.parse
import urllib.request
import threading

# Función para cargar credenciales desde variables de entorno o archivo .env
def cargar_credenciales():
    # Intentar cargar desde el archivo .env (que NO se sube a GitHub)
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for linea in f:
                if "=" in linea and not linea.startswith("#"):
                    llave, valor = linea.strip().split("=", 1)
                    os.environ[llave] = valor
    
    # Obtener variables. Si no existen, devuelven None
    token = os.getenv("TELEGRAM_TOKEN") 
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    return token, chat_id

TOKEN, CHAT_ID = cargar_credenciales()

# Función interna para enviar mensajes a Telegram usando la API HTTP
def _enviar_mensaje_http(texto: str):
    """Envía el mensaje en un hilo aparte para NO congelar la interfaz."""
    if TOKEN is None or CHAT_ID is None:
        print("[Info] Notificaciones de Telegram desactivadas (sin token).")
        return

    def _tarea():
        try:
            texto_codificado = urllib.parse.quote(texto)
            url = (f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                   f"?chat_id={CHAT_ID}&text={texto_codificado}&parse_mode=HTML")
            with urllib.request.urlopen(url, timeout=3.0):
                pass
        except Exception as e:
            print(f"Error Telegram: {e}")

    threading.Thread(target=_tarea, daemon=True).start()


# Función para enviar alerta de stock crítico
def enviar_alerta_stock(nombre_producto: str, codigo: str, stock_actual: int):
  mensaje = (
      f"⚠️ <b>STOCK CRÍTICO — ElectroTech Store</b>\n"
      f"📦 Producto: <b>{nombre_producto}</b>\n"
      f"🔑 Código: <code>{codigo}</code>\n"
      f"📉 Stock actual: <b>{stock_actual} unidades</b>\n"
      f"🚨 <i>Acción requerida: reabastecer urgente.</i>\n"
      f"🕐 {datetime.now().strftime('%H:%M:%S — %d/%m/%Y')}"
  )
  _enviar_mensaje_http(mensaje)

# Función para enviar resumen de cierre de turno
def enviar_cierre_turno(
    pedidos_despachados: int,
    pedidos_en_cola: int,
    producto_urgente: str,
    ultimo_tiempo_ms: float,
    algoritmo: str = "QuickSort",
):
  mensaje = (
      f"📊 <b>CIERRE DE TURNO — ElectroTech Store</b>\n"
      f"✅ Pedidos despachados hoy: <b>{pedidos_despachados}</b>\n"

      f"⏳ En cola esperando: <b>{pedidos_en_cola}</b>\n"
      f"🔴 Producto con más urgencia: <b>{producto_urgente}</b>\n"
      f"⚡ Último test de rendimiento: <b>{ultimo_tiempo_ms} ms</b>"
      f" ({algoritmo})\n"
      f"🕐 {datetime.now().strftime('%H:%M:%S — %d/%m/%Y')}"
  )
  _enviar_mensaje_http(mensaje)

# Función para enviar notificación de nuevo pedido recibido
def enviar_pedido_recibido(
    id_pedido: str, nombre_producto: str, cantidad: int, cola_total: int
):
  mensaje = (
      f"🛒 <b>NUEVO PEDIDO — ElectroTech Store</b>\n"
      f"📋 ID: <code>{id_pedido}</code>\n"
      f"🖥️ Producto: <b>{nombre_producto}</b>\n"
      f"📦 Cantidad: <b>{cantidad}</b>\n"
      f"⏳ Posición en cola: <b>#{cola_total}</b>\n"
      f"🕐 {datetime.now().strftime('%H:%M:%S')}"
  )
  _enviar_mensaje_http(mensaje)