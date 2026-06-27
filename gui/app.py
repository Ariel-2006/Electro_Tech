# =============================================================
#  ElectroTech Store — Ventana principal
#  Archivo: gui/app.py
#  Descripción: Ventana principal con menú lateral y 4 paneles.
#               Instancia las estructuras y las comparte con todos
#               los paneles (única fuente de verdad).
# =============================================================

import customtkinter as ctk
import threading

from structures.bst_productos  import ArbolBST
from structures.queue_pedidos  import Cola
from structures.stack_historial import Pila
from data.generator            import generar_todo

from gui.panel_productos   import PanelProductos
from gui.panel_pedidos     import PanelPedidos
from gui.panel_algoritmos  import PanelAlgoritmos
from gui.panel_generador   import PanelGenerador

# Tema global
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

COLOR_BG      = "#0f1117"
COLOR_SIDEBAR  = "#1a1f2e"
COLOR_ACCENT   = "#00c896"
COLOR_TEXT     = "#e2e8f0"
COLOR_SUBTEXT  = "#94a3b8"


class AppElectroTech(ctk.CTk):
    """
    Ventana principal de ElectroTech Store.
    Contiene el menú lateral y renderiza el panel activo.
    """

    def __init__(self):
        super().__init__()

        # ------ Configuración ventana ------
        self.title("⚡ ElectroTech Store — Gestión de Inventario")
        self.geometry("1200x700")
        self.minsize(1100, 650)
        self.configure(fg_color=COLOR_BG)

        # ------ Estructuras de datos (compartidas por todos los paneles) ------
        self.arbol  = ArbolBST()
        self.cola   = Cola()
        self.pila   = Pila()
        self._contador_pedido = 1

        # ------ Layout principal: sidebar + contenido ------
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._construir_sidebar()
        self._construir_area_contenido()

        # Mostrar panel inicial
        self._panel_activo = None
        self._botones_menu = {}
        self._registrar_botones()
        self.mostrar_panel("productos")

    # ------------------------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------------------------

    def _construir_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, fg_color=COLOR_SIDEBAR,
                               corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Logo / título
        ctk.CTkLabel(sidebar, text="⚡ ElectroTech",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLOR_ACCENT).pack(pady=(30, 4))
        ctk.CTkLabel(sidebar, text="Store Manager",
                     font=ctk.CTkFont(size=12),
                     text_color=COLOR_SUBTEXT).pack(pady=(0, 30))

        # Botones de navegación
        self._btn_productos  = self._boton_menu(sidebar, "🖥️  Catálogo",    "productos")
        self._btn_pedidos    = self._boton_menu(sidebar, "📦  Pedidos",      "pedidos")
        self._btn_algoritmos = self._boton_menu(sidebar, "⚡  Algoritmos",   "algoritmos")
        self._btn_generador  = self._boton_menu(sidebar, "🎲  Generador",    "generador")

        # Estadísticas rápidas
        ctk.CTkLabel(sidebar, text="────────────────",
                     text_color=COLOR_SUBTEXT).pack(pady=(20, 0))

        self.lbl_stat_arbol = ctk.CTkLabel(sidebar, text="Árbol: 0 productos",
                                            text_color=COLOR_SUBTEXT,
                                            font=ctk.CTkFont(size=11))
        self.lbl_stat_arbol.pack(pady=2)

        self.lbl_stat_cola = ctk.CTkLabel(sidebar, text="Cola: 0 pedidos",
                                           text_color=COLOR_SUBTEXT,
                                           font=ctk.CTkFont(size=11))
        self.lbl_stat_cola.pack(pady=2)

        self.lbl_stat_pila = ctk.CTkLabel(sidebar, text="Historial: 0 registros",
                                           text_color=COLOR_SUBTEXT,
                                           font=ctk.CTkFont(size=11))
        self.lbl_stat_pila.pack(pady=2)

        # Créditos
        ctk.CTkLabel(sidebar,
                     text="Freddy · Zuly · Ariel · Wendy",
                     font=ctk.CTkFont(size=9),
                     text_color="#475569").place(relx=0.5, rely=0.97, anchor="s")

    def _boton_menu(self, parent, texto: str, panel_id: str) -> ctk.CTkButton:
        btn = ctk.CTkButton(
            parent,
            text=texto,
            anchor="w",
            fg_color="transparent",
            hover_color="#2a3447",
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(size=13),
            height=42,
            corner_radius=8,
            command=lambda p=panel_id: self.mostrar_panel(p)
        )
        btn.pack(fill="x", padx=12, pady=3)
        return btn

    def _registrar_botones(self):
        self._botones_menu = {
            "productos":  self._btn_productos,
            "pedidos":    self._btn_pedidos,
            "algoritmos": self._btn_algoritmos,
            "generador":  self._btn_generador,
        }

    # ------------------------------------------------------------------
    # ÁREA DE CONTENIDO
    # ------------------------------------------------------------------

    def _construir_area_contenido(self):
        self.frame_contenido = ctk.CTkFrame(self, fg_color=COLOR_BG,
                                             corner_radius=0)
        self.frame_contenido.grid(row=0, column=1, sticky="nsew", padx=0)
        self.frame_contenido.grid_columnconfigure(0, weight=1)
        self.frame_contenido.grid_rowconfigure(0, weight=1)
        self._panel_widget_actual = None

    # ------------------------------------------------------------------
    # NAVEGACIÓN
    # ------------------------------------------------------------------

    def mostrar_panel(self, panel_id: str):
        """Destruye el panel actual y renderiza el nuevo."""
        if self._panel_widget_actual is not None:
            self._panel_widget_actual.destroy()

        # Resaltar botón activo
        for pid, btn in self._botones_menu.items():
            if pid == panel_id:
                btn.configure(fg_color="#1e3a2f", text_color=COLOR_ACCENT)
            else:
                btn.configure(fg_color="transparent", text_color=COLOR_TEXT)

        # Construir panel
        if panel_id == "productos":
            panel = PanelProductos(self.frame_contenido, self)
        elif panel_id == "pedidos":
            panel = PanelPedidos(self.frame_contenido, self)
        elif panel_id == "algoritmos":
            panel = PanelAlgoritmos(self.frame_contenido, self)
        elif panel_id == "generador":
            panel = PanelGenerador(self.frame_contenido, self)
        else:
            return

        panel.grid(row=0, column=0, sticky="nsew")
        self._panel_widget_actual = panel
        self._panel_activo = panel_id
        self.actualizar_stats()

    # ------------------------------------------------------------------
    # ESTADÍSTICAS SIDEBAR
    # ------------------------------------------------------------------

    def actualizar_stats(self):
        """Actualiza los contadores del sidebar."""
        self.lbl_stat_arbol.configure(
            text=f"Árbol: {self.arbol.total()} productos")
        self.lbl_stat_cola.configure(
            text=f"Cola: {self.cola.tamanio()} pedidos")
        self.lbl_stat_pila.configure(
            text=f"Historial: {self.pila.tamanio()} registros")

    # ------------------------------------------------------------------
    # HELPER COMPARTIDO — generar ID de pedido
    # ------------------------------------------------------------------

    def nuevo_id_pedido(self) -> str:
        id_str = f"PED-{self._contador_pedido:05d}"
        self._contador_pedido += 1
        return id_str
