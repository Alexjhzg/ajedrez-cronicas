"""Constantes compartidas por las reglas y la búsqueda del motor."""

from __future__ import annotations

WHITE = "w"   # Orden del Alba (Dorado / Marfil)
BLACK = "b"   # Legión del Eclipse (Obsidiana / Violeta)
RED = "c"     # Forja Carmesí (Rojo Sangre / Bronce)
GREEN = "v"   # Reino de Avalon (Verde Esmeralda / Jade)

ALL_COLORS = (WHITE, RED, BLACK, GREEN)

# Piezas clásicas
PAWN = "p"
KNIGHT = "n"
BISHOP = "b"
ROOK = "r"
QUEEN = "q"
KING = "k"

# Las 10 piezas del Códice de Hadas / Modo Imperial
FALCON = "h"       # 1. Halcón (Alfil + Caballo)
ELEPHANT = "e"     # 2. Elefante (Torre + Caballo)
AMAZON = "a"       # 3. Amazonas (Reina + Caballo)
GRASSHOPPER = "s"  # 4. Saltamontes (Salto obligatorio sobre 1 pieza y aterriza justo detrás)
NIGHTRIDER = "g"   # 5. Noctámbulo (Saltos repetidos de Caballo en línea recta)
CENTAUR = "u"      # 6. Centauro (Rey sin restricciones reales + Caballo)
CAMEL = "m"        # 7. Camello (Salto extendido 3x1)
LION = "l"         # 8. León (Salta sobre 1 pieza y aterriza en cualquier casilla posterior de la línea)
ZEBRA = "z"        # 9. Cebra (Salto exótico 3x2)
PHOENIX = "f"      # 10. Fénix (1 paso ortogonal o salto diagonal 2x2)

FAIRY_KINDS = (
    FALCON, ELEPHANT, AMAZON, GRASSHOPPER, NIGHTRIDER,
    CENTAUR, CAMEL, LION, ZEBRA, PHOENIX,
)

PIECE_VALUE = {
    PAWN: 100,
    CAMEL: 225,
    ZEBRA: 225,
    GRASSHOPPER: 250,
    PHOENIX: 275,
    KNIGHT: 320,
    BISHOP: 330,
    ROOK: 500,
    NIGHTRIDER: 500,
    CENTAUR: 500,
    FALCON: 750,
    LION: 750,
    ELEPHANT: 850,
    QUEEN: 900,
    AMAZON: 1250,
    KING: 20000,
}

PIECE_LETTER_ES = {
    KING: "R",
    AMAZON: "M",
    QUEEN: "D",
    ELEPHANT: "E",
    FALCON: "H",
    LION: "L",
    ROOK: "T",
    NIGHTRIDER: "N",
    CENTAUR: "U",
    BISHOP: "A",
    KNIGHT: "C",
    PHOENIX: "F",
    GRASSHOPPER: "S",
    CAMEL: "K",
    ZEBRA: "Z",
    PAWN: "",
}

FILE_LETTERS = "abcdefghijkl"

KNIGHT_DELTAS = (
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
)
CAMEL_DELTAS = (
    (-3, -1), (-3, 1), (-1, -3), (-1, 3),
    (1, -3), (1, 3), (3, -1), (3, 1),
)
ZEBRA_DELTAS = (
    (-3, -2), (-3, 2), (-2, -3), (-2, 3),
    (2, -3), (2, 3), (3, -2), (3, 2),
)
KING_DELTAS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
)
BISHOP_DIRS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
ROOK_DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))
QUEEN_DIRS = BISHOP_DIRS + ROOK_DIRS
ALFIL_DELTAS = ((-2, -2), (-2, 2), (2, -2), (2, 2))
ELEPHANT_DELTAS = ALFIL_DELTAS

IMPASSABLE_TERRAIN = frozenset({
    "acantilado", "penasco", "empalizada", "escombros",
})
PASSABLE_TERRAIN = frozenset({"bosque", "rio", "ruinas"})
VISION_BLOCKING_TERRAIN = frozenset({
    "bosque", "acantilado", "penasco", "empalizada", "escombros",
})
FORTIFIED_TERRAIN = frozenset({"ruinas"})
SLOW_TERRAIN = frozenset({"rio"})


def other(color: str) -> str:
    return BLACK if color == WHITE else WHITE
