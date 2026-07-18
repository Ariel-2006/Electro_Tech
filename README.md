# ⚡ ElectroTech Store

**Proyecto Investigación Formativa — Estructura de Datos | UNACH CDIA 2026-1S**

Equipo: Freddy Erazo · Zuly Correa · Ariel Jiménez · Wendy Moreta

## Descripción
Simulación de un sistema de gestión de tienda de tecnología que implementa estructuras de datos en Python con interfaz gráfica CustomTkinter.

## Estructuras implementadas
- **Cola FIFO** (`structures/queue_pedidos.py`) — Despacho de pedidos
- **Pila LIFO** (`structures/stack_historial.py`) — Historial de acciones
- **BST** (`structures/bst_productos.py`) — Catálogo de productos

## Algoritmos implementados
- **BubbleSort, QuickSort, MergeSort** con timer en ms (`algorithms/sorting.py`)
- **Búsqueda binaria y lineal** (`algorithms/searching.py`)

## Notificaciones de Telegram (Opcional)

El sistema incluye un módulo de alertas automáticas de stock crítico, cierres de turno y envíos vía Telegram. Las peticiones se ejecutan en hilos independientes (`threading`) para garantizar que la interfaz de usuario no se bloquee durante el envío

## Instalación
```bash
pip install customtkinter python-telegram-bot
python main.py
```

## Pruebas
```bash
python tests/test_structures.py
```
### *Como grupo, estamos contentos de haber realizado este proyecto, ya que nos permitió conocer una aproximación de lo que en verdad se lleva a cabo en realidad; estamos dispuestos a seguir mejorando y aprendiendo. Muchas gracias Ingeniera. 🙌😊*