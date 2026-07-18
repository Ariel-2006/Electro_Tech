# Panel de comparación de algoritmos de ordenación y búsqueda para la GUI.
import customtkinter as ctk
from tkinter import messagebox
from algorithms.sorting   import bubble_sort, quick_sort, merge_sort, comparar_algoritmos
from algorithms.searching import busqueda_binaria, busqueda_lineal

COLOR_ACCENT  = "#00c896"
COLOR_BG      = "#0f1117"
COLOR_CARD    = "#1a1f2e"
COLOR_TEXT    = "#e2e8f0"
COLOR_SUBTEXT = "#94a3b8"
COLOR_ERROR   = "#f87171"
COLOR_WARN    = "#fbbf24"
COLOR_INFO    = "#60a5fa"
COLOR_BUBBLE  = "#f59e0b"
COLOR_QUICK   = "#34d399"
COLOR_MERGE   = "#a78bfa"


class PanelAlgoritmos(ctk.CTkFrame):
    """
    Panel de comparación de algoritmos de ordenación y búsqueda.
    Muestra los tiempos en milisegundos directamente en pantalla.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BG, corner_radius=0)
        self.app = app
        self._lista_ordenada = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ──
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        ctk.CTkLabel(header, text="⚡  Algoritmos de Ordenación y Búsqueda",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLOR_ACCENT).pack(side="left", padx=16, pady=12)

        # ── Controles de Ordenación ──
        ctrl = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        ctrl.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

        ctk.CTkLabel(ctrl, text="Ordenar por:",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=11)).grid(
            row=0, column=0, padx=16, pady=12)

        self.combo_clave = ctk.CTkComboBox(
            ctrl, values=["precio", "codigo", "nombre", "stock"],
            width=130, state="readonly")
        self.combo_clave.set("precio")
        self.combo_clave.grid(row=0, column=1, padx=8)

        ctk.CTkButton(ctrl, text="🔄 Comparar los 3 algoritmos", width=200,
                      fg_color=COLOR_ACCENT, text_color="#000",
                      command=self._comparar).grid(row=0, column=2, padx=16)
        ctk.CTkButton(ctrl, text="BubbleSort", width=100,
                      fg_color=COLOR_BUBBLE, text_color="#000",
                      command=lambda: self._ordenar("bubble")).grid(row=0, column=3, padx=4)
        ctk.CTkButton(ctrl, text="QuickSort", width=100,
                      fg_color=COLOR_QUICK, text_color="#000",
                      command=lambda: self._ordenar("quick")).grid(row=0, column=4, padx=4)
        ctk.CTkButton(ctrl, text="MergeSort", width=100,
                      fg_color=COLOR_MERGE, text_color="#000",
                      command=lambda: self._ordenar("merge")).grid(row=0, column=5, padx=4)

        # Tarjetas de tiempo
        tiempos_frame = ctk.CTkFrame(ctrl, fg_color="transparent")
        tiempos_frame.grid(row=1, column=0, columnspan=6, pady=(0, 10), padx=16, sticky="ew")

        self.lbl_bubble = self._tarjeta_tiempo(tiempos_frame, "🟡 BubbleSort", "— ms", COLOR_BUBBLE, 0)
        self.lbl_quick  = self._tarjeta_tiempo(tiempos_frame, "🟢 QuickSort",  "— ms", COLOR_QUICK,  1)
        self.lbl_merge  = self._tarjeta_tiempo(tiempos_frame, "🟣 MergeSort",  "— ms", COLOR_MERGE,  2)
        self.lbl_ganador = ctk.CTkLabel(tiempos_frame, text="",
                                         font=ctk.CTkFont(size=12, weight="bold"),
                                         text_color=COLOR_ACCENT)
        self.lbl_ganador.grid(row=1, column=0, columnspan=3, pady=(4, 0))

        # ── Búsqueda ──
        busq = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        busq.grid(row=2, column=0, sticky="nsew", padx=20, pady=(5, 20))
        busq.grid_columnconfigure(0, weight=1)
        busq.grid_rowconfigure(1, weight=1)

        # Búsqueda binaria
        row_bin = ctk.CTkFrame(busq, fg_color="transparent")
        row_bin.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 4))

        ctk.CTkLabel(row_bin, text="🔍 Búsqueda Binaria (código exacto):",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=11)).pack(side="left")
        self.entry_bin = ctk.CTkEntry(row_bin, width=180, placeholder_text="LAP-SAM-0001")
        self.entry_bin.pack(side="left", padx=10)
        ctk.CTkButton(row_bin, text="Buscar", width=80,
                      fg_color=COLOR_INFO, text_color="#000",
                      command=self._buscar_binaria).pack(side="left", padx=4)

        # Búsqueda lineal
        row_lin = ctk.CTkFrame(busq, fg_color="transparent")
        row_lin.grid(row=1, column=0, sticky="ew", padx=16, pady=4)

        ctk.CTkLabel(row_lin, text="🔎 Búsqueda Lineal (nombre parcial):",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=11)).pack(side="left")
        self.entry_lin = ctk.CTkEntry(row_lin, width=180, placeholder_text="Samsung")
        self.entry_lin.pack(side="left", padx=10)
        ctk.CTkButton(row_lin, text="Buscar", width=80,
                      fg_color=COLOR_MERGE, text_color="#fff",
                      command=self._buscar_lineal).pack(side="left", padx=4)

        # Resultado búsqueda
        self.lbl_busq = ctk.CTkLabel(busq, text="",
                                      text_color=COLOR_ACCENT,
                                      font=ctk.CTkFont(size=11))
        self.lbl_busq.grid(row=2, column=0, padx=16, pady=4)

        # Scroll resultado
        self.scroll_resultados = ctk.CTkScrollableFrame(
            busq, fg_color="transparent", corner_radius=0)
        self.scroll_resultados.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))
        busq.grid_rowconfigure(3, weight=1)

    def _tarjeta_tiempo(self, parent, titulo, valor, color, col):
        frame = ctk.CTkFrame(parent, fg_color="#111827", corner_radius=8, width=200)
        frame.grid(row=0, column=col, padx=8, pady=4, sticky="ew")
        ctk.CTkLabel(frame, text=titulo, text_color=color,
                     font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(8, 2))
        lbl = ctk.CTkLabel(frame, text=valor,
                            font=ctk.CTkFont(size=22, weight="bold"),
                            text_color=color)
        lbl.pack(pady=(0, 8))
        return lbl

   # Ordenación y comparación de algoritmos
    def _obtener_lista(self) -> list:
        return self.app.arbol.inorden()

    def _comparar(self):
        lista = self._obtener_lista()
        if not lista:
            self.bell()
            messagebox.showinfo("Catálogo vacío",
                "No hay productos para ordenar.\n"
                "Ve al panel Generador y carga datos primero.")
            return
        clave    = self.combo_clave.get()
        resultado = comparar_algoritmos(lista, clave)

        t_b = resultado["bubble"]["tiempo_ms"]
        t_q = resultado["quick"]["tiempo_ms"]
        t_m = resultado["merge"]["tiempo_ms"]

        self.lbl_bubble.configure(text=f"{t_b} ms")
        self.lbl_quick.configure( text=f"{t_q} ms")
        self.lbl_merge.configure( text=f"{t_m} ms")

        minimo = min(t_b, t_q, t_m)
        if minimo == t_b:
            ganador = "BubbleSort"
        elif minimo == t_q:
            ganador = "QuickSort"
        else:
            ganador = "MergeSort"
        
        self.lbl_ganador.configure(
            text=f"🏆 Más rápido: {ganador} con {minimo} ms ordenando {len(lista)} productos por {clave}",
            text_color=COLOR_ACCENT)

    def _ordenar(self, algoritmo: str):
        lista = self._obtener_lista()
        if not lista:
            return
        clave = self.combo_clave.get()

        if algoritmo == "bubble":
            datos, ms = bubble_sort(lista, clave)
            self.lbl_bubble.configure(text=f"{ms} ms")

        elif algoritmo == "quick":
            datos, ms = quick_sort(lista, clave)
            self.lbl_quick.configure(text=f"{ms} ms")
            
        else:
            datos, ms = merge_sort(lista, clave)
            self.lbl_merge.configure(text=f"{ms} ms")

        self.lbl_ganador.configure(
            text=f"Ordenados {len(datos)} productos por {clave} en {ms} ms",
            text_color=COLOR_SUBTEXT)

    # Búsqueda de productos por código (binaria) o nombre (lineal)
    def _buscar_binaria(self):
        codigo = self.entry_bin.get().strip().upper()
        if not codigo:
            self.bell()
            messagebox.showwarning("Campo vacío",
                "Ingresa un código exacto para la búsqueda binaria.\n"
                "Ejemplo: LAP-SAM-0001")
            return

        # La búsqueda binaria requiere lista ordenada por código
        lista_ord = self.app.arbol.inorden()   # inorden ya está ordenada por código
        resultado, ms, comparaciones = busqueda_binaria(lista_ord, codigo)

        for w in self.scroll_resultados.winfo_children():
            w.destroy()

        if resultado:
            self.lbl_busq.configure(
                text=f"✅  Encontrado en {ms} ms con {comparaciones} comparaciones "
                     f"(de {len(lista_ord)} productos)",
                text_color=COLOR_ACCENT)
            self._fila_resultado(resultado)
        else:
            self.lbl_busq.configure(
                text=f"❌  '{codigo}' no encontrado. {comparaciones} comparaciones en {ms} ms",
                text_color=COLOR_ERROR)

    def _buscar_lineal(self):
        termino = self.entry_lin.get().strip()
        if not termino:
            self.bell()
            messagebox.showwarning("Campo vacío",
                "Ingresa un término parcial para la búsqueda lineal.\n"
                "Ejemplo: Samsung, Laptop, Xiaomi")
            return

        lista = self.app.arbol.inorden()
        resultados, ms, comparaciones = busqueda_lineal(lista, termino)

        for w in self.scroll_resultados.winfo_children():
            w.destroy()

        self.lbl_busq.configure(
            text=f"🔎  {len(resultados)} resultado(s) para '{termino}' "
                 f"en {ms} ms | {comparaciones} comparaciones",
            text_color=COLOR_INFO)

        for p in resultados:
            self._fila_resultado(p)

    def _fila_resultado(self, p):
        fila = ctk.CTkFrame(self.scroll_resultados, fg_color="#111827", corner_radius=6)
        fila.pack(fill="x", pady=2, padx=4)
        ctk.CTkLabel(fila, text=f"{p.codigo}  |  {p.nombre}  |  ${p.precio:.2f}  |  Stock: {p.stock}",
                     text_color=COLOR_TEXT, font=ctk.CTkFont(size=11)).pack(padx=12, pady=6)