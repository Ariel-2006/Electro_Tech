# Panel de catálogo de productos (BST) - GUI
import customtkinter as ctk
from tkinter import messagebox
from data.models import Producto

COLOR_ACCENT  = "#00c896"
COLOR_BG      = "#0f1117"
COLOR_CARD    = "#1a1f2e"
COLOR_TEXT    = "#e2e8f0"
COLOR_SUBTEXT = "#94a3b8"
COLOR_ERROR   = "#f87171"
COLOR_WARN    = "#fbbf24"

# Clase PanelProductos
class PanelProductos(ctk.CTkFrame):
    """
    Panel del catálogo de productos.
    Muestra el árbol BST como tabla dinámica (recorrido inorden).
    Permite insertar, buscar y eliminar productos individualmente.
    """
    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BG)
        self.app = app
        self.pagina = 0
        self.items_por_pag = 20
        self.grid_columnconfigure(0, weight=1)
        self._construir_ui()
        self._refrescar_tabla()

    # UI 
    def _construir_ui(self):
        # Encabezado
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

        # Formulario de inserción / búsqueda / eliminación
        form = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        form.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        # Campos del formulario
        # campos permite definir el label, el atributo del entry y la sugerencia de placeholder
        campos = [
            ("Código:", "entry_codigo", "ABC-DEF-0001"), 
            ("Nombre:", "entry_nombre", "Producto..."),
            ("Precio $:", "entry_precio", "0.00"), 
            ("Stock:", "entry_stock", "Cantidad")
        ]
        # Crear los labels y entries dinámicamente
        for i, (label, attr, sugerencia) in enumerate(campos):
            ctk.CTkLabel(form, text=label, text_color=COLOR_SUBTEXT,
                        font=ctk.CTkFont(size=12)).grid(row=0, column=i*2, padx=(16, 4), pady=(10, 4))
            
            entry = ctk.CTkEntry(form, width=130, placeholder_text=sugerencia)
            entry.grid(row=0, column=i*2+1, padx=(0, 8), pady=(10, 4))
            
            setattr(self, attr, entry)

        # Botones en fila separada para que no se salgan de la pantalla
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.grid(row=1, column=0, columnspan=8, pady=(4, 4))
        # Botones de acción para insertar, buscar, eliminar y limpiar
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
        self.lbl_estado.grid(row=2, column=0, columnspan=8, pady=(0, 8))

        # Tabla de productos con scroll y paginación
        tabla_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        tabla_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 20))
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Encabezados tabla
        cols = [("Código", 160), ("Nombre", 240), ("Precio $", 110),
                ("Stock", 80), ("Estado stock", 120)]
        hdr = ctk.CTkFrame(tabla_frame, fg_color="#111827", corner_radius=8)
        hdr.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 0))
        for i, (col, w) in enumerate(cols):
            ctk.CTkLabel(hdr, text=col, width=w,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=COLOR_ACCENT).grid(row=0, column=i, padx=4, pady=6)

        # Scroll para la tabla
        self.scroll_tabla = ctk.CTkScrollableFrame(
            tabla_frame, fg_color="transparent", corner_radius=0)
        self.scroll_tabla.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        tabla_frame.grid_rowconfigure(1, weight=1)

        # Barra de paginación
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

    # Acciones de los botones
    # Funciones para insertar, buscar y eliminar productos en el BST
    # Se inserta un producto solo si no existe el código
    def _insertar(self):
        codigo = self.entry_codigo.get().strip().upper()
        nombre = self.entry_nombre.get().strip()
        precio_txt = self.entry_precio.get().strip()
        stock_txt  = self.entry_stock.get().strip()

        if not codigo or not nombre or not precio_txt or not stock_txt:
            self.bell()
            messagebox.showwarning("Campos incompletos",
                "Para insertar un producto debes llenar los 4 campos:\n"
                "Código, Nombre, Precio y Stock.")
            return

        try:
            precio = float(precio_txt)
            stock  = int(stock_txt)
        except ValueError:
            self.bell()
            messagebox.showerror("Datos inválidos",
                "Precio debe ser un número decimal y Stock un número entero.")
            return

        if precio <= 0:
            self.bell()
            messagebox.showwarning("Precio inválido", "El precio debe ser mayor a 0.")
            return

        if stock < 0:
            self.bell()
            messagebox.showwarning("Stock inválido", "El stock no puede ser negativo.")
            return

        producto = Producto(codigo, nombre, precio, stock)
        self.app.arbol.insertar(producto)
        self._set_estado(f"✅  Producto {codigo} insertado en el BST.", COLOR_ACCENT)
        self._limpiar_form()
        self._refrescar_tabla()
    # Función para buscar un producto por código en el BST
    def _buscar(self):
        codigo = self.entry_codigo.get().strip().upper()
        if not codigo:
            self.bell()
            messagebox.showwarning("Campo vacío",
                "Ingresa un código en el campo 'Código' para buscar.")
            return
        p = self.app.arbol.buscar(codigo)
        if p:
            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, p.nombre)
            self.entry_precio.delete(0, "end")
            self.entry_precio.insert(0, str(p.precio))
            self.entry_stock.delete(0, "end")
            self.entry_stock.insert(0, str(p.stock))
            self._set_estado(f"🔍  Producto {codigo} encontrado en el BST.", COLOR_ACCENT)
        else:
            self.bell()
            messagebox.showinfo("No encontrado",
                f"El código {codigo} no existe en el catálogo.")
    # Función para eliminar un producto por código en el BST
    def _eliminar(self):
        codigo = self.entry_codigo.get().strip().upper()
        if not codigo:
            self.bell()
            messagebox.showwarning("Campo vacío",
                "Ingresa el código del producto a eliminar en el campo 'Código'.")
            return
        ok = self.app.arbol.eliminar(codigo)
        if ok:
            self._set_estado(f"🗑️  Producto {codigo} eliminado del BST.", COLOR_ACCENT)
            self._limpiar_form()
            self._refrescar_tabla()
        else:
            self.bell()
            messagebox.showerror("No existe",
                f"El código {codigo} no existe en el BST. No se puede eliminar.")
    # Función para limpiar los campos del formulario
    def _limpiar_form(self):
        for attr in ("entry_codigo", "entry_nombre", "entry_precio", "entry_stock"):
            getattr(self, attr).delete(0, "end")
    # Función para actualizar el mensaje de estado en la interfaz
    def _set_estado(self, msg: str, color: str = COLOR_ACCENT):
        self.lbl_estado.configure(text=msg, text_color=color)

    # Paginación de la tabla
    def _total_paginas(self) -> int:
        total = self.app.arbol.total()
        if total == 0:
            return 1
        return (total - 1) // self.items_por_pag + 1
    # Cambiar página (anterior o siguiente)
    def _cambiar_pagina(self, delta: int):
        nueva_pagina = self.pagina + delta
        if 0 <= nueva_pagina < self._total_paginas():
            self.pagina = nueva_pagina
            self._refrescar_tabla()

    # Tabla dinámica (recorrido inorden del BST)
    def _refrescar_tabla(self):
        for widget in self.scroll_tabla.winfo_children():
            widget.destroy()

        lista_total = self.app.arbol.inorden()
        total_items = len(lista_total)

        if self.pagina >= self._total_paginas():
            self.pagina = self._total_paginas() - 1

        inicio = self.pagina * self.items_por_pag
        fin = inicio + self.items_por_pag
        productos_pagina = lista_total[inicio:fin]

        if total_items == 0:
            self.lbl_paginacion.configure(text="Sin productos")
        else:
            self.lbl_paginacion.configure(
                text=f"Página {self.pagina + 1} de {self._total_paginas()}"
                     f"   ·   mostrando {inicio + 1}–{min(fin, total_items)} de {total_items}")

        for idx, p in enumerate(productos_pagina):
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

        self.lbl_info_arbol.configure(
            text=f"BST: {self.app.arbol.total()} productos | "
                 f"Altura: {self.app.arbol.altura()} niveles")
        self.app.actualizar_stats()