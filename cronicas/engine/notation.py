"""Notación algebraica en español (tableros 8x8 y 12x12)."""

from __future__ import annotations

from .constants import FILE_LETTERS, PAWN, PIECE_LETTER_ES
from .model import Move


def algebraic(r: int, c: int, size: int = 8) -> str:
    return f"{FILE_LETTERS[c]}{size - r}"


def move_notation(
    move: Move, check: bool = False, mate: bool = False, size: int = 8,
) -> str:
    if move.castle == "K":
        text = "0-0"
    elif move.castle == "Q":
        text = "0-0-0"
    else:
        piece = move.moved
        dest = algebraic(move.tr, move.tc, size)
        if piece is not None and piece.kind == PAWN:
            text = (FILE_LETTERS[move.fc] + "x" if move.captured else "") + dest
        else:
            letter = PIECE_LETTER_ES.get(piece.kind, "") if piece else ""
            text = letter + ("x" if move.captured else "") + dest
        if move.promotion:
            text += "=" + PIECE_LETTER_ES.get(move.promotion, "")
    return text + ("#" if mate else "+" if check else "")
