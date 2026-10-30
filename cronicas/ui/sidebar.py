"""Panel derecho: personaje, turno, botín y crónica."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from .. import lore
from ..engine import BLACK, PIECE_VALUE, WHITE, Game, Piece
from .pieces import create_piece_items
from .state import ViewState
from .story import StoryLog
from .theme import (
    BG, BORDER, DANGER_SOFT, FACTION_ACCENT, GOLD, GOLD_DIM, GOLD_LIGHT,
    GLYPH_FONT, IVORY, MUTED, MUTED_DARK, PANEL, PIECE_GLYPHS, SANS, SERIF,
    VIOLET,
)
from .widgets import card


class SidebarView(tk.Frame):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, bg=BG, width=396)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self._build_character_card()
        self._build_turn_card()
        self._build_loot_card()
        self._build_story_card()
        tk.Label(
            self, text="La historia se escribe con cada jugada.",
            bg=BG, fg=MUTED_DARK, font=(SERIF, 8, "italic"),
        ).grid(row=4, column=0, sticky="ew", pady=(2, 0))

    def _build_character_card(self) -> None:
        char_card, body = card(self, "PERSONAJE")
        char_card.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        body.grid_columnconfigure(1, weight=1)
        self.char_canvas = tk.Canvas(
            body, width=68, height=68, bg=PANEL, highlightthickness=0,
        )
        self.char_canvas.grid(row=0, column=0, rowspan=4, sticky="n", padx=(0, 11))
        self.char_name = tk.Label(
            body, text="", bg=PANEL, fg=IVORY, font=(SERIF, 11, "bold"),
            anchor="w", justify="left", wraplength=278,
        )
        self.char_name.grid(row=0, column=1, sticky="ew")
        self.char_title = tk.Label(
            body, text="", bg=PANEL, fg=GOLD, font=(SERIF, 8, "italic"),
            anchor="w", justify="left", wraplength=278,
        )
        self.char_title.grid(row=1, column=1, sticky="ew", pady=(1, 1))
        self.char_meta = tk.Label(
            body, text="", bg=PANEL, fg=MUTED, font=(SANS, 7, "bold"),
            anchor="w",
        )
        self.char_meta.grid(row=2, column=1, sticky="ew")
        self.char_bio = tk.Label(
            body, text="", bg=PANEL, fg=MUTED, font=(SANS, 7),
            anchor="w", justify="left", wraplength=278,
        )
        self.char_bio.grid(row=3, column=1, sticky="ew", pady=(3, 0))

    def _build_turn_card(self) -> None:
        turn_card, body = card(self, "EL TURNO")
        turn_card.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        body.grid_columnconfigure(1, weight=1)
        self.turn_crest = tk.Label(
            body, text="☀", bg=PANEL, fg=GOLD_LIGHT,
            font=(SANS, 21), width=2,
        )
        self.turn_crest.grid(row=0, column=0, rowspan=3, sticky="w", padx=(0, 9))
        self.turn_name = tk.Label(
            body, text="Turno del Alba", bg=PANEL, fg=GOLD_LIGHT,
            font=(SERIF, 11, "bold"), anchor="w",
        )
        self.turn_name.grid(row=0, column=1, sticky="ew")
        self.turn_sub = tk.Label(
            body, text="Jugada 1", bg=PANEL, fg=MUTED,
            font=(SANS, 8), anchor="w",
        )
        self.turn_sub.grid(row=1, column=1, sticky="ew", pady=(1, 1))
        self.turn_note = tk.Label(
            body, text="Comienza la batalla", bg=PANEL, fg=GOLD_DIM,
            font=(SANS, 7), anchor="w",
        )
        self.turn_note.grid(row=2, column=1, sticky="ew")

    def _build_loot_card(self) -> None:
        loot_card, body = card(self, "BOTÍN DE GUERRA")
        loot_card.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        body.grid_columnconfigure(1, weight=1)
        self.player_loot_title = tk.Label(
            body, text="TU FRENTE", bg=PANEL, fg=GOLD_DIM,
            font=(SANS, 7, "bold"),
        )
        self.player_loot_title.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.white_loot = tk.Label(
            body, text="—", bg=PANEL, fg=VIOLET,
            font=(GLYPH_FONT, 13), anchor="w",
        )
        self.white_loot.grid(row=0, column=1, sticky="ew", pady=(0, 3))
        self.rival_loot_title = tk.Label(
            body, text="RIVALES", bg=PANEL, fg=GOLD_DIM,
            font=(SANS, 7, "bold"),
        )
        self.rival_loot_title.grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.black_loot = tk.Label(
            body, text="—", bg=PANEL, fg=IVORY,
            font=(GLYPH_FONT, 13), anchor="w",
        )
        self.black_loot.grid(row=1, column=1, sticky="ew")
        self.material_label = tk.Label(
            body, text="Equilibrio", bg=PANEL, fg=GOLD,
            font=(SANS, 7, "bold"), anchor="e",
        )
        self.material_label.grid(
            row=2, column=0, columnspan=2, sticky="e", pady=(3, 0),
        )

    def _build_story_card(self) -> None:
        story_card, body = card(self, "CRÓNICA DE GUERRA")
        story_card.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.story = StoryLog(body)
        self.story.grid(row=0, column=0, sticky="nsew")

    def update(self, state: ViewState) -> None:
        self.update_character(state.game, state.focus_piece)
        self.update_turn(state)
        self.update_loot(state.game)

    def update_character(self, game: Game, piece: Optional[Piece]) -> None:
        if piece is None:
            self._draw_portrait(None)
            self.char_name.configure(text="Ningún personaje")
            self.char_title.configure(text="La crónica aguarda")
            self.char_meta.configure(text="")
            self.char_bio.configure(
                text="Toca una pieza del tablero para conocer su historia."
            )
            return
        pos = lore.piece_on_board(game, piece)
        vet_prefix = "★ " if piece.veteran else ""
        self.char_name.configure(text=f"{vet_prefix}{piece.name}")
        vet_suffix = " · Veterano" if piece.veteran else ""
        self.char_title.configure(text=f"{piece.title}{vet_suffix}")
        kind = lore.KIND_LABEL.get(piece.color, lore.KIND_LABEL[WHITE])[piece.kind]
        faction = lore.faction_name(piece.color)
        self.char_meta.configure(text=f"{kind.upper()}  ·  {faction.upper()}")
        location = (
            "Caído en batalla"
            if pos is None
            else lore.location_label(*pos, game.size)
        )
        self.char_bio.configure(
            text=f"{location}\n{lore.character_bio(piece)}"
        )
        self._draw_portrait(piece)

    def _draw_portrait(self, piece: Optional[Piece]) -> None:
        canvas = self.char_canvas
        canvas.delete("all")
        canvas.create_oval(2, 2, 66, 66, fill="#120d19", outline=BORDER, width=1)
        ring = FACTION_ACCENT.get(piece.color, GOLD_DIM) if piece is not None else GOLD_DIM
        canvas.create_oval(7, 7, 61, 61, outline=ring, width=1)
        if piece is None:
            canvas.create_text(
                34, 34, text="✦", font=(SANS, -20), fill=MUTED, anchor="center",
            )
            return
        create_piece_items(
            canvas, 34, 34, piece, 33, tags=("portrait",), font=GLYPH_FONT,
        )

    def update_turn(self, state: ViewState) -> None:
        game = state.game
        if state.game_over and state.result is not None:
            _title, subtitle, color_key = lore.result_title(state.result)
            self.turn_crest.configure(
                text=lore.result_icon(state.result),
                fg=FACTION_ACCENT.get(color_key, GOLD_LIGHT),
            )
            self.turn_name.configure(text="La crónica ha concluido", fg=GOLD_LIGHT)
            self.turn_sub.configure(text=subtitle, fg=MUTED)
            self.turn_note.configure(text="El trono ha hablado", fg=GOLD_DIM)
            return

        color = game.turn
        faction_info = lore.FACTIONS.get(color, lore.FACTIONS[WHITE])
        crest = faction_info["crest"]
        faction = faction_info["name"]
        accent = FACTION_ACCENT.get(color, GOLD_LIGHT)
        self.turn_crest.configure(text=crest, fg=accent)

        if state.ai_thinking:
            name = "El Oráculo medita…"
            name_color = accent
        else:
            name = f"Turno de {faction}"
            name_color = accent
        self.turn_name.configure(text=name, fg=name_color)

        if game.in_check(color):
            sub = "¡El monarca está en jaque!"
            sub_color = DANGER_SOFT
        elif game.multi_front:
            active_count = len(game.active_colors())
            sub = f"Jugada {game.fullmove} · {active_count} frentes activos"
            sub_color = MUTED
        else:
            sub = f"Jugada {game.fullmove} · {faction}"
            sub_color = MUTED
        self.turn_sub.configure(text=sub, fg=sub_color)
        if state.notation:
            self.turn_note.configure(
                text=f"Última: {state.notation[-1]}", fg=GOLD_DIM,
            )
        else:
            self.turn_note.configure(text="Comienza la batalla", fg=GOLD_DIM)

    def update_loot(self, game: Game) -> None:
        player_c = game.turn_order[0] if game.turn_order else WHITE
        captured = [m.captured for m in game.history if m.captured is not None]
        player_booty = sorted(
            [p for p in captured if p.color != player_c],
            key=lambda p: PIECE_VALUE[p.kind], reverse=True,
        )
        rival_booty = sorted(
            [p for p in captured if p.color == player_c],
            key=lambda p: PIECE_VALUE[p.kind], reverse=True,
        )

        def strip(pieces: list[Piece]) -> str:
            if not pieces:
                return "—"
            shown = pieces[:12]
            text = " ".join(PIECE_GLYPHS[p.kind] for p in shown)
            if len(pieces) > len(shown):
                text += f" +{len(pieces) - len(shown)}"
            return text

        self.white_loot.configure(
            text=strip(player_booty),
            fg=VIOLET if player_booty else MUTED_DARK,
        )
        self.black_loot.configure(
            text=strip(rival_booty),
            fg=IVORY if rival_booty else MUTED_DARK,
        )
        p_score = sum(PIECE_VALUE[p.kind] for p in player_booty)
        r_score = sum(PIECE_VALUE[p.kind] for p in rival_booty)
        advantage = (p_score - r_score) / 100
        if abs(advantage) < 0.5:
            text, color = "Equilibrio", GOLD
        elif advantage > 0:
            short = lore.FACTIONS.get(player_c, lore.FACTIONS[WHITE])["short"].title()
            text, color = f"{short} +{advantage:.1f}".replace(".0", ""), FACTION_ACCENT.get(player_c, GOLD_LIGHT)
        else:
            text, color = f"Rivales +{abs(advantage):.1f}".replace(".0", ""), VIOLET
        self.material_label.configure(text=text, fg=color)
