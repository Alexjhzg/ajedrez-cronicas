"""Curvas de movimiento y efectos de ataque para cada tipo de pieza."""

from __future__ import annotations

import math
import tkinter as tk

from ..engine import (
    AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FALCON, GRASSHOPPER,
    KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, QUEEN, ROOK, WHITE, ZEBRA,
    Piece,
)
from .pieces import create_piece_items
from .theme import DANGER, FACTION_ACCENT, GOLD_LIGHT, GLYPH_FONT, IVORY

ACCENT = FACTION_ACCENT
DUST = "#a9845b"
STONE = "#b7a189"

FRAMES = {
    PAWN: 16,
    KNIGHT: 22,
    BISHOP: 20,
    ELEPHANT: 22,
    FALCON: 21,
    AMAZON: 22,
    GRASSHOPPER: 20,
    NIGHTRIDER: 24,
    CENTAUR: 20,
    CAMEL: 22,
    LION: 22,
    ZEBRA: 22,
    PHOENIX: 20,
    ROOK: 18,
    QUEEN: 20,
    KING: 17,
}

IMPACT_AT = {
    PAWN: 0.58,
    KNIGHT: 0.78,
    BISHOP: 0.64,
    ELEPHANT: 0.74,
    FALCON: 0.72,
    AMAZON: 0.70,
    GRASSHOPPER: 0.76,
    NIGHTRIDER: 0.78,
    CENTAUR: 0.72,
    CAMEL: 0.78,
    LION: 0.74,
    ZEBRA: 0.78,
    PHOENIX: 0.70,
    ROOK: 0.68,
    QUEEN: 0.66,
    KING: 0.62,
}


def frames_for(kind: str) -> int:
    return FRAMES.get(kind, 18)


def impact_at(kind: str) -> float:
    return IMPACT_AT.get(kind, 0.66)


