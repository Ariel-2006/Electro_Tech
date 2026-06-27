# =============================================================
#  ElectroTech Store — Punto de entrada
#  Archivo: main.py
#  Uso: python main.py
# =============================================================

import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import AppElectroTech


def main():
    app = AppElectroTech()
    app.mainloop()


if __name__ == "__main__":
    main()
