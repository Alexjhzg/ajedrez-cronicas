"""Paleta, tipografía y configuración visual compartida (4 reinos)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ..engine import (
    AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FALCON, GRASSHOPPER,
    GREEN, KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, QUEEN, RED, ROOK,
    WHITE, ZEBRA,
)

BG = "#0f0b14"
PANEL = "#171120"
PANEL_2 = "#1d1527"
PANEL_3 = "#261b33"
BORDER = "#3a2a4b"
BORDER_SOFT = "#2b2038"
GOLD = "#c8a35f"
GOLD_LIGHT = "#ecd398"
GOLD_DIM = "#8b744a"
IVORY = "#f1e3c6"
TEXT = "#e6d8c2"
MUTED = "#97869f"
MUTED_DARK = "#6b5b78"
VIOLET = "#b28ce0"
VIOLET_DARK = "#6f4e95"
CRIMSON = "#e06d5b"
CRIMSON_DARK = "#8b3328"
EMERALD = "#6ac48a"
EMERALD_DARK = "#2d6e46"
DANGER = "#d96a5f"
DANGER_SOFT = "#e6a094"
SQUARE_LIGHT = "#b79a6f"
SQUARE_DARK = "#4d3346"
WHITE_FILL = "#f4e7ca"
WHITE_LINE = "#2b1b14"
BLACK_FILL = "#38204d"
BLACK_LINE = "#d7b170"
RED_FILL = "#8c2620"
RED_LINE = "#f2c17d"
GREEN_FILL = "#1f5938"
GREEN_LINE = "#c7e8ac"
SHADOW = "#08050c"

FACTION_ACCENT = {
    WHITE: GOLD_LIGHT,
    BLACK: VIOLET,
    RED: CRIMSON,
    GREEN: EMERALD,
}

SCENE_PALETTES = {
    "classic": {
        "light": SQUARE_LIGHT, "dark": SQUARE_DARK,
        "frame": PANEL_2, "edge": "#4b3560",
        "coord": GOLD_DIM, "coord_dim": "#5b4967",
    },
    "bosque": {
        "light": "#a8b58a", "dark": "#405442",
        "frame": "#172019", "edge": "#617a52",
        "coord": "#a3b47d", "coord_dim": "#64745c",
    },
    "rio": {
        "light": "#aeb8b3", "dark": "#465760",
        "frame": "#172026", "edge": "#63808c",
        "coord": "#9fb7bd", "coord_dim": "#5c7178",
    },
    "acantilado": {
        "light": "#c1a486", "dark": "#5b4140",
        "frame": "#24181a", "edge": "#8a6657",
        "coord": "#c0a489", "coord_dim": "#76605a",
    },
    "ruinas": {
        "light": "#b6a990", "dark": "#514355",
        "frame": "#221b28", "edge": "#786782",
        "coord": "#b1a3bf", "coord_dim": "#6d6074",
    },
    "paso": {
        "light": "#bda88b", "dark": "#514c4a",
        "frame": "#1f1d1c", "edge": "#7d6d5f",
        "coord": "#b8a088", "coord_dim": "#6d625a",
    },
    "imperial": {
        "light": "#c8ad7f", "dark": "#432c47",
        "frame": "#1a1124", "edge": "#9c7b44",
        "coord": "#d8b778", "coord_dim": "#705b7a",
    },
}

TERRAIN_STYLE = {
    "bosque": {
        "base": "#253b27", "edge": "#7fa86a",
        "detail": "#4e7c4c", "deep": "#172719",
    },
    "rio": {
        "base": "#1e3a4c", "edge": "#78b5cc",
        "detail": "#3c6c82", "deep": "#142733",
    },
    "acantilado": {
        "base": "#3f2e2b", "edge": "#a78472",
        "detail": "#6a4f49", "deep": "#271b19",
    },
    "penasco": {
        "base": "#3b3538", "edge": "#9e939a",
        "detail": "#665c62", "deep": "#241f22",
    },
    "ruinas": {
        "base": "#4f4656", "edge": "#9a839f",
        "detail": "#6d5d73", "deep": "#332d38",
    },
    "empalizada": {
        "base": "#4b3627", "edge": "#b28858",
        "detail": "#755038", "deep": "#2f2118",
    },
    "escombros": {
        "base": "#4a4440", "edge": "#9b8d7b",
        "detail": "#6b6055", "deep": "#302c29",
    },
}

SERIF = "Georgia"
SANS = "DejaVu Sans"
GLYPH_FONT = "DejaVu Sans"

PIECE_GLYPHS = {
    KING: "♚",
    QUEEN: "♛",
    ROOK: "♜",
    BISHOP: "♝",
    ELEPHANT: "⛨",
    FALCON: "✦",
    AMAZON: "♕",
    GRASSHOPPER: "☥",
    NIGHTRIDER: "♘",
    CENTAUR: "⛉",
    CAMEL: "◈",
    LION: "⚜",
    ZEBRA: "❖",
    PHOENIX: "❂",
    KNIGHT: "♞",
    PAWN: "♟",
}

CARDS = {
    WHITE: (WHITE_FILL, WHITE_LINE),
    BLACK: (BLACK_FILL, BLACK_LINE),
    RED: (RED_FILL, RED_LINE),
    GREEN: (GREEN_FILL, GREEN_LINE),
}

DIFFICULTIES = {
    "Escudero": {
        "depth": 1,
        "randomness": 0.45,
        "time": 0.8,
        "desc": "Movimientos imprevisibles. Ideal para aprender el arte de la guerra.",
    },
    "Caballero": {
        "depth": 2,
        "randomness": 0.12,
        "time": 2.0,
        "desc": "Un rival paciente y táctico. Cada error se paga con acero.",
    },
    "Archimago": {
        "depth": 3,
        "randomness": 0.0,
        "time": 4.0,
        "desc": "Lee el porvenir. Pocos han visto amanecer después de enfrentarlo.",
    },
}


def configure_styles(root: tk.Misc) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "Dark.Vertical.TScrollbar",
        background=PANEL_3,
        troughcolor=PANEL,
        bordercolor=PANEL,
        arrowcolor=GOLD_DIM,
        darkcolor=PANEL_3,
        lightcolor=PANEL_3,
        width=8,
    )
    style.map(
        "Dark.Vertical.TScrollbar",
        background=[("active", "#3b2b4d")],
    )
