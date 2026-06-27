# =============================================================
#  ElectroTech Store — Panel Catálogo de Productos (BST)
#  Archivo: gui/panel_productos.py
# =============================================================

import customtkinter as ctk
from data.models import Producto

COLOR_ACCENT  = "#00c896"
COLOR_BG      = "#0f1117"
COLOR_CARD    = "#1a1f2e"
COLOR_TEXT    = "#e2e8f0"
COLOR_SUBTEXT = "#94a3b8"
COLOR_ERROR   = "#f87171"
COLOR_WARN    = "#fbbf24"


class PanelProductos(ctk.CTkFrame):
    """
    Panel del catálogo de productos.
    Muestra el árbol BST como tabla dinámica (recorrido inorden).
    Permite insertar, buscar y eliminar productos individualmente.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BG, corner_radius=0)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._construir_ui()
        self._refrescar_tabla()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _construir_ui(self):
        # ── Encabezado ──
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header, text="🖥️  Catálogo de Productos",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLOR_ACCENT).grid(row=0, column=0, padx=16, pady=12, sticky="w")

        self.lbl_info_arbol = ctk.CTkLabel(
            header, text="BST: 0 productos | Altura: 0",
            text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=11))
        self.lbl_info_arbol.grid(row=0, column=1, padx=16, sticky="e")

        # ── Formulario ──
        form = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        form.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

        campos = [("Código", "entry_codigo"), ("Nombre", "entry_nombre"),
                  ("Precio $", "entry_precio"), ("Stock", "entry_stock")]

        for i, (label, attr) in enumerate(campos):
            ctk.CTkLabel(form, text=label, text_color=COLOR_SUBTEXT,
                         font=ctk.CTkFont(size=11)).grid(row=0, column=i*2, padx=(16,4), pady=10)
            entry = ctk.CTkEntry(form, width=140, placeholder_text=label)
            entry.grid(row=0, column=i*2+1, padx=(0,12), pady=10)
            setattr(self, attr, entry)

        # Botones
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=0, column=8, padx=10)

        ctk.CTkButton(btn_frame, text="➕ Insertar", width=100,
                      fg_color=COLOR_ACCENT, text_color="#000",
                      command=self._insertar).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="🔍 Buscar", width=90,
                      fg_color="#1e40af",
                      command=self._buscar).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="🗑️ Eliminar", width=90,
                      fg_color="#7f1d1d",
                      command=self._eliminar).pack(side="left", padx=4)
        ctk.CTkButton(btn_frame, text="🔄 Limpiar", width=80,
                      fg_color="#374151",
                      command=self._limpiar_form).pack(side="left", padx=4)

        # Mensaje de estado
        self.lbl_estado = ctk.CTkLabel(form, text="", text_color=COLOR_ACCENT,
                                        font=ctk.CTkFont(size=11))
        self.lbl_estado.grid(row=1, column=0, columnspan=9, pady=(0,8))

        # ── Tabla ──
        tabla_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        tabla_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5,20))
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Encabezados tabla
        cols = [("Código", 160), ("Nombre", 240), ("Precio $", 110),
                ("Stock", 80), ("Estado stock", 120)]
        hdr = ctk.CTkFrame(tabla_frame, fg_color="#111827", corner_radius=8)
        hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8,0))
        for i, (col, w) in enumerate(cols):
            ctk.CTkLabel(hdr, text=col, width=w,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=COLOR_ACCENT).grid(row=0, column=i, padx=4, pady=6)

        # Scroll
        self.scroll_tabla = ctk.CTkScrollableFrame(
            tabla_frame, fg_color="transparent", corner_radius=0)
        self.scroll_tabla.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0,8))
        tabla_frame.grid_rowconfigure(1, weight=1)

    # ------------------------------------------------------------------
    # ACCIONES
    # ------------------------------------------------------------------

    def _insertar(self):
        codigo = self.entry_codigo.get().strip().upper()
        nombre = self.entry_nombre.get().strip()
        try:
            precio = float(self.entry_precio.get().strip())
            stock  = int(self.entry_stock.get().strip())
        except ValueError:
            self._set_estado("⚠️  Precio y Stock deben ser numéricos.", COLOR_ERROR)
            return

        if not codigo or not nombre:
            self._set_estado("⚠️  Código y Nombre son obligatorios.", COLOR_ERROR)
            return

        producto = Producto(codigo, nombre, precio, stock)
        self.app.arbol.insertar(producto)
        self._set_estado(f"✅  Producto {codigo} insertado en el BST.", COLOR_ACCENT)
        self._limpiar_form()
        self._refrescar_tabla()

    def _buscar(self):
        codigo = self.entry_codigo.get().strip().upper()
        if not codigo:
            self._set_estado("⚠️  Ingresa un código para buscar.", COLOR_WARN)
            return
        p = self.app.arbol.buscar(codigo)
        if p:
            self.entry_nombre.delete(0, "end"); self.entry_nombre.insert(0, p.nombre)
            self.entry_precio.delete(0, "end"); self.entry_precio.insert(0, str(p.precio))
            self.entry_stock.delete(0, "end");  self.entry_stock.insert(0, str(p.stock))
            self._set_estado(f"🔍  Producto {codigo} encontrado en el BST.", COLOR_ACCENT)
        else:
            self._set_estado(f"❌  Código {codigo} no encontrado en el BST.", COLOR_ERROR)

    def _eliminar(self):
        codigo = self.entry_codigo.get().strip().upper()
        if not codigo:
            self._set_estado("⚠️  Ingresa el código del producto a eliminar.", COLOR_WARN)
            return
        ok = self.app.arbol.eliminar(codigo)
        if ok:
            self._set_estado(f"🗑️  Producto {codigo} eliminado del BST.", COLOR_ACCENT)
            self._limpiar_form()
            self._refrescar_tabla()
        else:
            self._set_estado(f"❌  Código {codigo} no existe en el BST.", COLOR_ERROR)

    def _limpiar_form(self):
        for attr in ("entry_codigo", "entry_nombre", "entry_precio", "entry_stock"):
            getattr(self, attr).delete(0, "end")

    def _set_estado(self, msg: str, color: str = COLOR_ACCENT):
        self.lbl_estado.configure(text=msg, text_color=color)

    # ------------------------------------------------------------------
    # TABLA DINÁMICA
    # ------------------------------------------------------------------
    # Verificar si es aquí donde ocurre la lentidud al mostrar muchos productos,
    # Talvez, se podría mostrar de acuerdo a los filtros de búsqueda, o paginar la tabla para no mostrar todos a la vez.
    def _refrescar_tabla(self):
        """Limpia y redibuja la tabla con el recorrido inorden del BST."""
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        productos = self.app.arbol.inorden()  # Lista ordenada por código

        for idx, p in enumerate(productos):
            color_fila = "#111827" if idx % 2 == 0 else "#0f1117"
            fila = ctk.CTkFrame(self.scroll_tabla, fg_color=color_fila, corner_radius=4)
            fila.pack(fill="x", pady=1)

            estado_stock = "🔴 CRÍTICO" if p.tiene_stock_critico() else "🟢 OK"
            color_stock  = COLOR_ERROR if p.tiene_stock_critico() else COLOR_ACCENT

            valores = [p.codigo, p.nombre, f"${p.precio:.2f}", str(p.stock), estado_stock]
            anchos  = [160, 240, 110, 80, 120]
            colores = [COLOR_TEXT, COLOR_TEXT, COLOR_TEXT, COLOR_TEXT, color_stock]

            for i, (val, w, col) in enumerate(zip(valores, anchos, colores)):
                ctk.CTkLabel(fila, text=val, width=w, text_color=col,
                             font=ctk.CTkFont(size=11)).grid(row=0, column=i, padx=4, pady=5)

        # Actualizar info del árbol
        self.lbl_info_arbol.configure(
            text=f"BST: {self.app.arbol.total()} productos | "
                 f"Altura: {self.app.arbol.altura()} niveles")
        self.app.actualizar_stats()
