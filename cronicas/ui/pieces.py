"""Dibujo de piezas con contorno y sombra sobre un canvas."""

from __future__ import annotations

import tkinter as tk

from ..engine import WHITE, Piece
from .theme import (
    CARDS, FACTION_ACCENT, GOLD_LIGHT, GLYPH_FONT, PIECE_GLYPHS, SANS, SHADOW,
)


def create_piece_items(
    canvas: tk.Canvas,
    x: float,
    y: float,
    piece: Piece,
    size: int,
    tags=("piece",),
    font: str = GLYPH_FONT,
) -> list[tuple[int, float, float]]:
    glyph = PIECE_GLYPHS[piece.kind]
    fill, line = CARDS.get(piece.color, CARDS[WHITE])
    text_font = (font, -max(10, size))
    outline_off = max(1, int(size * 0.035))
    items: list[tuple[int, float, float]] = []

    shadow = canvas.create_text(
        x + outline_off * 0.6, y + outline_off * 1.5,
        text=glyph, font=text_font, fill=SHADOW, anchor="center",
        tags=tags,
    )
    items.append((shadow, outline_off * 0.6, outline_off * 1.5))

    offsets = [
        (-outline_off, 0), (outline_off, 0), (0, -outline_off), (0, outline_off),
        (-outline_off, -outline_off), (outline_off, -outline_off),
        (-outline_off, outline_off), (outline_off, outline_off),
    ]
    for dx, dy in offsets:
        item = canvas.create_text(
            x + dx, y + dy, text=glyph, font=text_font,
            fill=line, anchor="center", tags=tags,
        )
        items.append((item, dx, dy))

    body = canvas.create_text(
        x, y, text=glyph, font=text_font, fill=fill,
        anchor="center", tags=tags,
    )
    items.append((body, 0, 0))

    if piece.veteran:
        star_dx = size * 0.34
        star_dy = -size * 0.32
        star_font = (SANS, -max(8, int(size * 0.28)), "bold")
        star_color = FACTION_ACCENT.get(piece.color, GOLD_LIGHT)
        star_shadow = canvas.create_text(
            x + star_dx + 1, y + star_dy + 1,
            text="★", font=star_font, fill=SHADOW, anchor="center",
            tags=tags,
        )
        items.append((star_shadow, star_dx + 1, star_dy + 1))
        star = canvas.create_text(
            x + star_dx, y + star_dy,
            text="★", font=star_font, fill=star_color, anchor="center",
            tags=tags,
        )
        items.append((star, star_dx, star_dy))
    return items
