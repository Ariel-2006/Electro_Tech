#  ElectroTech Store — Panel Cola de Pedidos
import customtkinter as ctk
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
    Visualiza la cola FIFO en tiempo real.
    Permite agregar pedidos manuales, despachar (dequeue) y deshacer.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BG, corner_radius=0)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._construir_ui()
        self._refrescar_tabla()

    def _construir_ui(self):
        # Encabezado de la UI: título + info de la cola
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

        # Formulario nuevo pedido
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
        ctk.CTkButton(btn_frame, text="⚡ Despachar siguiente", width=150,
                      fg_color="#1e40af",
                      command=self._despachar).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="↩️ Deshacer", width=100,
                      fg_color="#7f1d1d",
                      command=self._deshacer).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="🔔 Cerrar turno", width=120,
                      fg_color="#0d9488",
                      command=self._cerrar_turno).pack(side="left", padx=4)

        self.lbl_estado = ctk.CTkLabel(form, text="", text_color=COLOR_ACCENT,
                                        font=ctk.CTkFont(size=11))
        self.lbl_estado.grid(row=1, column=0, columnspan=5, pady=(0, 8))

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

    # Acciones de los botones
    def _agregar_pedido(self):
        codigo   = self.entry_codigo.get().strip().upper()
        try:
            cantidad = int(self.entry_cantidad.get().strip())
        except ValueError:
            self._set_estado("⚠️  Cantidad debe ser un número entero.", COLOR_ERROR)
            return

        if not codigo:
            self._set_estado("⚠️  Ingresa el código del producto.", COLOR_WARN)
            return

        # Verificar que el producto existe en el BST
        producto = self.app.arbol.buscar(codigo)
        if not producto:
            self._set_estado(f"❌  Producto {codigo} no existe en el catálogo.", COLOR_ERROR)
            return

        if cantidad <= 0 or cantidad > producto.stock:
            self._set_estado(
                f"⚠️  Stock disponible: {producto.stock} unidades.", COLOR_WARN)
            return

        id_pedido = self.app.nuevo_id_pedido()
        pedido    = Pedido(id_pedido, codigo, producto.nombre, cantidad)
        self.app.cola.enqueue(pedido)
        # Llamada a la función de Telegram para notificar el pedido recibido
        enviar_pedido_recibido(id_pedido, producto.nombre, cantidad, self.app.cola.tamanio())

        self._set_estado(f"✅  Pedido {id_pedido} agregado a la cola.", COLOR_ACCENT)
        self.entry_codigo.delete(0, "end")
        self.entry_cantidad.delete(0, "end")
        self._refrescar_tabla()

    def _despachar(self):
        """Procesa el pedido del frente: dequeue + reduce stock + push historial."""
        pedido = self.app.cola.dequeue()
        if not pedido:
            self._set_estado("⚠️  La cola está vacía.", COLOR_WARN)
            return

        # Reducir stock en el BST
        producto = self.app.arbol.buscar(pedido.codigo_producto)
        if producto:
           producto.reducir_stock(pedido.cantidad)
        # La alerta se revisa después de reducir el stock, para reflejar el stock actual
        if producto.tiene_stock_critico():
            enviar_alerta_stock(producto.nombre, producto.codigo, producto.stock)
            # Mensaje en pantalla
            if producto.tiene_stock_critico():
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
                             f"Producto no encontrado en el catálogo", COLOR_INFO)

        # Registrar en la pila de historial
        registro = RegistroTransaccional(
            pedido.id_pedido, pedido.codigo_producto, pedido.cantidad)
        self.app.pila.push(registro)
        self._refrescar_tabla()

    def _cerrar_turno(self):
        """Envía a Telegram el resumen del turno (3er tipo de alerta)."""
        despachados = self.app.pila.tamanio()
        en_cola     = self.app.cola.tamanio()

        # Buscar el producto con stock mínimo para alertar
        producto_urgente = "Ninguno"
        stock_minimo = None
        # Bucle para encontrar el producto con stock mínimo en el BST
        # .inorden() devuelve una lista de productos en orden ascendente por código
        for p in self.app.arbol.inorden():
            if stock_minimo is None or p.stock < stock_minimo:
                stock_minimo = p.stock
                producto_urgente = f"{p.nombre} ({p.stock} uds.)"

        enviar_cierre_turno(despachados, en_cola, producto_urgente, 0.0)
        self._set_estado("🔔  Resumen de cierre de turno enviado a Telegram.", COLOR_INFO)

    def _deshacer(self):
        """Deshace el último despacho: pop historial + repone stock en BST."""
        registro = self.app.pila.pop()
        if not registro:
            self._set_estado("⚠️  No hay acciones en el historial para deshacer.", COLOR_WARN)
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

    # Tabla
    def _refrescar_tabla(self):
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        pedidos = self.app.cola.listar_todos()

        for idx, p in enumerate(pedidos):
            color_fila = "#111827" if idx % 2 == 0 else "#0f1117"
            fila = ctk.CTkFrame(self.scroll_tabla, fg_color=color_fila, corner_radius=4)
            fila.pack(fill="x", pady=1)

            pos_icon = "🥇" if idx == 0 else f"#{idx+1}"
            valores  = [pos_icon, p.id_pedido, p.nombre_producto,
                        str(p.cantidad), p.estado]
            anchos   = [80, 120, 200, 90, 120]

            for i, (val, w) in enumerate(zip(valores, anchos)):
                color = COLOR_ACCENT if idx == 0 and i == 0 else COLOR_TEXT
                ctk.CTkLabel(fila, text=val, width=w, text_color=color,
                             font=ctk.CTkFont(size=11)).grid(row=0, column=i, padx=4, pady=5)

        total = self.app.cola.tamanio()
        siguiente = self.app.cola.peek()
        sig_txt = siguiente.id_pedido if siguiente else "—"
        self.lbl_cola_info.configure(
            text=f"En cola: {total} pedidos | Próximo: {sig_txt}")
        self.app.actualizar_stats()