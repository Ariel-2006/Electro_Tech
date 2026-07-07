# Panel de pedidos: cola FIFO, paginación, agregar, despachar, deshacer, cierre turno.
import customtkinter as ctk
from tkinter import messagebox
from data.models import Pedido, RegistroTransaccional
from telegram.bot import (
    enviar_pedido_recibido,
    enviar_alerta_stock,
    enviar_cierre_turno,
)

COLOR_ACCENT  = "#00c896"
COLOR_BG      = "#0f1117"
COLOR_CARD    = "#1a1f2e"
COLOR_TEXT    = "#e2e8f0"
COLOR_SUBTEXT = "#94a3b8"
COLOR_ERROR   = "#f87171"
COLOR_WARN    = "#fbbf24"
COLOR_INFO    = "#60a5fa"


class PanelPedidos(ctk.CTkFrame):
    """
    Panel de la cola de despacho de pedidos.
    Visualiza la cola FIFO en tiempo real con paginación.
    Permite agregar pedidos manuales, despachar (dequeue) y deshacer.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BG, corner_radius=0)
        self.app = app
        self.pagina = 0
        self.items_por_pag = 20
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._construir_ui()
        self._refrescar_tabla()

    def _construir_ui(self):
        # ── Encabezado ──
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header, text="📦  Cola de Despacho (FIFO)",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLOR_ACCENT).grid(row=0, column=0, padx=16, pady=12, sticky="w")

        self.lbl_cola_info = ctk.CTkLabel(
            header, text="Cola vacía", text_color=COLOR_SUBTEXT,
            font=ctk.CTkFont(size=11))
        self.lbl_cola_info.grid(row=0, column=1, padx=16, sticky="e")

        # ── Formulario nuevo pedido ──
        form = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        form.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

        ctk.CTkLabel(form, text="Código producto:", text_color=COLOR_SUBTEXT,
                     font=ctk.CTkFont(size=11)).grid(row=0, column=0, padx=16, pady=10)
        self.entry_codigo = ctk.CTkEntry(form, width=160, placeholder_text="LAP-SAM-0001")
        self.entry_codigo.grid(row=0, column=1, padx=8)

        ctk.CTkLabel(form, text="Cantidad:", text_color=COLOR_SUBTEXT,
                     font=ctk.CTkFont(size=11)).grid(row=0, column=2, padx=8)
        self.entry_cantidad = ctk.CTkEntry(form, width=80, placeholder_text="1")
        self.entry_cantidad.grid(row=0, column=3, padx=8)

        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=0, column=4, padx=16)

        ctk.CTkButton(btn_frame, text="➕ Agregar pedido", width=130,
                      fg_color=COLOR_ACCENT, text_color="#000",
                      command=self._agregar_pedido).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="⚡ Despachar", width=120,
                      fg_color="#1e40af",
                      command=self._despachar).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="↩️ Deshacer", width=100,
                      fg_color="#7f1d1d",
                      command=self._deshacer).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="🔔 Cerrar turno", width=120,
                      fg_color="#0d9488",
                      command=self._cerrar_turno).pack(side="left", padx=4)

        # Mensaje informativo bajo los botones
        ctk.CTkLabel(form,
                     text="ℹ️  Solo 'Agregar pedido' requiere código y cantidad. "
                          "Los demás botones operan sin llenar campos.",
                     text_color=COLOR_SUBTEXT,
                     font=ctk.CTkFont(size=10)).grid(
            row=1, column=0, columnspan=5, pady=(0, 2))

        self.lbl_estado = ctk.CTkLabel(form, text="", text_color=COLOR_ACCENT,
                                        font=ctk.CTkFont(size=11))
        self.lbl_estado.grid(row=2, column=0, columnspan=5, pady=(0, 8))

        # ── Tabla cola ──
        tabla_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        tabla_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 20))
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(1, weight=1)

        cols = [("Posición", 80), ("ID Pedido", 120), ("Producto", 200),
                ("Cantidad", 90), ("Estado", 120)]
        hdr = ctk.CTkFrame(tabla_frame, fg_color="#111827", corner_radius=8)
        hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 0))
        for i, (col, w) in enumerate(cols):
            ctk.CTkLabel(hdr, text=col, width=w,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=COLOR_ACCENT).grid(row=0, column=i, padx=4, pady=6)

        self.scroll_tabla = ctk.CTkScrollableFrame(
            tabla_frame, fg_color="transparent", corner_radius=0)
        self.scroll_tabla.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        tabla_frame.grid_rowconfigure(1, weight=1)

        # ── Barra de paginación ──
        barra_pag = ctk.CTkFrame(tabla_frame, fg_color="transparent")
        barra_pag.grid(row=2, column=0, sticky="ew", padx=8, pady=(0, 8))

        ctk.CTkButton(barra_pag, text="◀ Anterior", width=110,
                      fg_color="#374151", hover_color="#4b5563",
                      command=lambda: self._cambiar_pagina(-1)).pack(side="left", padx=4)

        self.lbl_paginacion = ctk.CTkLabel(
            barra_pag, text="Página 1 de 1",
            text_color=COLOR_ACCENT, font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_paginacion.pack(side="left", expand=True)

        ctk.CTkButton(barra_pag, text="Siguiente ▶", width=110,
                      fg_color="#374151", hover_color="#4b5563",
                      command=lambda: self._cambiar_pagina(1)).pack(side="right", padx=4)

    # ------------------------------------------------------------------
    # ACCIONES
    # ------------------------------------------------------------------

    def _agregar_pedido(self):
        codigo = self.entry_codigo.get().strip().upper()
        cant_txt = self.entry_cantidad.get().strip()

        if not codigo or not cant_txt:
            self.bell()
            messagebox.showwarning("Campos incompletos",
                "Para agregar un pedido debes llenar:\n"
                "• Código producto (ej: LAP-SAM-0001)\n"
                "• Cantidad (número entero)")
            return

        try:
            cantidad = int(cant_txt)
        except ValueError:
            self.bell()
            messagebox.showerror("Cantidad inválida",
                "La cantidad debe ser un número entero.\n"
                "Ejemplo: 1, 5, 10")
            return

        # Verificar que el producto existe en el BST
        producto = self.app.arbol.buscar(codigo)
        if not producto:
            self.bell()
            messagebox.showerror("Producto no encontrado",
                f"El código {codigo} no existe en el catálogo.\n"
                "Verifica el código o inserta el producto primero en el panel Catálogo.")
            return

        if cantidad <= 0:
            self.bell()
            messagebox.showwarning("Cantidad inválida",
                "La cantidad debe ser mayor a 0.")
            return

        if cantidad > producto.stock:
            self.bell()
            messagebox.showwarning("Stock insuficiente",
                f"Stock disponible de {producto.nombre}: {producto.stock} unidades.\n"
                f"No puedes pedir {cantidad}.")
            return

        id_pedido = self.app.nuevo_id_pedido()
        pedido    = Pedido(id_pedido, codigo, producto.nombre, cantidad)
        self.app.cola.enqueue(pedido)
        # Notificación SOLO en alta manual (la carga masiva NO notifica)
        enviar_pedido_recibido(id_pedido, producto.nombre, cantidad, self.app.cola.tamanio())

        self._set_estado(f"✅  Pedido {id_pedido} agregado a la cola.", COLOR_ACCENT)
        self.entry_codigo.delete(0, "end")
        self.entry_cantidad.delete(0, "end")
        self._refrescar_tabla()

    def _despachar(self):
        """Procesa el pedido del frente: dequeue + reduce stock + push historial."""
        pedido = self.app.cola.dequeue()
        if not pedido:
            self.bell()
            messagebox.showinfo("Cola vacía",
                "No hay pedidos en la cola para despachar.\n"
                "Agrega pedidos primero o genera datos masivos.")
            return

        # Reducir stock en el BST
        producto = self.app.arbol.buscar(pedido.codigo_producto)
        if producto:
            producto.reducir_stock(pedido.cantidad)
            # La alerta se revisa DESPUÉS de reducir
            if producto.tiene_stock_critico():
                enviar_alerta_stock(producto.nombre, producto.codigo, producto.stock)
            # Mensaje en pantalla
            if producto.tiene_stock_critico():
                self.bell()
                messagebox.showwarning("⚠️ Stock Crítico",
                    f"El producto {producto.nombre} quedó con "
                    f"solo {producto.stock} unidades.\n"
                    "Se envió alerta a Telegram.")
                self._set_estado(
                    f"🔴  Despachado {pedido.id_pedido} | "
                    f"⚠️ Stock crítico: {producto.nombre} → {producto.stock} uds.",
                    COLOR_WARN)
            else:
                self._set_estado(
                    f"✅  Despachado {pedido.id_pedido} — "
                    f"{producto.nombre} x{pedido.cantidad}",
                    COLOR_ACCENT)
        else:
            self._set_estado(f"✅  Despachado {pedido.id_pedido} "
                             f"(producto no encontrado en BST)", COLOR_INFO)

        # Registrar en la pila de historial
        registro = RegistroTransaccional(
            pedido.id_pedido, pedido.codigo_producto, pedido.cantidad)
        self.app.pila.push(registro)
        self._refrescar_tabla()

    def _cerrar_turno(self):
        """Envía a Telegram el resumen del turno (3er tipo de alerta)."""
        if self.app.arbol.esta_vacio():
            self.bell()
            messagebox.showinfo("Sin datos",
                "No hay productos en el catálogo.\n"
                "Genera datos primero para poder cerrar un turno.")
            return

        despachados = self.app.pila.tamanio()
        en_cola     = self.app.cola.tamanio()

        producto_urgente = "Ninguno"
        stock_minimo = None
        for p in self.app.arbol.inorden():
            if stock_minimo is None or p.stock < stock_minimo:
                stock_minimo = p.stock
                producto_urgente = f"{p.nombre} ({p.stock} uds.)"

        enviar_cierre_turno(despachados, en_cola, producto_urgente, 0.0)
        messagebox.showinfo("Cierre de turno",
            f"Resumen enviado a Telegram:\n"
            f"• Despachados: {despachados}\n"
            f"• En cola: {en_cola}\n"
            f"• Más urgente: {producto_urgente}")
        self._set_estado("🔔  Resumen de cierre de turno enviado a Telegram.", COLOR_INFO)

    def _deshacer(self):
        """Deshace el último despacho: pop historial + repone stock en BST."""
        registro = self.app.pila.pop()
        if not registro:
            self.bell()
            messagebox.showinfo("Sin historial",
                "No hay acciones en el historial para deshacer.\n"
                "Primero despacha algún pedido.")
            return

        # Reponer stock en el BST
        producto = self.app.arbol.buscar(registro.codigo_producto)
        if producto:
            producto.reponer_stock(registro.cantidad)
            self._set_estado(
                f"↩️  Deshecho {registro.id_pedido} — "
                f"Stock repuesto: {producto.nombre} +{registro.cantidad}",
                COLOR_INFO)
        else:
            self._set_estado(
                f"↩️  Deshecho {registro.id_pedido} "
                f"(producto no encontrado en BST)", COLOR_WARN)

        # Re-encolar el pedido
        pedido = Pedido(registro.id_pedido, registro.codigo_producto,
                        producto.nombre if producto else registro.codigo_producto,
                        registro.cantidad)
        self.app.cola.enqueue(pedido)
        self._refrescar_tabla()

    def _set_estado(self, msg: str, color: str = COLOR_ACCENT):
        self.lbl_estado.configure(text=msg, text_color=color)

    # ------------------------------------------------------------------
    # PAGINACIÓN
    # ------------------------------------------------------------------

    def _total_paginas(self) -> int:
        total = self.app.cola.tamanio()
        if total == 0:
            return 1
        return (total - 1) // self.items_por_pag + 1

    def _cambiar_pagina(self, delta: int):
        nueva_pagina = self.pagina + delta
        if 0 <= nueva_pagina < self._total_paginas():
            self.pagina = nueva_pagina
            self._refrescar_tabla()

    # ------------------------------------------------------------------
    # TABLA
    # ------------------------------------------------------------------

    def _refrescar_tabla(self):
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        pedidos = self.app.cola.listar_todos()
        total_items = len(pedidos)

        # Ajustar página si quedó fuera de rango
        if self.pagina >= self._total_paginas():
            self.pagina = self._total_paginas() - 1

        inicio = self.pagina * self.items_por_pag
        fin = inicio + self.items_por_pag
        pedidos_pagina = pedidos[inicio:fin]

        # Etiqueta de paginación
        if total_items == 0:
            self.lbl_paginacion.configure(text="Sin pedidos")
        else:
            self.lbl_paginacion.configure(
                text=f"Página {self.pagina + 1} de {self._total_paginas()}"
                     f"   ·   mostrando {inicio + 1}–{min(fin, total_items)} de {total_items}")

        for idx, p in enumerate(pedidos_pagina):
            pos_real = inicio + idx   # posición real en toda la cola
            color_fila = "#111827" if idx % 2 == 0 else "#0f1117"
            fila = ctk.CTkFrame(self.scroll_tabla, fg_color=color_fila, corner_radius=4)
            fila.pack(fill="x", pady=1)

            pos_icon = "🥇" if pos_real == 0 else f"#{pos_real + 1}"
            valores  = [pos_icon, p.id_pedido, p.nombre_producto,
                        str(p.cantidad), p.estado]
            anchos   = [80, 120, 200, 90, 120]

            for i, (val, w) in enumerate(zip(valores, anchos)):
                color = COLOR_ACCENT if pos_real == 0 and i == 0 else COLOR_TEXT
                ctk.CTkLabel(fila, text=val, width=w, text_color=color,
                             font=ctk.CTkFont(size=11)).grid(row=0, column=i, padx=4, pady=5)

        total = self.app.cola.tamanio()
        siguiente = self.app.cola.peek()
        sig_txt = siguiente.id_pedido if siguiente else "—"
        self.lbl_cola_info.configure(
            text=f"En cola: {total} pedidos | Próximo: {sig_txt}")
        self.app.actualizar_stats()