# =============================================================
#  ElectroTech Store — Bot de Telegram (Módulo de Innovación)
#  Archivo: telegram/bot.py
#  Descripción: Notificaciones asíncronas automáticas:
#               1. Alerta de stock crítico (stock <= 5)
#               2. Cierre de turno diario con resumen
#  Requiere: python-telegram-bot>=20.0
#  Uso: Configurar TOKEN en variable de entorno TELEGRAM_TOKEN
#       y CHAT_ID con el ID del grupo o chat del admin.
# =============================================================

import os
import asyncio
from datetime import datetime

# Importación condicional para que el proyecto funcione sin el token configurado
try:
    from telegram import Bot
    from telegram.error import TelegramError
    TELEGRAM_DISPONIBLE = True
except ImportError:
    TELEGRAM_DISPONIBLE = False


# ------------------------------------------------------------------
# Configuración — cambiar estos valores o usar variables de entorno
# ------------------------------------------------------------------

TOKEN   = os.getenv("TELEGRAM_TOKEN", "TU_TOKEN_AQUI")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "TU_CHAT_ID_AQUI")


# ------------------------------------------------------------------
# Funciones de notificación
# ------------------------------------------------------------------

async def _enviar_mensaje(texto: str):
    """Envía un mensaje al chat configurado."""
    if not TELEGRAM_DISPONIBLE:
        print(f"[Telegram simulado] {texto}")
        return
    if TOKEN == "TU_TOKEN_AQUI":
        print(f"[Telegram sin token] {texto}")
        return
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="HTML")
    except Exception as e:
        print(f"[Telegram error] {e}")


def enviar_alerta_stock(nombre_producto: str, codigo: str, stock_actual: int):
    """
    Alerta automática cuando un producto cae a stock crítico (<= 5).

    Mensaje de ejemplo:
    ⚠️ STOCK CRÍTICO — ElectroTech Store
    Producto: Celular Xiaomi
    Código: CEL-XIA-0042
    Stock actual: 3 unidades
    Acción requerida: reabastecer urgente.
    """
    mensaje = (
        f"⚠️ <b>STOCK CRÍTICO — ElectroTech Store</b>\n"
        f"📦 Producto: <b>{nombre_producto}</b>\n"
        f"🔑 Código: <code>{codigo}</code>\n"
        f"📉 Stock actual: <b>{stock_actual} unidades</b>\n"
        f"🚨 <i>Acción requerida: reabastecer urgente.</i>\n"
        f"🕐 {datetime.now().strftime('%H:%M:%S — %d/%m/%Y')}"
    )
    asyncio.run(_enviar_mensaje(mensaje))


def enviar_cierre_turno(pedidos_despachados: int,
                         pedidos_en_cola: int,
                         producto_urgente: str,
                         ultimo_tiempo_ms: float,
                         algoritmo: str = "QuickSort"):
    """
    Resumen automático de cierre de turno.

    Mensaje de ejemplo:
    📊 CIERRE DE TURNO — ElectroTech Store
    ✅ Pedidos despachados hoy: 942
    ⏳ En cola esperando: 58
    🔴 Producto con más urgencia: Foco Recargable
    ⚡ Último test de rendimiento: 0.0021 ms (QuickSort)
    """
    mensaje = (
        f"📊 <b>CIERRE DE TURNO — ElectroTech Store</b>\n"
        f"✅ Pedidos despachados hoy: <b>{pedidos_despachados}</b>\n"
        f"⏳ En cola esperando: <b>{pedidos_en_cola}</b>\n"
        f"🔴 Producto con más urgencia: <b>{producto_urgente}</b>\n"
        f"⚡ Último test de rendimiento: <b>{ultimo_tiempo_ms} ms</b> ({algoritmo})\n"
        f"🕐 {datetime.now().strftime('%H:%M:%S — %d/%m/%Y')}"
    )
    asyncio.run(_enviar_mensaje(mensaje))


def enviar_pedido_recibido(id_pedido: str, nombre_producto: str,
                            cantidad: int, cola_total: int):
    """Notifica al admin cuando se recibe un nuevo pedido por Telegram."""
    mensaje = (
        f"🛒 <b>NUEVO PEDIDO — ElectroTech Store</b>\n"
        f"📋 ID: <code>{id_pedido}</code>\n"
        f"🖥️ Producto: <b>{nombre_producto}</b>\n"
        f"📦 Cantidad: <b>{cantidad}</b>\n"
        f"⏳ Posición en cola: <b>#{cola_total}</b>\n"
        f"🕐 {datetime.now().strftime('%H:%M:%S')}"
    )
    asyncio.run(_enviar_mensaje(mensaje))
