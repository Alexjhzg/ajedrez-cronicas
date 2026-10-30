"""Nombres y coordenadas de las casillas del reino (8x8 y 12x12)."""

from __future__ import annotations

from ..engine import algebraic

FILES = [
    "el Valle", "el Bosque", "el Río", "la Cañada",
    "la Colina", "el Puente", "las Ruinas", "el Torreón",
    "la Ciudadela", "el Santuario", "el Desfiladero", "la Cumbre",
]
RANKS = [
    "del Alba", "de los Susurros", "de las Cenizas", "del Cuervo",
    "del Dragón", "de la Niebla", "de las Estrellas", "del Trono",
    "del Fénix", "de los Colosos", "de los Antiguos", "del Imperio",
]


def square_name(r: int, c: int, size: int = 8) -> str:
    f_idx = max(0, min(len(FILES) - 1, c))
    r_idx = max(0, min(len(RANKS) - 1, size - 1 - r))
    return f"{FILES[f_idx]} {RANKS[r_idx]}"


def location_label(r: int, c: int, size: int = 8) -> str:
    return f"{square_name(r, c, size)} · {algebraic(r, c, size).upper()}"
