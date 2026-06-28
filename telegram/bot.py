# =============================================================
#  ElectroTech Store — Bot de Telegram (Módulo de Innovación)
#  Archivo: telegram/bot.py
#  Implementación: Nativa con urllib (Cero librerías externas / Sin asyncio)
# =============================================================

from datetime import datetime
import os
import urllib.parse
import urllib.request


def cargar_credenciales():
  if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
      for linea in f:
        if "=" in linea and not linea.startswith("#"):
          llave, valor = linea.strip().split("=", 1)
          os.environ[llave] = valor

  # Variables de entorno con claves de respaldo quemadas
  token = os.getenv("TELEGRAM_TOKEN", "7914828466:AAGAfLgxRpqlrdVZRcVegPH5R1XQjDobiho")
  chat_id = os.getenv("TELEGRAM_CHAT_ID", "-5351269085")
  return token, chat_id


TOKEN, CHAT_ID = cargar_credenciales()


def _enviar_mensaje_http(texto: str):
  """Disparador interno síncrono vía HTTP GET nativo."""
  if not TOKEN or TOKEN.startswith("TU_TOKEN"):
    print(f"[Telegram Simulado] {texto}")
    return

  try:
    texto_codificado = urllib.parse.quote(texto)
    url = (
        f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={texto_codificado}&parse_mode=HTML"
    )

    # Solicitud HTTP nativa con tiempo de espera máximo de 3 segundos
    with urllib.request.urlopen(url, timeout=3.0) as response:
      pass
  except Exception as e:
    print(f"[Error de Red Telegram] No se pudo enviar la notificación: {e}")


# ------------------------------------------------------------------
# Funciones Públicas de Notificación
# ------------------------------------------------------------------


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