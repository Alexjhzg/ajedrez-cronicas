"""Barra de estado situada bajo el tablero."""

from __future__ import annotations

import tkinter as tk

from .. import lore
from .state import ViewState
from .theme import BG, FACTION_ACCENT, GOLD_DIM, IVORY, MUTED, SANS, VIOLET


class StatusBar(tk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, bg=BG)
        self.grid_columnconfigure(0, weight=1)
        self.hint_label = tk.Label(
            self, text="La crónica aguarda…", bg=BG, fg=MUTED,
            font=(SANS, 9), anchor="w",
        )
        self.hint_label.grid(row=0, column=0, sticky="w")
        self.move_label = tk.Label(
            self, text="", bg=BG, fg=GOLD_DIM,
            font=(SANS, 8, "bold"), anchor="e",
        )
        self.move_label.grid(row=0, column=1, sticky="e", padx=(12, 0))

    def set_hint(self, text: str, color: str = MUTED) -> None:
        self.hint_label.configure(text=text, fg=color)

    def update(self, state: ViewState) -> None:
        player_color = state.game.turn_order[0] if state.game.turn_order else "w"
        if state.game_over:
            hint, color = "La crónica ha terminado.", MUTED
        elif not state.started:
            hint, color = "La crónica aguarda…", MUTED
        elif state.busy:
            hint, color = "El destino se escribe…", GOLD_DIM
        elif state.ai_thinking:
            hint, color = "El Oráculo Umbrío medita…", VIOLET
        elif state.mode == "ai" and state.game.turn != player_color:
            f_name = lore.faction_name(state.game.turn)
            hint, color = f"{f_name} mueve. Observa.", FACTION_ACCENT.get(state.game.turn, VIOLET)
        elif state.selected is not None:
            hint, color = "Elige una casilla iluminada.", IVORY
        else:
            hint, color = "Selecciona una pieza para mover.", MUTED
        self.set_hint(hint, color)

        if state.notation:
            self.move_label.configure(
                text=f"Crónica {lore.to_roman(state.chapter)} · {state.notation[-1]}"
            )
        else:
            self.move_label.configure(text="La primera página está en blanco")