def _ease_out(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


def motion_point(
    kind: str,
    t: float,
    start: tuple[float, float],
    end: tuple[float, float],
    cell: float,
) -> tuple[float, float]:
    fx, fy = start
    tx, ty = end
    impact = impact_at(kind)
    progress = min(1.0, max(0.0, t / impact))
    eased = _ease_out(progress)
    x = fx + (tx - fx) * eased
    y = fy + (ty - fy) * eased
    dx = tx - fx
    dy = ty - fy

    if kind in (KNIGHT, NIGHTRIDER, CAMEL, ZEBRA, GRASSHOPPER):
        y -= math.sin(math.pi * progress) * cell * 0.56
    elif kind in (ELEPHANT, FALCON, LION, CENTAUR, PHOENIX):
        y -= math.sin(math.pi * progress) * cell * 0.42
    elif kind == BISHOP:
        distance = math.hypot(dx, dy)
        if distance:
            sway = math.sin(math.pi * progress) * cell * 0.055
            x += (-dy / distance) * sway
            y += (dx / distance) * sway
    elif kind in (QUEEN, AMAZON):
        y -= math.sin(math.pi * progress) * cell * 0.13
    elif kind == KING:
        y -= math.sin(math.pi * progress) * cell * 0.055
    elif kind == PAWN:
        y -= math.sin(math.pi * progress) * cell * 0.07

    if t > impact:
        settle = min(1.0, (t - impact) / max(0.001, 1.0 - impact))
        if kind in (ROOK, ELEPHANT, LION, CENTAUR):
            x += math.sin(settle * math.pi * 7) * (1.0 - settle) * cell * 0.022
        elif kind == KING:
            y -= math.sin(settle * math.pi) * cell * 0.02

    return x, y


class TrailEffect:
    def __init__(
        self,
        canvas: tk.Canvas,
        kind: str,
        side: str,
        cell: float,
        tags: tuple[str, ...] = ("anim", "anim_trail"),
    ) -> None:
        self.canvas = canvas
        self.kind = kind
        self.cell = cell
        self.impact = impact_at(kind)
        magical = kind in (BISHOP, QUEEN, KING)
        color = ACCENT.get(side, GOLD_LIGHT) if magical else DUST
        count = 2 if kind == PAWN else 3
        sizes = (0.052, 0.039, 0.027)
        self.items: list[int] = []
        for index in range(count):
            item = canvas.create_oval(
                0, 0, 0, 0, fill=color, outline="",
                stipple="" if index == 0 else ("gray50" if index == 1 else "gray25"),
                state="hidden", tags=tags,
            )
            self.items.append(item)
        self.sizes = [cell * size for size in sizes[:count]]

    def update(
        self,
        t: float,
        start: tuple[float, float],
        end: tuple[float, float],
    ) -> None:
        if t <= 0 or t >= self.impact:
            for item in self.items:
                self.canvas.itemconfigure(item, state="hidden")
            return
        for index, item in enumerate(self.items):
            lag = t - 0.075 * (index + 1)
            if lag <= 0 or lag >= self.impact:
                self.canvas.itemconfigure(item, state="hidden")
                continue
            x, y = motion_point(self.kind, lag, start, end, self.cell)
            if self.kind in (PAWN, KNIGHT, ELEPHANT, ROOK):
                progress = min(1.0, lag / self.impact)
                eased = _ease_out(progress)
                y = start[1] + (end[1] - start[1]) * eased
            progress = min(1.0, lag / self.impact)
            radius = self.sizes[index] * (1.0 - progress * 0.3)
            self.canvas.coords(
                item, x - radius, y - radius, x + radius, y + radius,
            )
            self.canvas.itemconfigure(item, state="normal")


class VictimEffect:
    def __init__(
        self,
        canvas: tk.Canvas,
        piece: Piece,
        x: float,
        y: float,
        cell: float,
        tags: tuple[str, ...] = ("anim", "anim_victim"),
    ) -> None:
        self.canvas = canvas
        self.x = x
        self.y = y
        self.cell = cell
        self.size = max(10, int(cell * 0.72))
        self.items = create_piece_items(
            canvas, x, y, piece, self.size, tags=tags, font=GLYPH_FONT,
        )

    def update(
        self,
        progress: float,
        push: tuple[float, float],
        cell: float,
    ) -> None:
        progress = min(1.0, max(0.0, progress))
        if progress <= 0:
            return
        scale = max(0.58, 1.0 - progress * 0.42)
        travel = cell * 0.27 * progress
        gravity = cell * 0.2 * progress * progress
        cx = self.x + push[0] * travel
        cy = self.y + push[1] * travel + gravity
        font_size = max(8, int(self.size * scale))
        stipple = ""
        if progress >= 0.74:
            stipple = "gray25"
        elif progress >= 0.46:
            stipple = "gray50"
        for item, dx, dy in self.items:
            self.canvas.coords(
                item, cx + dx * scale, cy + dy * scale,
            )
            self.canvas.itemconfigure(
                item, font=(GLYPH_FONT, -font_size), stipple=stipple,
            )
        if progress >= 0.9:
            for item, _dx, _dy in self.items:
                self.canvas.itemconfigure(item, state="hidden")


class ImpactEffect:
    def __init__(
        self,
        canvas: tk.Canvas,
        kind: str,
        side: str,
        x: float,
        y: float,
        cell: float,
        tags: tuple[str, ...] = ("anim", "anim_fx"),
    ) -> None:
        self.canvas = canvas
        self.kind = kind
        self.side = side
        self.x = x
        self.y = y
        self.cell = cell
        self.accent = ACCENT.get(side, GOLD_LIGHT)
        self.tags = tags
        self.specs: list[dict] = []
        self._build()

    def _spec(
        self,
        item: int,
        start: tuple[float, ...],
        end: tuple[float, ...],
        width_start: float = 0.0,
        width_end: float = 0.0,
        delay: float = 0.0,
    ) -> None:
        self.specs.append({
            "item": item,
            "start": start,
            "end": end,
            "width_start": width_start,
            "width_end": width_end,
            "delay": delay,
        })

    def _line(
        self,
        angle_a: float,
        radius_a: float,
        angle_b: float,
        radius_b: float,
        color: str,
        width_start: float,
        width_end: float,
        delay: float = 0.0,
    ) -> None:
        start = (
            self.x + math.cos(angle_a) * radius_a,
            self.y + math.sin(angle_a) * radius_a,
            self.x + math.cos(angle_b) * radius_b * 0.08,
            self.y + math.sin(angle_b) * radius_b * 0.08,
        )
        end = (
            self.x + math.cos(angle_a) * radius_a,
            self.y + math.sin(angle_a) * radius_a,
            self.x + math.cos(angle_b) * radius_b,
            self.y + math.sin(angle_b) * radius_b,
        )
        item = self.canvas.create_line(
            *start, fill=color, width=max(1.0, width_end),
            capstyle=tk.ROUND, state="hidden", tags=self.tags,
        )
        self._spec(item, start, end, width_start, width_end, delay)

    def _ring(
        self,
        radius_start: float,
        radius_end: float,
        color: str,
        width_start: float,
        width_end: float,
        delay: float = 0.0,
    ) -> None:
        cx, cy = self.x, self.y
        start = (
            cx - radius_start, cy - radius_start,
            cx + radius_start, cy + radius_start,
        )
        end = (
            cx - radius_end, cy - radius_end,
            cx + radius_end, cy + radius_end,
        )
        item = self.canvas.create_oval(
            *start, outline=color, width=max(1.0, width_start),
            state="hidden", tags=self.tags,
        )
        self._spec(item, start, end, width_start, width_end, delay)

    def _rect(
        self,
        half_start: float,
        half_end: float,
        color: str,
        width_start: float,
        width_end: float,
        delay: float = 0.0,
    ) -> None:
        cx, cy = self.x, self.y
        start = (
            cx - half_start, cy - half_start,
            cx + half_start, cy + half_start,
        )
        end = (
            cx - half_end, cy - half_end,
            cx + half_end, cy + half_end,
        )
        item = self.canvas.create_rectangle(
            *start, outline=color, width=max(1.0, width_start),
            state="hidden", tags=self.tags,
        )
        self._spec(item, start, end, width_start, width_end, delay)

    def _orb(
        self,
        angle: float,
        distance_start: float,
        distance_end: float,
        radius_start: float,
        radius_end: float,
        color: str,
        delay: float = 0.0,
    ) -> None:
        cx = self.x + math.cos(angle) * distance_start
        cy = self.y + math.sin(angle) * distance_start
        ex = self.x + math.cos(angle) * distance_end
        ey = self.y + math.sin(angle) * distance_end
        start = (
            cx - radius_start, cy - radius_start,
            cx + radius_start, cy + radius_start,
        )
        end = (
            ex - radius_end, ey - radius_end,
            ex + radius_end, ey + radius_end,
        )
        item = self.canvas.create_oval(
            *start, fill=color, outline="", state="hidden", tags=self.tags,
        )
        self._spec(item, start, end, delay=delay)

    def _flash(self, radius_start: float, radius_end: float) -> None:
        cx, cy = self.x, self.y
        start = (
            cx - radius_start, cy - radius_start,
            cx + radius_start, cy + radius_start,
        )
        end = (
            cx - radius_end, cy - radius_end,
            cx + radius_end, cy + radius_end,
        )
        item = self.canvas.create_oval(
            *start, fill=DANGER, outline="", state="hidden", tags=self.tags,
        )
        self._spec(item, start, end)

    def _build(self) -> None:
        cell = self.cell
        if self.kind == PAWN:
            self._flash(cell * 0.14, cell * 0.035)
            self._line(
                math.radians(45), cell * 0.03,
                math.radians(225), cell * 0.33,
                DANGER, cell * 0.05, cell * 0.006,
            )
            self._line(
                math.radians(135), cell * 0.03,
                math.radians(315), cell * 0.27,
                IVORY, cell * 0.032, cell * 0.005, 0.04,
            )
            for index, angle in enumerate((0, 90, 180, 270)):
                self._orb(
                    math.radians(angle), cell * 0.08, cell * 0.31,
                    cell * 0.035, cell * 0.006, self.accent,
                    0.08 + index * 0.02,
                )
        elif self.kind == KNIGHT:
            self._flash(cell * 0.21, cell * 0.05)
            self._ring(cell * 0.05, cell * 0.43, DANGER, cell * 0.06, cell * 0.008)
            self._ring(cell * 0.08, cell * 0.31, self.accent, cell * 0.035, cell * 0.005, 0.06)
            for index in range(8):
                angle = math.radians(index * 45 + 22.5)
                self._line(
                    angle, cell * 0.1, angle, cell * 0.37,
                    DUST if index % 2 else self.accent,
                    cell * 0.035, cell * 0.006, index * 0.008,
                )
            for index, angle in enumerate((205, 240, 275, 310, 345, 25)):
                self._orb(
                    math.radians(angle), cell * 0.14, cell * 0.44,
                    cell * 0.052, cell * 0.012, DUST,
                    0.07 + index * 0.014,
                )
        elif self.kind == BISHOP:
            self._flash(cell * 0.18, cell * 0.04)
            for index, angle in enumerate((45, 135, 225, 315)):
                radians = math.radians(angle)
                self._line(
                    radians, cell * 0.04, radians, cell * 0.54,
                    self.accent, cell * 0.03, cell * 0.004,
                    index * 0.012,
                )
                self._line(
                    radians, cell * 0.12, radians, cell * 0.31,
                    IVORY, cell * 0.018, cell * 0.003,
                    0.06 + index * 0.012,
                )
                self._orb(
                    radians, cell * 0.14, cell * 0.45,
                    cell * 0.028, cell * 0.005, self.accent,
                    0.12 + index * 0.02,
                )
            self._ring(cell * 0.08, cell * 0.36, self.accent, cell * 0.035, cell * 0.005)
            self._ring(cell * 0.14, cell * 0.25, IVORY, cell * 0.02, cell * 0.004, 0.05)
        elif self.kind in (ROOK, ELEPHANT):
            self._flash(cell * 0.23, cell * 0.055)
            self._rect(cell * 0.1, cell * 0.47, DANGER, cell * 0.06, cell * 0.008)
            self._ring(cell * 0.05, cell * 0.34, STONE, cell * 0.03, cell * 0.005, 0.03)
            for index, angle in enumerate((45, 135, 225, 315)):
                radians = math.radians(angle)
                self._line(
                    radians, cell * 0.12, radians, cell * 0.39,
                    STONE if index % 2 else DANGER,
                    cell * 0.034, cell * 0.005, 0.03 + index * 0.012,
                )
            for index, angle in enumerate((20, 65, 115, 160, 205, 250, 295, 340)):
                self._orb(
                    math.radians(angle), cell * 0.13, cell * 0.44,
                    cell * 0.052, cell * 0.012,
                    DUST if index % 2 else STONE,
                    0.06 + index * 0.012,
                )
        elif self.kind == QUEEN:
            self._flash(cell * 0.24, cell * 0.055)
            for index in range(8):
                angle = math.radians(index * 45)
                length = cell * (0.56 if index % 2 == 0 else 0.44)
                self._line(
                    angle, cell * 0.05, angle, length,
                    self.accent if index % 2 == 0 else IVORY,
                    cell * 0.03, cell * 0.004, index * 0.009,
                )
                self._orb(
                    angle, cell * 0.14, cell * 0.48,
                    cell * 0.026, cell * 0.005,
                    self.accent if index % 2 == 0 else IVORY,
                    0.12 + index * 0.012,
                )
            self._ring(cell * 0.08, cell * 0.41, self.accent, cell * 0.04, cell * 0.006)
            self._ring(cell * 0.15, cell * 0.28, IVORY, cell * 0.02, cell * 0.004, 0.06)
        else:
            self._flash(cell * 0.2, cell * 0.05)
            self._ring(cell * 0.07, cell * 0.43, GOLD_LIGHT, cell * 0.045, cell * 0.006)
            self._ring(cell * 0.14, cell * 0.29, IVORY, cell * 0.022, cell * 0.004, 0.06)
            crown_angles = (-150, -120, -90, -60, -30)
            for index, angle in enumerate(crown_angles):
                radians = math.radians(angle)
                length = cell * (0.44 if index == 2 else 0.37)
                self._line(
                    radians, cell * 0.08, radians, length,
                    GOLD_LIGHT, cell * 0.026, cell * 0.004, index * 0.01,
                )
                self._orb(
                    radians, cell * 0.13, cell * 0.41,
                    cell * 0.04, cell * 0.008, IVORY,
                    0.12 + index * 0.015,
                )

    def update(self, progress: float) -> None:
        progress = min(1.0, max(0.0, progress))
        for spec in self.specs:
            delay = spec["delay"]
            local = 0.0 if progress <= delay else min(
                1.0, (progress - delay) / max(0.001, 1.0 - delay),
            )
            item = spec["item"]
            if local <= 0:
                self.canvas.itemconfigure(item, state="hidden")
                continue
            coords = [
                start + (end - start) * local
                for start, end in zip(spec["start"], spec["end"])
            ]
            self.canvas.coords(item, *coords)
            width_start = spec["width_start"]
            width_end = spec["width_end"]
            if width_start or width_end:
                width = width_start + (width_end - width_start) * local
                self.canvas.itemconfigure(item, width=max(1.0, width))
            stipple = ""
            if local >= 0.82:
                stipple = "gray12"
            elif local >= 0.56:
                stipple = "gray25"
            elif local >= 0.34:
                stipple = "gray50"
            self.canvas.itemconfigure(
                item, state="normal", stipple=stipple,
            )
