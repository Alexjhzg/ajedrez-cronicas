"""Diálogos modales de la aplicación (4 reinos y múltiples frentes)."""

from __future__ import annotations

import time
import tkinter as tk
from typing import Callable, Optional

from .. import lore
from ..engine import (
    ALL_COLORS, AMAZON, BISHOP, BLACK, ELEPHANT, FALCON, GREEN, KNIGHT, QUEEN,
    RED, ROOK, WHITE, Game,
)
from .theme import (
    BG, BORDER, BORDER_SOFT, DANGER, DIFFICULTIES, FACTION_ACCENT, GLYPH_FONT,
    GOLD, GOLD_LIGHT, IVORY, MUTED, MUTED_DARK, PANEL_2, PANEL_3, PIECE_GLYPHS,
    SANS, SERIF, TEXT, VIOLET, WHITE_FILL,
)
from .widgets import bind_recursive, center_window, make_button


class ModalDialog(tk.Toplevel):
    """Base común para ventanas modales centradas y con cierre controlado."""

    def __init__(
        self,
        master: tk.Misc,
        title: str,
        on_closed: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(master)
        self.master_window = master
        self._on_closed = on_closed
        self._closed = False
        self.title(title)
        self.configure(bg=BG)
        self.resizable(False, False)
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _present(self) -> None:
        self.update_idletasks()
        self._try_grab(0)
        self.after(30, self._center)
        self.after(60, self._focus)

    def _try_grab(self, attempt: int) -> None:
        if self._closed:
            return
        try:
            self.grab_set()
        except tk.TclError:
            if attempt < 10:
                self.after(20, lambda: self._try_grab(attempt + 1))

    def _center(self) -> None:
        if not self._closed:
            center_window(self, self.master_window)

    def _focus(self) -> None:
        if not self._closed:
            self.focus_force()

    def _close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()
        if self._on_closed is not None:
            self._on_closed()

    def _cancel(self) -> None:
        self._close()


class SetupDialog(ModalDialog):
    def __init__(
        self,
        master: tk.Misc,
        on_start: Callable[..., None],
        cancel_allowed: bool = True,
        on_cancel: Optional[Callable[[], None]] = None,
        on_closed: Optional[Callable[[], None]] = None,
        initial_mode: str = "ai",
        initial_difficulty: str = "Caballero",
        initial_wild: bool = False,
        initial_elephant: bool = False,
        initial_fog: bool = False,
        initial_crusade: bool = False,
        initial_four_fronts: bool = False,
        initial_player_color: str = WHITE,
        initial_imperial: bool = False,
    ) -> None:
        super().__init__(master, "Nueva crónica", on_closed)
        self.on_start = on_start
        self.on_cancel = on_cancel
        self.cancel_allowed = cancel_allowed
        self.mode = initial_mode
        self.difficulty = initial_difficulty
        self.wild = initial_wild
        self.crusade = initial_crusade
        self.four_fronts = initial_four_fronts
        self.imperial = initial_imperial
        self.player_color = initial_player_color
        self.elephant = initial_elephant
        self.fog = initial_fog
        self.bind("<Return>", lambda _e: self._start())
        self.bind("<Escape>", lambda _e: self._cancel())

        outer = tk.Frame(self, bg=BG, highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill="both", expand=True, padx=24, pady=18)
        inner.grid_columnconfigure(0, weight=1)

        tk.Label(
            inner, text="CRÓNICAS DE AETHELGARD", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            inner, text="Forja tu crónica", bg=BG, fg=GOLD_LIGHT,
            font=(SERIF, 22, "bold"),
        ).grid(row=1, column=0, sticky="w", pady=(2, 4))
        tk.Label(
            inner,
            text=(
                "Cuatro reinos se disputan el Trono de Aethelgard: la Orden del Alba, "
                "la Forja Carmesí, el Pacto de la Espesura y la Legión del Eclipse."
            ),
            bg=BG, fg=MUTED, font=(SERIF, 9, "italic"),
            wraplength=580, justify="left",
        ).grid(row=2, column=0, sticky="ew", pady=(0, 12))

        tk.Frame(inner, bg=BORDER_SOFT, height=1).grid(
            row=3, column=0, sticky="ew", pady=(0, 10),
        )
        tk.Label(
            inner, text="ELIGE TU RIVAL", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).grid(row=4, column=0, sticky="w", pady=(0, 6))

        modes = tk.Frame(inner, bg=BG)
        modes.grid(row=5, column=0, sticky="ew")
        modes.grid_columnconfigure(0, weight=1)
        modes.grid_columnconfigure(1, weight=1)
        self.mode_cards: dict[str, dict] = {}

        definitions = [
            (
                "local", "♚", "Duelo de Reyes",
                "Varias voluntades comparten el tablero en el mismo equipo.",
            ),
            (
                "ai", "☾", "Contra el Oráculo",
                "Enfrenta al Oráculo Umbrío en duelos, cruzada o guerra de 4 frentes.",
            ),
        ]
        for index, (mode, crest, title, desc) in enumerate(definitions):
            frame = tk.Frame(
                modes, bg=PANEL_2, highlightbackground=BORDER, highlightthickness=1,
                cursor="hand2",
            )
            frame.grid(
                row=0, column=index, sticky="nsew",
                padx=(0, 8) if index == 0 else (8, 0),
            )
            crest_label = tk.Label(
                frame, text=crest, bg=PANEL_2, fg=GOLD, font=(SANS, 20),
            )
            crest_label.pack(anchor="w", padx=14, pady=(10, 0))
            title_label = tk.Label(
                frame, text=title, bg=PANEL_2, fg=IVORY,
                font=(SERIF, 11, "bold"),
            )
            title_label.pack(anchor="w", padx=14, pady=(0, 2))
            desc_label = tk.Label(
                frame, text=desc, bg=PANEL_2, fg=MUTED, font=(SANS, 8),
                wraplength=250, justify="left",
            )
            desc_label.pack(anchor="w", padx=14, pady=(0, 10))
            bind_recursive(
                frame, "<Button-1>", lambda _e, m=mode: self._select_mode(m),
            )
            self.mode_cards[mode] = {
                "frame": frame,
                "crest": crest_label,
                "title": title_label,
                "desc": desc_label,
            }

        tk.Label(
            inner, text="TU REINO", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).grid(row=6, column=0, sticky="w", pady=(12, 6))

        factions_bar = tk.Frame(inner, bg=BG)
        factions_bar.grid(row=7, column=0, sticky="ew")
        self.faction_buttons: dict[str, tk.Button] = {}
        for f_color in ALL_COLORS:
            f_info = lore.FACTIONS[f_color]
            btn_text = f"{f_info['crest']} {f_info['name']}"
            btn = tk.Button(
                factions_bar, text=btn_text, bd=0, relief="flat",
                highlightthickness=0, font=(SANS, 8, "bold"),
                padx=11, pady=6, cursor="hand2",
                command=lambda c=f_color: self._select_faction(c),
            )
            btn.pack(side="left", padx=(0, 6))
            self.faction_buttons[f_color] = btn

        self.faction_desc = tk.Label(
            inner, text="", bg=BG, fg=MUTED,
            font=(SERIF, 8, "italic"), wraplength=560, justify="left",
        )
        self.faction_desc.grid(row=8, column=0, sticky="w", pady=(5, 0))

        tk.Label(
            inner, text="CAMPAÑA", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).grid(row=9, column=0, sticky="w", pady=(12, 6))

        campaign = tk.Frame(inner, bg=BG)
        campaign.grid(row=10, column=0, sticky="ew")
        self.campaign_buttons: dict[str, tk.Button] = {}
        for key, label in (
            ("classic", "Clásica"),
            ("imperial", "Imperio 12x12"),
            ("wild", "Tierra salvaje"),
            ("crusade", "Cruzada"),
            ("four_fronts", "4 Frentes"),
        ):
            button = tk.Button(
                campaign, text=label, bd=0, relief="flat", highlightthickness=0,
                font=(SANS, 8, "bold"), padx=12, pady=6, cursor="hand2",
                command=lambda k=key: self._select_campaign_key(k),
            )
            button.pack(side="left", padx=(0, 6))
            self.campaign_buttons[key] = button

        self.campaign_desc = tk.Label(
            inner, text="", bg=BG, fg=MUTED,
            font=(SERIF, 8, "italic"), wraplength=560, justify="left",
        )
        self.campaign_desc.grid(row=11, column=0, sticky="w", pady=(5, 0))

        tk.Label(
            inner, text="REGLAS DE CAMPAÑA", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).grid(row=12, column=0, sticky="w", pady=(12, 6))

        rules = tk.Frame(inner, bg=BG)
        rules.grid(row=13, column=0, sticky="ew")
        self.elephant_btn = tk.Button(
            rules, text="Elefante de guerra", bd=0, relief="flat",
            highlightthickness=0, font=(SANS, 8, "bold"), padx=14, pady=6,
            cursor="hand2", command=self._toggle_elephant,
        )
        self.elephant_btn.pack(side="left", padx=(0, 7))
        self.fog_btn = tk.Button(
            rules, text="Niebla de guerra", bd=0, relief="flat",
            highlightthickness=0, font=(SANS, 8, "bold"), padx=14, pady=6,
            cursor="hand2", command=self._toggle_fog,
        )
        self.fog_btn.pack(side="left", padx=(0, 7))

        self.rules_desc = tk.Label(
            inner, text="", bg=BG, fg=MUTED,
            font=(SERIF, 8, "italic"), wraplength=560, justify="left",
        )
        self.rules_desc.grid(row=14, column=0, sticky="w", pady=(5, 0))

        self.difficulty_frame = tk.Frame(inner, bg=BG)
        self.difficulty_frame.grid(row=15, column=0, sticky="ew", pady=(12, 0))
        self.difficulty_frame.grid_columnconfigure(0, weight=1)
        tk.Label(
            self.difficulty_frame, text="DIFICULTAD DEL ORÁCULO",
            bg=BG, fg=GOLD, font=(SANS, 8, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        pills = tk.Frame(self.difficulty_frame, bg=BG)
        pills.grid(row=1, column=0, sticky="w")
        self.diff_buttons: dict[str, tk.Button] = {}
        for label in ("Escudero", "Caballero", "Archimago"):
            button = tk.Button(
                pills, text=label, bd=0, relief="flat", highlightthickness=0,
                font=(SANS, 8, "bold"), padx=14, pady=6, cursor="hand2",
                command=lambda d=label: self._select_difficulty(d),
            )
            button.pack(side="left", padx=(0, 7))
            self.diff_buttons[label] = button

        self.diff_desc = tk.Label(
            self.difficulty_frame, text="", bg=BG, fg=MUTED,
            font=(SERIF, 8, "italic"), wraplength=560, justify="left",
        )
        self.diff_desc.grid(row=2, column=0, sticky="w", pady=(5, 0))

        footer = tk.Frame(inner, bg=BG)
        footer.grid(row=16, column=0, sticky="ew", pady=(14, 0))
        footer.grid_columnconfigure(0, weight=1)
        if self.cancel_allowed:
            cancel = make_button(footer, "Volver al tablero", self._cancel)
            cancel.grid(row=0, column=0, sticky="w")
        tk.Label(
            footer, text="Tu reino abre la marcha", bg=BG, fg=MUTED_DARK,
            font=(SANS, 7, "italic"),
        ).grid(row=0, column=1, sticky="e", padx=(0, 10))
        start = make_button(footer, "Comenzar la crónica", self._start, accent=True)
        start.grid(row=0, column=2, sticky="e")

        self._select_mode(initial_mode)
        self._select_faction(initial_player_color)
        self._select_difficulty(initial_difficulty)
        self._select_campaign_key(
            "imperial"
            if initial_imperial
            else (
                "four_fronts"
                if initial_four_fronts
                else ("crusade" if initial_crusade else ("wild" if initial_wild else "classic"))
            )
        )
        self._refresh_rule_buttons()
        self._present()

    def _select_faction(self, color: str) -> None:
        self.player_color = color
        for c, btn in self.faction_buttons.items():
            selected = c == color
            accent = FACTION_ACCENT.get(c, GOLD)
            btn.configure(
                bg=accent if selected else PANEL_3,
                fg="#181020" if selected else TEXT,
                activebackground=GOLD_LIGHT if selected else "#342545",
                activeforeground="#181020" if selected else TEXT,
            )
        info = lore.FACTIONS.get(color, lore.FACTIONS[WHITE])
        self.faction_desc.configure(
            text=(
                f"{info['name']} ({info['culture']}) · Soberanos: {info['sovereigns']}.\n"
                f"{info['lore']}"
            )
        )

    def _select_mode(self, mode: str) -> None:
        self.mode = mode
        for key, widgets in self.mode_cards.items():
            selected = key == mode
            widgets["frame"].configure(
                highlightbackground=GOLD_LIGHT if selected else BORDER,
                highlightthickness=2 if selected else 1,
                bg=PANEL_3 if selected else PANEL_2,
            )
            for child in widgets["frame"].winfo_children():
                child.configure(bg=PANEL_3 if selected else PANEL_2)
            widgets["title"].configure(fg=GOLD_LIGHT if selected else IVORY)
            widgets["crest"].configure(
                fg=GOLD_LIGHT if selected else (GOLD if key == "local" else VIOLET),
            )
        ai_mode = mode == "ai"
        for button in self.diff_buttons.values():
            button.configure(
                state="normal" if ai_mode else "disabled",
                cursor="hand2" if ai_mode else "",
            )
        if ai_mode:
            self._select_difficulty(self.difficulty)
        else:
            self.diff_desc.configure(
                text="El duelo local no invoca al Oráculo: todas las voluntades son humanas."
            )
            self._refresh_diff_buttons()

    def _select_difficulty(self, difficulty: str) -> None:
        self.difficulty = difficulty
        self._refresh_diff_buttons()
        if self.mode == "ai":
            self.diff_desc.configure(text=DIFFICULTIES[difficulty]["desc"])

    def _select_campaign_key(self, key: str) -> None:
        self.imperial = key == "imperial"
        self.four_fronts = key == "four_fronts"
        self.crusade = key == "crusade"
        self.wild = key in ("wild", "crusade")
        if self.crusade and self.mode != "ai":
            self._select_mode("ai")
        self._refresh_campaign_buttons()
        if key == "imperial":
            desc = (
                "Gran Tablero Imperial de 12x12 casillas con las 10 nuevas piezas "
                "míticas (Halcón, Elefante, Amazonas, Saltamontes, Noctámbulo, "
                "Centauro, Camello, León, Cebra y Fénix) desplegadas en 3 filas."
            )
        elif key == "four_fronts":
            desc = (
                "Batalla simultánea de los 4 reinos en el mismo tablero (Sur, Oeste, "
                "Norte y Este). Si un monarca cae o queda sin jugadas, su frente se "
                "desmorona."
            )
        elif key == "crusade":
            desc = (
                "Cuatro batallas encadenadas enfrentando a los distintos reinos rivales "
                "con refuerzos míticos dinámicos. Tus sobrevivientes avanzan de etapa."
            )
        elif key == "wild":
            desc = (
                "Ejércitos aleatorios con criaturas míticas y un teatro de guerra con "
                "bosques, ríos, peñascos y ruinas tácticas."
            )
        else:
            desc = (
                "La formación tradicional del ajedrez entre dos reinos, con ascenso a "
                "Veterano al lograr dos bajas en combate."
            )
        self.campaign_desc.configure(text=desc)

    def _refresh_campaign_buttons(self) -> None:
        active_key = (
            "imperial"
            if self.imperial
            else (
                "four_fronts"
                if self.four_fronts
                else ("crusade" if self.crusade else ("wild" if self.wild else "classic"))
            )
        )
        for key, button in self.campaign_buttons.items():
            selected = key == active_key
            button.configure(
                bg=GOLD if selected else PANEL_3,
                fg="#181020" if selected else TEXT,
                activebackground=GOLD_LIGHT if selected else "#342545",
                activeforeground="#181020" if selected else TEXT,
            )

    def _toggle_elephant(self) -> None:
        self.elephant = not self.elephant
        self._refresh_rule_buttons()

    def _toggle_fog(self) -> None:
        self.fog = not self.fog
        self._refresh_rule_buttons()

    def _refresh_rule_buttons(self) -> None:
        for active, button in (
            (self.elephant, self.elephant_btn),
            (self.fog, self.fog_btn),
        ):
            button.configure(
                bg=GOLD if active else PANEL_3,
                fg="#181020" if active else TEXT,
                activebackground=GOLD_LIGHT if active else "#342545",
                activeforeground="#181020" if active else TEXT,
            )
        notes = []
        if self.elephant:
            notes.append(
                "El Elefante de Guerra reemplaza a un alfil y combina Torre + Caballo."
            )
        if self.fog:
            notes.append(
                "La Niebla de Guerra oculta las casillas fuera del alcance de tus piezas."
            )
        self.rules_desc.configure(
            text=" ".join(notes) if notes else "Sin modificadores adicionales."
        )

    def _refresh_diff_buttons(self) -> None:
        for label, button in self.diff_buttons.items():
            selected = label == self.difficulty and self.mode == "ai"
            button.configure(
                bg=GOLD if selected else PANEL_3,
                fg="#181020" if selected else TEXT,
                activebackground=GOLD_LIGHT if selected else "#342545",
                activeforeground="#181020" if selected else TEXT,
                disabledforeground=MUTED_DARK,
            )

    def _start(self) -> None:
        mode = self.mode
        difficulty = self.difficulty
        wild = self.wild
        elephant = self.elephant
        fog = self.fog
        crusade = self.crusade
        four_fronts = self.four_fronts
        player_color = self.player_color
        imperial = self.imperial
        self._close()
        self.on_start(
            mode, difficulty, wild, elephant, fog, crusade,
            four_fronts, player_color, imperial,
        )

    def _cancel(self) -> None:
        self._close()
        if self.on_cancel is not None:
            self.on_cancel()


class PromotionDialog(ModalDialog):
    OPTIONS = [
        (AMAZON, "Amazonas", "Reina + Caballo"),
        (QUEEN, "Dama", "Poder absoluto"),
        (ELEPHANT, "Elefante", "Torre + Caballo"),
        (FALCON, "Halcón", "Alfil + Caballo"),
        (ROOK, "Torre", "Muralla viva"),
        (KNIGHT, "Caballo", "Salto de sombra"),
    ]

    def __init__(
        self,
        master: tk.Misc,
        color: str,
        mover_name: str,
        callback: Callable[[Optional[str]], None],
        on_closed: Optional[Callable[[], None]] = None,
        allowed_kinds: Optional[set[str]] = None,
    ) -> None:
        super().__init__(master, "Altar de coronación", on_closed)
        self.callback = callback
        self.choice: Optional[str] = None
        self.color = color
        self.bind("<Escape>", lambda _e: self._cancel())
        active_options = [
            opt for opt in self.OPTIONS
            if allowed_kinds is None or opt[0] in allowed_kinds
        ]
        if not active_options:
            active_options = self.OPTIONS[1:]
        for index, (kind, _name, _desc) in enumerate(active_options, start=1):
            self.bind(str(index), lambda _e, k=kind: self._choose(k))

        outer = tk.Frame(self, bg=BG, highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(
            inner, text="EL ALTAR DE CORONACIÓN", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            inner, text="Elige un nuevo destino", bg=BG, fg=GOLD_LIGHT,
            font=(SERIF, 20, "bold"),
        ).pack(anchor="w", pady=(2, 4))
        tk.Label(
            inner,
            text=f"{mover_name} alcanza el último escalón. La piedra arde y exige un juramento.",
            bg=BG, fg=MUTED, font=(SERIF, 9, "italic"),
            wraplength=540, justify="left",
        ).pack(anchor="w", pady=(0, 16))

        options = tk.Frame(inner, bg=BG)
        options.pack(fill="x")
        total_opts = len(active_options)
        for index, (kind, name, desc) in enumerate(active_options):
            frame = tk.Frame(
                options, bg=PANEL_2, highlightbackground=BORDER,
                highlightthickness=1, cursor="hand2",
            )
            frame.grid(
                row=0, column=index,
                padx=(0, 8) if index < total_opts - 1 else 0, sticky="nsew",
            )
            options.grid_columnconfigure(index, weight=1)
            glyph_color = FACTION_ACCENT.get(self.color, WHITE_FILL)
            glyph = tk.Label(
                frame, text=PIECE_GLYPHS[kind], bg=PANEL_2, fg=glyph_color,
                font=(GLYPH_FONT, 26),
            )
            glyph.pack(pady=(12, 0))
            glyph_line = tk.Label(
                frame, text=name, bg=PANEL_2, fg=GOLD_LIGHT,
                font=(SERIF, 10, "bold"),
            )
            glyph_line.pack(pady=(2, 0))
            tk.Label(
                frame, text=desc, bg=PANEL_2, fg=MUTED, font=(SANS, 7),
            ).pack(pady=(1, 10))
            bind_recursive(frame, "<Button-1>", lambda _e, k=kind: self._choose(k))
            bind_recursive(
                frame, "<Enter>",
                lambda _e, f=frame: f.configure(
                    highlightbackground=GOLD_LIGHT, highlightthickness=2,
                ),
            )
            bind_recursive(
                frame, "<Leave>",
                lambda _e, f=frame: f.configure(
                    highlightbackground=BORDER, highlightthickness=1,
                ),
            )

        tk.Label(
            inner, text=f"Pulsa 1–{total_opts} o elige con el ratón · Esc para cancelar",
            bg=BG, fg=MUTED_DARK, font=(SANS, 7, "italic"),
        ).pack(anchor="w", pady=(14, 0))
        self._present()

    def _choose(self, kind: str) -> None:
        self.choice = kind
        self._close()
        self.callback(kind)

    def _cancel(self) -> None:
        self._close()
        self.callback(None)


class ConfirmDialog(ModalDialog):
    def __init__(
        self,
        master: tk.Misc,
        title: str,
        message: str,
        confirm_text: str,
        on_confirm: Callable[[], None],
        on_closed: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(master, title, on_closed)
        self.on_confirm = on_confirm
        self.bind("<Escape>", lambda _e: self._cancel())

        outer = tk.Frame(self, bg=BG, highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(
            inner, text="ÚLTIMO AVISO", bg=BG, fg=DANGER,
            font=(SANS, 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            inner, text=title, bg=BG, fg=GOLD_LIGHT,
            font=(SERIF, 18, "bold"),
        ).pack(anchor="w", pady=(2, 6))
        tk.Label(
            inner, text=message, bg=BG, fg=TEXT, font=(SERIF, 10),
            wraplength=420, justify="left",
        ).pack(anchor="w", pady=(0, 16))

        buttons = tk.Frame(inner, bg=BG)
        buttons.pack(fill="x")
        make_button(buttons, "Seguir luchando", self._cancel).pack(side="left")
        make_button(buttons, confirm_text, self._confirm, accent=True).pack(side="right")
        self._present()

    def _confirm(self) -> None:
        self._close()
        self.on_confirm()


class EndDialog(ModalDialog):
    def __init__(
        self,
        master: tk.Misc,
        result: dict,
        game: Game,
        start_time: Optional[float],
        on_new: Callable[[], None],
        on_closed: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(master, "El trono ha hablado", on_closed)
        self.on_new = on_new
        self.bind("<Escape>", lambda _e: self._review())

        title, subtitle, color_key = lore.result_title(result)
        icon = lore.result_icon(result)
        color = FACTION_ACCENT.get(color_key, GOLD)

        outer = tk.Frame(self, bg=BG, highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill="both", expand=True, padx=28, pady=22)

        tk.Label(
            inner, text="EL TRONO HA HABLADO", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).pack(anchor="center")
        tk.Label(
            inner, text=icon, bg=BG, fg=color, font=(SANS, 40),
        ).pack(pady=(2, 0))
        tk.Label(
            inner, text=title, bg=BG, fg=color, font=(SERIF, 24, "bold"),
        ).pack()
        tk.Label(
            inner, text=subtitle, bg=BG, fg=MUTED, font=(SERIF, 10, "italic"),
        ).pack(pady=(2, 12))

        tk.Frame(inner, bg=BORDER_SOFT, height=1).pack(fill="x", pady=(0, 12))
        epilogue = lore.epilogue(result)
        tk.Label(
            inner, text=epilogue.text, bg=BG, fg=TEXT, font=(SERIF, 10),
            wraplength=470, justify="left",
        ).pack(anchor="w")

        stats = tk.Frame(inner, bg=PANEL_2, highlightbackground=BORDER, highlightthickness=1)
        stats.pack(fill="x", pady=(16, 16))
        captures = len([m for m in game.history if m.captured is not None])
        moves = (len(game.history) + 1) // 2
        duration = ""
        if start_time is not None:
            seconds = max(0, int(time.time() - start_time))
            duration = f"{seconds // 60:02d}:{seconds % 60:02d}"
        for col, (label, value) in enumerate((
            ("JUGADAS", str(moves)),
            ("CAÍDOS", str(captures)),
            ("DURACIÓN", duration or "—"),
        )):
            stats.grid_columnconfigure(col, weight=1)
            box = tk.Frame(stats, bg=PANEL_2)
            box.grid(row=0, column=col, sticky="ew", padx=10, pady=10)
            tk.Label(
                box, text=label, bg=PANEL_2, fg=MUTED,
                font=(SANS, 7, "bold"),
            ).pack()
            tk.Label(
                box, text=value, bg=PANEL_2, fg=GOLD_LIGHT,
                font=(SERIF, 14, "bold"),
            ).pack()

        buttons = tk.Frame(inner, bg=BG)
        buttons.pack(fill="x")
        make_button(buttons, "Revisar el tablero", self._review).pack(side="left")
        make_button(buttons, "Nueva crónica", self._new_game, accent=True).pack(side="right")
        self._present()

    def _new_game(self) -> None:
        self._close()
        self.on_new()

    def _review(self) -> None:
        self._close()


class DilemmaDialog(ModalDialog):
    def __init__(
        self,
        master: tk.Misc,
        dilemma: lore.WildDilemma,
        callback: Callable[[lore.WildChoice], None],
        on_closed: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(master, "Suceso de guerra", on_closed)
        self.dilemma = dilemma
        self.callback = callback
        self.chosen: Optional[lore.WildChoice] = None
        self.bind("1", lambda _e: self._choose(0))
        self.bind("2", lambda _e: self._choose(1))
        self.bind("<Escape>", lambda _e: self._choose(0))

        outer = tk.Frame(self, bg=BG, highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(
            inner, text="SUCESO DE GUERRA INTERACTIVO", bg=BG, fg=GOLD,
            font=(SANS, 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            inner, text=dilemma.title, bg=BG, fg=GOLD_LIGHT,
            font=(SERIF, 19, "bold"),
        ).pack(anchor="w", pady=(2, 4))
        tk.Label(
            inner, text=dilemma.prompt, bg=BG, fg=MUTED,
            font=(SERIF, 9, "italic"), wraplength=520, justify="left",
        ).pack(anchor="w", pady=(0, 14))

        cards = tk.Frame(inner, bg=BG)
        cards.pack(fill="x")
        for idx, choice in enumerate(dilemma.options):
            frame = tk.Frame(
                cards, bg=PANEL_2, highlightbackground=BORDER,
                highlightthickness=1, cursor="hand2",
            )
            frame.pack(fill="x", pady=(0, 8))
            tk.Label(
                frame, text=f"OPCIÓN {idx + 1}  ·  {choice.label.upper()}",
                bg=PANEL_2, fg=GOLD_LIGHT, font=(SANS, 8, "bold"),
            ).pack(anchor="w", padx=14, pady=(10, 2))
            tk.Label(
                frame, text=choice.description, bg=PANEL_2, fg=TEXT,
                font=(SERIF, 9), wraplength=480, justify="left",
            ).pack(anchor="w", padx=14, pady=(0, 10))
            bind_recursive(frame, "<Button-1>", lambda _e, i=idx: self._choose(i))
            bind_recursive(
                frame, "<Enter>",
                lambda _e, f=frame: f.configure(
                    highlightbackground=GOLD_LIGHT, highlightthickness=2,
                ),
            )
            bind_recursive(
                frame, "<Leave>",
                lambda _e, f=frame: f.configure(
                    highlightbackground=BORDER, highlightthickness=1,
                ),
            )

        tk.Label(
            inner, text="Pulsa 1 o 2, o haz clic en una decisión",
            bg=BG, fg=MUTED_DARK, font=(SANS, 7, "italic"),
        ).pack(anchor="w", pady=(6, 0))
        self._present()

    def _choose(self, index: int) -> None:
        if self.chosen is not None:
            return
        self.chosen = self.dilemma.options[index]
        choice = self.chosen
        self._close()
        self.callback(choice)

    def _cancel(self) -> None:
        self._choose(0)


class CrusadeInterludeDialog(ModalDialog):
    BOONS = (
        (
            "reinforce",
            "Reclutar vanguardia",
            "Suma 1 unidad mítica de vanguardia y 2 soldados a tu ejército superviviente.",
        ),
        (
            "veteran",
            "Nombrar veteranos",
            "Asciende de inmediato a 2 de tus piezas al rango de Veterano (★).",
        ),
        (
            "elephant",
            "Convocar Elefante de Guerra",
            "Incorpora un Elefante de Guerra (⛨, híbrido Torre + Caballo) a tu ejército.",
        ),
        (
            "mythic",
            "Invocar Campeón Mítico",
            "Recluta un Halcón (✦), León (⚜), Noctámbulo (♘), Centauro (⛉) o Fénix (❂).",
        ),
    )

    def __init__(
        self,
        master: tk.Misc,
        crusade: lore.CrusadeState,
        on_boon: Callable[[str], None],
        on_closed: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(master, "Campamento de la Cruzada", on_closed)
        self.on_boon = on_boon
        self._picked = False
        self.bind("1", lambda _e: self._choose("reinforce"))
        self.bind("2", lambda _e: self._choose("veteran"))
        self.bind("3", lambda _e: self._choose("elephant"))
        self.bind("4", lambda _e: self._choose("mythic"))
        self.bind("<Escape>", lambda _e: self._choose("reinforce"))

        outer = tk.Frame(self, bg=BG, highlightbackground=BORDER, highlightthickness=1)
        outer.pack(fill="both", expand=True, padx=12, pady=12)
        inner = tk.Frame(outer, bg=BG)
        inner.pack(fill="both", expand=True, padx=24, pady=20)

        stage_num = crusade.stage + 1
        f_name = lore.faction_name(crusade.player_color)
        tk.Label(
            inner,
            text=f"VICTORIA EN LA ETAPA {stage_num} DE {crusade.total_stages}",
            bg=BG, fg=GOLD, font=(SANS, 8, "bold"),
        ).pack(anchor="w")
        tk.Label(
            inner, text=f"Campamento de {f_name}", bg=BG, fg=GOLD_LIGHT,
            font=(SERIF, 20, "bold"),
        ).pack(anchor="w", pady=(2, 4))
        survivors = len(crusade.roster)
        veterans = sum(1 for p in crusade.roster if p.veteran)
        tk.Label(
            inner,
            text=(
                f"Han sobrevivido {survivors} piezas ({veterans} con rango Veterano ★). "
                "Antes de marchar hacia el siguiente frente, elige un refuerzo:"
            ),
            bg=BG, fg=MUTED, font=(SERIF, 9, "italic"),
            wraplength=520, justify="left",
        ).pack(anchor="w", pady=(0, 14))

        cards = tk.Frame(inner, bg=BG)
        cards.pack(fill="x")
        for idx, (key, title, desc) in enumerate(self.BOONS, start=1):
            frame = tk.Frame(
                cards, bg=PANEL_2, highlightbackground=BORDER,
                highlightthickness=1, cursor="hand2",
            )
            frame.pack(fill="x", pady=(0, 8))
            tk.Label(
                frame, text=f"{idx}. {title.upper()}",
                bg=PANEL_2, fg=GOLD_LIGHT, font=(SANS, 8, "bold"),
            ).pack(anchor="w", padx=14, pady=(10, 2))
            tk.Label(
                frame, text=desc, bg=PANEL_2, fg=TEXT,
                font=(SERIF, 9), wraplength=480, justify="left",
            ).pack(anchor="w", padx=14, pady=(0, 10))
            bind_recursive(frame, "<Button-1>", lambda _e, k=key: self._choose(k))
            bind_recursive(
                frame, "<Enter>",
                lambda _e, f=frame: f.configure(
                    highlightbackground=GOLD_LIGHT, highlightthickness=2,
                ),
            )
            bind_recursive(
                frame, "<Leave>",
                lambda _e, f=frame: f.configure(
                    highlightbackground=BORDER, highlightthickness=1,
                ),
            )

        tk.Label(
            inner, text="Pulsa 1–3 o haz clic para marchar a la siguiente batalla",
            bg=BG, fg=MUTED_DARK, font=(SANS, 7, "italic"),
        ).pack(anchor="w", pady=(6, 0))
        self._present()

    def _choose(self, boon: str) -> None:
        if self._picked:
            return
        self._picked = True
        self._close()
        self.on_boon(boon)

    def _cancel(self) -> None:
        self._choose("reinforce")
