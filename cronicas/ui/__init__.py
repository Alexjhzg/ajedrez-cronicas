"""Interfaz gráfica de Crónicas de Aethelgard."""

from .app import ChroniclesApp


def run() -> None:
    app = ChroniclesApp()
    app.mainloop()


__all__ = ["ChroniclesApp", "run"]
