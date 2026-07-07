#Genera 1,000+ productos/pedidos en un hilo separado para no congelar la GUI. Muestra barra de progreso y log de resultados.
import customtkinter as ctk
import threading
import time
from data.generator import generar_todo

COLOR_ACCENT  = "#00c896"
COLOR_BG      = "#0f1117"
COLOR_CARD    = "#1a1f2e"
COLOR_TEXT    = "#e2e8f0"
COLOR_SUBTEXT = "#94a3b8"
COLOR_ERROR   = "#f87171"
COLOR_WARN    = "#fbbf24"

# Clase PanelGenerador: permite generar datos sintéticos masivos (productos y pedidos) 
# en un hilo separado para no congelar la GUI. Muestra barra de progreso y log de resultados.
class PanelGenerador(ctk.CTkFrame):
    """
    Panel de carga masiva de datos sintéticos.
    Usa threading para no congelar CustomTkinter durante la inserción.
    """

    def __init__(self, parent, app):
        super().__init__(parent, fg_color=COLOR_BG, corner_radius=0)
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self._generando = False
        self._construir_ui()

    def _construir_ui(self):
        # ── Encabezado ──
        header = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        ctk.CTkLabel(header, text="🎲  Generador Masivo de Datos Sintéticos",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLOR_ACCENT).pack(side="left", padx=16, pady=12)

        # ── Controles ──
        ctrl = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        ctrl.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

        ctk.CTkLabel(ctrl, text="Productos a generar:",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=12)).grid(
            row=0, column=0, padx=16, pady=16)

        self.entry_n = ctk.CTkEntry(ctrl, width=100, placeholder_text="1000")
        self.entry_n.insert(0, "1000")
        self.entry_n.grid(row=0, column=1, padx=8)

        ctk.CTkLabel(ctrl, text="Pedidos a encolar:",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=12)).grid(
            row=0, column=2, padx=16)

        self.entry_p = ctk.CTkEntry(ctrl, width=100, placeholder_text="500")
        self.entry_p.insert(0, "500")
        self.entry_p.grid(row=0, column=3, padx=8)

        ctk.CTkLabel(ctrl, text="Limpiar estructuras antes:",
                     text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=12)).grid(
            row=0, column=4, padx=16)

        self.check_limpiar = ctk.CTkCheckBox(ctrl, text="", width=30)
        self.check_limpiar.select()
        self.check_limpiar.grid(row=0, column=5, padx=4)

        self.btn_generar = ctk.CTkButton(
            ctrl, text="🚀 GENERAR AHORA", width=160, height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=COLOR_ACCENT, text_color="#000",
            command=self._iniciar_generacion)
        self.btn_generar.grid(row=0, column=6, padx=20)

        # ── Barra de progreso ──
        prog_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        prog_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        prog_frame.grid_columnconfigure(0, weight=1)

        self.lbl_progreso = ctk.CTkLabel(
            prog_frame, text="Listo para generar datos...",
            text_color=COLOR_SUBTEXT, font=ctk.CTkFont(size=12))
        self.lbl_progreso.pack(padx=16, pady=(12, 4))

        self.progress_bar = ctk.CTkProgressBar(prog_frame, height=14,
                                                progress_color=COLOR_ACCENT)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=16, pady=(0, 12))

        # ── Log de resultados ──
        log_frame = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=12)
        log_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(5, 20))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(log_frame, text="📋 Log de resultados",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLOR_SUBTEXT).grid(row=0, column=0, padx=16, pady=(12, 4), sticky="w")

        self.txt_log = ctk.CTkTextbox(log_frame, fg_color="#111827",
                                       text_color=COLOR_TEXT,
                                       font=ctk.CTkFont(family="Courier", size=11))
        self.txt_log.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        log_frame.grid_rowconfigure(1, weight=1)

        self._log("Sistema iniciado. Presiona 'GENERAR AHORA' para cargar datos masivos.")

    # Genera productos y pedidos en un hilo separado para no congelar la GUI
    def _iniciar_generacion(self):
        if self._generando:
            return
        try:
            n_prod = int(self.entry_n.get().strip())
            n_ped  = int(self.entry_p.get().strip())
        except ValueError:
            self._log("⚠️  Valores inválidos. Usa números enteros.", COLOR_WARN)
            return

        if n_prod < 1:
            self._log("⚠️  Debes generar al menos 1 producto.", COLOR_WARN)
            return

        self._generando = True
        self.btn_generar.configure(state="disabled", text="⏳ Generando...")
        self.progress_bar.set(0)

        hilo = threading.Thread(
            target=self._generar_en_hilo,
            args=(n_prod, n_ped),
            daemon=True)
        hilo.start()

    def _generar_en_hilo(self, n_prod: int, n_ped: int):
        """Corre en thread separado para no bloquear la GUI."""
        try:
            inicio = time.perf_counter()

            # Limpiar estructuras si está marcado
            if self.check_limpiar.get():
                self.app.arbol._raiz  = None
                self.app.arbol._total = 0
                self.app.cola.limpiar()
                self.app.pila.limpiar()
                self._actualizar_ui(lambda: self._log("🧹 Estructuras limpiadas."))

            # Generar datos
            self._actualizar_ui(lambda: self._log(f"⚙️  Generando {n_prod} productos..."))
            self._actualizar_ui(lambda: self.progress_bar.set(0.1))

            productos, pedidos = generar_todo(n_prod, n_ped)

            # Insertar productos en BST
            self._actualizar_ui(lambda: self._log(f"🌳 Insertando en BST..."))
            self._actualizar_ui(lambda: self.progress_bar.set(0.3))

            for i, p in enumerate(productos):
                self.app.arbol.insertar(p)
                if i % 100 == 0:
                    progreso = 0.3 + (i / n_prod) * 0.4
                    self._actualizar_ui(
                        lambda pr=progreso: self.progress_bar.set(pr))

            self._actualizar_ui(lambda: self.progress_bar.set(0.7))
            self._actualizar_ui(lambda: self._log(f"📦 Encolando {n_ped} pedidos..."))

            # Encolar pedidos
            for p in pedidos:
                self.app.cola.enqueue(p)

            self._actualizar_ui(lambda: self.progress_bar.set(0.95))

            fin       = time.perf_counter()
            tiempo_ms = round((fin - inicio) * 1000, 2)

            # Resultados finales
            self._actualizar_ui(lambda: self._mostrar_resultado(
                n_prod, n_ped, tiempo_ms))

        except Exception as e:
            self._actualizar_ui(lambda: self._log(f"❌ Error: {e}", COLOR_ERROR))
        finally:
            self._generando = False
            self._actualizar_ui(lambda: self.btn_generar.configure(
                state="normal", text="🚀 GENERAR AHORA"))

    def _mostrar_resultado(self, n_prod, n_ped, tiempo_ms):
        self.progress_bar.set(1.0)
        self._log("─" * 60)
        self._log(f"✅  GENERACIÓN COMPLETADA")
        self._log(f"   Productos insertados en BST : {n_prod:>6}")
        self._log(f"   Pedidos encolados (FIFO)    : {n_ped:>6}")
        self._log(f"   Altura del árbol BST        : {self.app.arbol.altura():>6} niveles")
        self._log(f"   Tiempo total                : {tiempo_ms:>6} ms")
        self._log("─" * 60)
        self.app.actualizar_stats()

    def _actualizar_ui(self, fn):
        """Programa la actualización en el hilo principal de Tkinter."""
        self.after(0, fn)

    def _log(self, mensaje: str, color: str = None):
        self.txt_log.configure(state="normal")
        self.txt_log.insert("end", mensaje + "\n")
        self.txt_log.see("end")
        self.txt_log.configure(state="disabled")