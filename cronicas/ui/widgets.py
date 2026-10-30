"""Widgets y utilidades visuales reutilizables."""

from __future__ import annotations

import tkinter as tk
from typing import Callable

from .theme import (
    BORDER, BORDER_SOFT, GOLD, GOLD_LIGHT, MUTED_DARK, PANEL, PANEL_3, SANS, TEXT,
)


def make_button(
    parent: tk.Misc,
    text: str,
    command: Callable[[], None],
    accent: bool = False,
    compact: bool = False,
) -> tk.Button:
    bg = GOLD if accent else PANEL_3
    fg = "#181020" if accent else TEXT
    hover = GOLD_LIGHT if accent else "#342545"
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=hover,
        activeforeground=fg,
        disabledforeground=MUTED_DARK,
        relief="flat",
        bd=0,
        highlightthickness=0,
        padx=10 if compact else 16,
        pady=4 if compact else 8,
        font=(SANS, 8 if compact else 9, "bold"),
        cursor="hand2",
    )

    def on_enter(_event):
        if str(button["state"]) != "disabled":
            button.configure(bg=hover)

    def on_leave(_event):
        if str(button["state"]) != "disabled":
            button.configure(bg=bg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button


def rounded_rect(canvas: tk.Canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1,
        x2, y1 + radius, x2, y2 - radius, x2, y2,
        x2 - radius, y2, x1 + radius, y2, x1, y2,
        x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=24, **kwargs)


def center_window(window: tk.Toplevel, parent: tk.Misc) -> None:
    window.update_idletasks()
    width = max(window.winfo_reqwidth(), 420)
    height = max(window.winfo_reqheight(), 220)
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
    y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2 - 10
    x = max(20, min(x, screen_w - width - 20))
    y = max(20, min(y, screen_h - height - 60))
    window.geometry(f"{width}x{height}+{x}+{y}")


def card(parent: tk.Misc, title: str) -> tuple[tk.Frame, tk.Frame]:
    outer = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
    header = tk.Frame(outer, bg=PANEL)
    header.pack(fill="x", padx=14, pady=(8, 0))
    tk.Label(
        header, text=title, bg=PANEL, fg=GOLD,
        font=(SANS, 8, "bold"),
    ).pack(anchor="w")
    tk.Frame(outer, bg=BORDER_SOFT, height=1).pack(fill="x", padx=14, pady=(5, 0))
    body = tk.Frame(outer, bg=PANEL)
    body.pack(fill="both", expand=True, padx=14, pady=8)
    return outer, body


def bind_recursive(widget: tk.Misc, sequence: str, callback) -> None:
    widget.bind(sequence, callback)
    for child in widget.winfo_children():
        bind_recursive(child, sequence, callback)
