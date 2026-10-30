"""Modelos de estado compartidos entre el controlador y las vistas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..engine import Game, Piece


@dataclass
class Snapshot:
    game: Game
    story: list
    notation: list[str]
    chapter: int
    ply: int
    focus: Optional[Piece]


@dataclass(frozen=True)
class ViewState:
    game: Game
    focus_piece: Optional[Piece]
    started: bool
    game_over: bool
    result: Optional[dict]
    busy: bool
    ai_thinking: bool
    mode: str
    selected: Optional[tuple[int, int]]
    notation: list[str]
    chapter: int
