"""Registro visual de la crónica de guerra."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..lore import LoreEntry
from .theme import (
    DANGER, DANGER_SOFT, GOLD_LIGHT, MUTED, MUTED_DARK, SANS, SERIF, TEXT,
)


class StoryLog(tk.Frame):
    HEAD_COLORS = {
        "move": GOLD_LIGHT,
        "capture": DANGER_SOFT,
        "check": "#e8bd77",
        "castle": GOLD_LIGHT,
        "promo": GOLD_LIGHT,
        "mate": DANGER,
        "prologue": MUTED,
        "epilogue": GOLD_LIGHT,
        "ambient": MUTED_DARK,
        "event": "#d8b978",
        "fog": MUTED,
    }

    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, bg="#140f1c")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text = tk.Text(
            self, bg="#140f1c", fg=TEXT, bd=0, relief="flat",
            wrap="word", padx=10, pady=8, font=(SERIF, 9),
            insertbackground=GOLD_LIGHT, cursor="arrow", highlightthickness=0,
            spacing1=1, spacing3=2, width=1, height=1,
        )
        self.text.grid(row=0, column=0, sticky="nsew")
        scroll = ttk.Scrollbar(
            self, orient="vertical", command=self.text.yview,
            style="Dark.Vertical.TScrollbar",
        )
        scroll.grid(row=0, column=1, sticky="ns", padx=(4, 0))
        self.text.configure(yscrollcommand=scroll.set)
        self._configure_tags()

    def _configure_tags(self) -> None:
        for tag, color in self.HEAD_COLORS.items():
            font = (SANS, 8, "bold") if tag != "ambient" else (SANS, 7, "bold")
            self.text.tag_configure(
                f"head_{tag}", foreground=color, font=font,
                spacing1=7, spacing3=2,
            )
        self.text.tag_configure("body", foreground=TEXT, font=(SERIF, 9), spacing3=9)
        self.text.tag_configure(
            "body_ambient", foreground=MUTED_DARK, font=(SERIF, 8, "italic"),
            spacing3=9,
        )
        self.text.tag_configure(
            "body_prologue", foreground=MUTED, font=(SERIF, 9),
            spacing3=9,
        )
        self.text.tag_configure(
            "body_epilogue", foreground=GOLD_LIGHT, font=(SERIF, 9, "italic"),
            spacing3=9,
        )
        self.text.tag_configure(
            "body_event", foreground="#d8b978", font=(SERIF, 9, "italic"),
            spacing3=9,
        )
        self.text.tag_configure(
            "body_fog", foreground=MUTED, font=(SERIF, 9, "italic"),
            spacing3=9,
        )
        self.text.configure(state="disabled")

    def redraw(self, entries: list[LoreEntry]) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        if not entries:
            self.text.insert("end", "CRÓNICA DE GUERRA\n", ("head_ambient",))
            self.text.insert(
                "end",
                "La crónica aguarda su primera página. El tablero respira.",
                ("body_ambient",),
            )
        else:
            for entry in entries:
                self._insert_entry(entry)
        self.text.configure(state="disabled")
        self.text.see("end")

    def append(self, entry: LoreEntry) -> None:
        self.text.configure(state="normal")
        self._insert_entry(entry)
        self.text.configure(state="disabled")
        self.text.see("end")

    def _insert_entry(self, entry: LoreEntry) -> None:
        head_tag = f"head_{entry.tag}"
        if entry.tag in ("prologue", "epilogue", "ambient", "event", "fog"):
            body_tag = f"body_{entry.tag}"
        else:
            body_tag = "body"
        if entry.tag == "ambient":
            self.text.insert("end", f"{entry.heading}  —  ", (head_tag,))
            self.text.insert("end", f"{entry.text}\n", (body_tag,))
        else:
            self.text.insert("end", f"{entry.heading}\n", (head_tag,))
            self.text.insert("end", f"{entry.text}\n", (body_tag,))
