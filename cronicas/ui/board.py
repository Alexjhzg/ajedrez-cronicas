"""Vista del tablero: geometría, resaltados y dibujo de piezas."""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from ..engine import FILE_LETTERS, Game, Move
from .pieces import create_piece_items
from .theme import (
    BG, DANGER, GOLD, GOLD_DIM, GOLD_LIGHT, GLYPH_FONT, SANS,
    SCENE_PALETTES, TERRAIN_STYLE,
)
from .widgets import rounded_rect


class BoardView(tk.Canvas):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(
            parent, bg=BG, highlightthickness=0, bd=0, takefocus=1,
        )
        self.cell = 70.0
        self.ox = 0.0
        self.oy = 0.0
        self.flipped = False
        self.scene = "classic"
        self.board_size = 8

    def set_scene(self, scene: str) -> None:
        self.scene = scene if scene in SCENE_PALETTES else "classic"

    def reset_flip(self) -> None:
        self.flipped = False

    def toggle_flip(self) -> None:
        self.flipped = not self.flipped

    def display_pos(self, r: int, c: int) -> tuple[int, int]:
        n = self.board_size
        if self.flipped:
            return (n - 1) - r, (n - 1) - c
        return r, c

    def board_pos(self, dr: int, dc: int) -> tuple[int, int]:
        n = self.board_size
        if self.flipped:
            return (n - 1) - dr, (n - 1) - dc
        return dr, dc

    def square_center(self, r: int, c: int) -> tuple[float, float]:
        dr, dc = self.display_pos(r, c)
        return (
            self.ox + (dc + 0.5) * self.cell,
            self.oy + (dr + 0.5) * self.cell,
        )

    def square_at(self, x: float, y: float) -> Optional[tuple[int, int]]:
        if self.cell <= 0:
            return None
        n = self.board_size
        dc = int((x - self.ox) // self.cell)
        dr = int((y - self.oy) // self.cell)
        if 0 <= dr < n and 0 <= dc < n:
            return self.board_pos(dr, dc)
        return None

    def anim_dest(self, anim: Optional[dict]) -> tuple[int, int]:
        if anim is None:
            return (-1, -1)
        to_x, to_y = anim["to"]
        return self.board_pos(
            int((to_y - self.oy) // self.cell),
            int((to_x - self.ox) // self.cell),
        )

    def render(
        self,
        game: Game,
        selected: Optional[tuple[int, int]],
        selected_moves: list[Move],
        anim: Optional[dict],
        visible: Optional[set[tuple[int, int]]] = None,
    ) -> None:
        self.delete("all")
        n = game.size
        self.board_size = n
        width = max(self.winfo_width(), 200)
        height = max(self.winfo_height(), 200)
        size = min(width, height)
        margin = max(30.0, size * 0.055)
        square_size = (size - margin * 2) / n
        board = square_size * n
        self.cell = square_size
        self.ox = (width - board) / 2
        self.oy = (height - board) / 2
        ox, oy, cell = self.ox, self.oy, self.cell
        palette = SCENE_PALETTES.get(self.scene, SCENE_PALETTES["classic"])

        frame_pad = max(10.0, cell * 0.18)
        rounded_rect(
            self, ox - frame_pad + 4, oy - frame_pad + 5,
            ox + board + frame_pad + 4, oy + board + frame_pad + 5,
            9, fill="#08050c", outline="",
        )
        rounded_rect(
            self, ox - frame_pad, oy - frame_pad,
            ox + board + frame_pad, oy + board + frame_pad,
            9, fill=palette["frame"], outline=palette["edge"], width=2,
        )
        self.create_rectangle(
            ox - 5, oy - 5, ox + board + 5, oy + board + 5,
            outline=GOLD_DIM, width=1,
        )
        for cx, cy in (
            (ox - frame_pad + 1, oy - frame_pad + 1),
            (ox + board + frame_pad - 1, oy - frame_pad + 1),
            (ox - frame_pad + 1, oy + board + frame_pad - 1),
            (ox + board + frame_pad - 1, oy + board + frame_pad - 1),
        ):
            r = max(2.2, cell * 0.055)
            self.create_polygon(
                cx, cy - r, cx + r, cy, cx, cy + r, cx - r, cy,
                fill=GOLD_DIM, outline="",
            )

        coord_font = (SANS, -max(8, int(cell * 0.13)))
        for dr in range(n):
            for dc in range(n):
                r, c = self.board_pos(dr, dc)
                x1 = ox + dc * cell
                y1 = oy + dr * cell
                color = palette["light"] if (r + c) % 2 == 0 else palette["dark"]
                self.create_rectangle(
                    x1, y1, x1 + cell + 1, y1 + cell + 1,
                    fill=color, outline=color,
                )
                if dc == 0:
                    rank = str(n - r)
                    self.create_text(
                        ox - frame_pad / 2 - 2, y1 + cell / 2,
                        text=rank, fill=palette["coord"], font=coord_font,
                    )
                    self.create_text(
                        ox + board + frame_pad / 2 + 2, y1 + cell / 2,
                        text=rank, fill=palette["coord_dim"], font=coord_font,
                    )
                if dr == n - 1:
                    letter = FILE_LETTERS[c].upper()
                    self.create_text(
                        x1 + cell / 2, oy + board + frame_pad / 2 + 1,
                        text=letter, fill=palette["coord"], font=coord_font,
                    )
                    self.create_text(
                        x1 + cell / 2, oy - frame_pad / 2 - 1,
                        text=letter, fill=palette["coord_dim"], font=coord_font,
                    )

        self._draw_terrain(game, ox, oy, cell, visible)

        last_move = game.last_move
        if last_move is not None:
            for r, c in ((last_move.fr, last_move.fc), (last_move.tr, last_move.tc)):
                if visible is None or (r, c) in visible:
                    self._highlight_square(r, c, GOLD, 0.16)

        if game.in_check(game.turn):
            king_pos = game.find_king(game.turn)
            if king_pos is not None and (visible is None or king_pos in visible):
                self._highlight_square(king_pos[0], king_pos[1], DANGER, 0.32)
                dr, dc = self.display_pos(*king_pos)
                self.create_rectangle(
                    ox + dc * cell + 1, oy + dr * cell + 1,
                    ox + (dc + 1) * cell - 1, oy + (dr + 1) * cell - 1,
                    outline=DANGER, width=2,
                )

        if selected is not None:
            self._highlight_square(selected[0], selected[1], GOLD_LIGHT, 0.28)
            dr, dc = self.display_pos(*selected)
            self.create_rectangle(
                ox + dc * cell + 1.5, oy + dr * cell + 1.5,
                ox + (dc + 1) * cell - 1.5, oy + (dr + 1) * cell - 1.5,
                outline=GOLD_LIGHT, width=2,
            )

            for move in selected_moves:
                dr, dc = self.display_pos(move.tr, move.tc)
                cx = ox + (dc + 0.5) * cell
                cy = oy + (dr + 0.5) * cell
                if (
                    move.captured is not None
                    or move.is_en_passant
                    or game.grid[move.tr][move.tc] is not None
                ):
                    radius = cell * 0.36
                    self.create_oval(
                        cx - radius, cy - radius, cx + radius, cy + radius,
                        outline=DANGER, width=max(2, int(cell * 0.045)),
                    )
                else:
                    radius = cell * 0.105
                    self.create_oval(
                        cx - radius, cy - radius, cx + radius, cy + radius,
                        fill=GOLD_LIGHT, outline=GOLD, width=1,
                    )

        move_dest = self.anim_dest(anim)
        hide_piece: Optional[tuple[str, int]] = None
        if anim is not None:
            moving = anim["piece"]
            hide_piece = (moving.color, moving.pid)

        for r in range(n):
            for c in range(n):
                if visible is not None and (r, c) not in visible:
                    continue
                piece = game.grid[r][c]
                if piece is None:
                    continue
                if hide_piece is not None and move_dest == (r, c):
                    if (piece.color, piece.pid) == hide_piece:
                        continue
                x, y = self.square_center(r, c)
                create_piece_items(
                    self, x, y, piece, int(cell * 0.72), font=GLYPH_FONT,
                )

        if visible is not None:
            self._draw_fog(visible, ox, oy, cell)

    def _draw_fog(
        self, visible: set[tuple[int, int]], ox: float, oy: float, cell: float,
    ) -> None:
        n = self.board_size
        for r in range(n):
            for c in range(n):
                if (r, c) in visible:
                    continue
                dr, dc = self.display_pos(r, c)
                x1 = ox + dc * cell
                y1 = oy + dr * cell
                self.create_rectangle(
                    x1, y1, x1 + cell + 1, y1 + cell + 1,
                    fill="#0d0914", outline="#1a1226", width=1, stipple="gray75",
                )

    # ------------------------------------------------------------------
    # Terreno de campaña
    # ------------------------------------------------------------------
    def _draw_terrain(
        self,
        game: Game,
        ox: float,
        oy: float,
        cell: float,
        visible: Optional[set[tuple[int, int]]] = None,
    ) -> None:
        for (r, c), kind in game.terrain.items():
            if visible is not None and (r, c) not in visible:
                continue
            dr, dc = self.display_pos(r, c)
            x = ox + dc * cell
            y = oy + dr * cell
            style = TERRAIN_STYLE.get(kind, TERRAIN_STYLE["escombros"])
            self.create_rectangle(
                x, y, x + cell + 1, y + cell + 1,
                fill=style["base"], outline=style["deep"], width=1,
            )
            drawer = getattr(self, f"_terrain_{kind}", self._terrain_escombros)
            drawer(x, y, cell, style)

    def _terrain_bosque(self, x: float, y: float, s: float, style: dict) -> None:
        width = max(1, int(s * 0.03))
        for fx, fy, scale in ((0.30, 0.74, 0.20), (0.63, 0.65, 0.16), (0.47, 0.45, 0.11)):
            cx, base, h = x + fx * s, y + fy * s, scale * s
            self.create_line(
                cx, base, cx, base - h * 0.5,
                fill=style["deep"], width=width,
            )
            self.create_polygon(
                cx, base - h * 1.55,
                cx + h * 0.72, base - h * 0.42,
                cx - h * 0.72, base - h * 0.42,
                fill=style["detail"], outline=style["edge"], width=width,
            )

    def _terrain_rio(self, x: float, y: float, s: float, style: dict) -> None:
        width = max(1, int(s * 0.045))
        for index, fy in enumerate((0.28, 0.52, 0.76)):
            points = (
                x + 0.08 * s, y + fy * s,
                x + 0.32 * s, y + (fy - 0.07) * s,
                x + 0.56 * s, y + (fy + 0.06) * s,
                x + 0.92 * s, y + fy * s,
            )
            self.create_line(
                *points, fill=style["edge"] if index == 1 else style["detail"],
                width=width, smooth=True,
            )

    def _terrain_acantilado(
        self, x: float, y: float, s: float, style: dict,
    ) -> None:
        width = max(1, int(s * 0.03))
        points = (
            x + 0.02 * s, y + 0.90 * s,
            x + 0.10 * s, y + 0.55 * s,
            x + 0.24 * s, y + 0.62 * s,
            x + 0.35 * s, y + 0.28 * s,
            x + 0.50 * s, y + 0.50 * s,
            x + 0.68 * s, y + 0.22 * s,
            x + 0.80 * s, y + 0.48 * s,
            x + 0.98 * s, y + 0.38 * s,
            x + 0.98 * s, y + 0.90 * s,
        )
        self.create_polygon(
            *points, fill=style["detail"], outline=style["edge"], width=width,
        )
        for fy in (0.58, 0.72, 0.84):
            self.create_line(
                x + 0.08 * s, y + fy * s,
                x + 0.92 * s, y + (fy - 0.04) * s,
                fill=style["deep"], width=width,
            )

    def _terrain_penasco(self, x: float, y: float, s: float, style: dict) -> None:
        width = max(1, int(s * 0.03))
        for cx, cy, radius in ((0.34, 0.64, 0.22), (0.62, 0.73, 0.18), (0.55, 0.42, 0.13)):
            px, py, r = x + cx * s, y + cy * s, radius * s
            points = (
                px, py - r, px + r, py - r * 0.2,
                px + r * 0.55, py + r, px - r * 0.55, py + r,
                px - r, py - r * 0.2,
            )
            self.create_polygon(
                *points, fill=style["detail"], outline=style["edge"], width=width,
            )

    def _terrain_ruinas(self, x: float, y: float, s: float, style: dict) -> None:
        width = max(1, int(s * 0.025))
        for fx, fy, w, h in (
            (0.14, 0.48, 0.16, 0.36),
            (0.36, 0.34, 0.15, 0.50),
            (0.58, 0.52, 0.13, 0.32),
            (0.76, 0.41, 0.12, 0.43),
        ):
            self.create_rectangle(
                x + fx * s, y + fy * s,
                x + (fx + w) * s, y + (fy + h) * s,
                fill=style["detail"], outline=style["edge"], width=width,
            )
        self.create_line(
            x + 0.08 * s, y + 0.86 * s, x + 0.94 * s, y + 0.86 * s,
            fill=style["deep"], width=width,
        )
        self.create_line(
            x + 0.44 * s, y + 0.34 * s, x + 0.50 * s, y + 0.62 * s,
            fill=style["deep"], width=width,
        )

    def _terrain_empalizada(
        self, x: float, y: float, s: float, style: dict,
    ) -> None:
        width = max(1, int(s * 0.035))
        for fx in (0.20, 0.40, 0.60, 0.80):
            cx = x + fx * s
            self.create_line(
                cx, y + 0.24 * s, cx, y + 0.82 * s,
                fill=style["detail"], width=width,
            )
            self.create_line(
                cx, y + 0.24 * s, cx - 0.04 * s, y + 0.34 * s,
                fill=style["edge"], width=width,
            )
            self.create_line(
                cx, y + 0.24 * s, cx + 0.04 * s, y + 0.34 * s,
                fill=style["edge"], width=width,
            )
        for fy in (0.46, 0.68):
            self.create_line(
                x + 0.08 * s, y + fy * s, x + 0.92 * s, y + fy * s,
                fill=style["edge"], width=width,
            )

    def _terrain_escombros(
        self, x: float, y: float, s: float, style: dict,
    ) -> None:
        width = max(1, int(s * 0.025))
        for cx, cy, radius in ((0.28, 0.66, 0.15), (0.55, 0.58, 0.18), (0.76, 0.72, 0.12)):
            px, py, r = x + cx * s, y + cy * s, radius * s
            points = (
                px - r, py + r * 0.5, px - r * 0.5, py - r,
                px + r * 0.7, py - r * 0.4, px + r, py + r * 0.7,
            )
            self.create_polygon(
                *points, fill=style["detail"], outline=style["edge"], width=width,
            )

    def _highlight_square(self, r: int, c: int, color: str, density: float) -> None:
        dr, dc = self.display_pos(r, c)
        x1 = self.ox + dc * self.cell
        y1 = self.oy + dr * self.cell
        stipple = "gray25" if density >= 0.25 else "gray12"
        self.create_rectangle(
            x1, y1, x1 + self.cell, y1 + self.cell,
            fill=color, outline="", stipple=stipple,
        )
