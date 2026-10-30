"""Modelos inmutables de piezas y movimientos."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Piece:
    color: str
    kind: str
    pid: int
    name: str = ""
    title: str = ""
    kills: int = 0
    veteran: bool = False


@dataclass
class Move:
    fr: int
    fc: int
    tr: int
    tc: int
    promotion: Optional[str] = None
    castle: Optional[str] = None
    is_en_passant: bool = False
    captured: Optional[Piece] = None
    moved: Optional[Piece] = None
    placed: Optional[Piece] = None
    eliminated_factions: tuple[str, ...] = ()
