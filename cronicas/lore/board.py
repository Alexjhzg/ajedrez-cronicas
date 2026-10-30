"""Composición del tablero (duelo 8x8, Guerra de 4 Frentes e Imperio 12x12)."""

from __future__ import annotations

from typing import Optional

from ..engine import (
    ALL_COLORS, AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FALCON,
    GRASSHOPPER, GREEN, KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, QUEEN,
    RED, ROOK, WHITE, ZEBRA, Game, Piece,
)
from .characters import (
    FACTION_BACK, FACTION_ELEPHANT, FACTION_PAWNS, PIECE_DISPLAY_NAME,
)
from .factions import KIND_LABEL


def create_game(
    elephant: bool = False,
    player_color: str = WHITE,
    enemy_color: str = BLACK,
) -> Game:
    if enemy_color == player_color:
        enemy_color = BLACK if player_color != BLACK else WHITE

    game = Game(turn_order=(player_color, enemy_color))
    pid = 1

    player_back = list(FACTION_BACK.get(player_color, FACTION_BACK[WHITE]))
    enemy_back = list(FACTION_BACK.get(enemy_color, FACTION_BACK[BLACK]))
    if elephant:
        player_back[2] = FACTION_ELEPHANT.get(player_color, FACTION_ELEPHANT[WHITE])
        enemy_back[2] = FACTION_ELEPHANT.get(enemy_color, FACTION_ELEPHANT[BLACK])

    player_pawns = FACTION_PAWNS.get(player_color, FACTION_PAWNS[WHITE])[:8]
    enemy_pawns = FACTION_PAWNS.get(enemy_color, FACTION_PAWNS[BLACK])[:8]

    for col, (kind, name, title) in enumerate(player_back):
        game.place(Piece(player_color, kind, pid, name, title), 7, col)
        pid += 1
    for col, (name, title) in enumerate(player_pawns):
        game.place(Piece(player_color, PAWN, pid, name, title), 6, col)
        pid += 1
    for col, (kind, name, title) in enumerate(enemy_back):
        game.place(Piece(enemy_color, kind, pid, name, title), 0, col)
        pid += 1
    for col, (name, title) in enumerate(enemy_pawns):
        game.place(Piece(enemy_color, PAWN, pid, name, title), 1, col)
        pid += 1

    game.castling[player_color] = {"K": True, "Q": True}
    game.castling[enemy_color] = {"K": True, "Q": True}
    return game


IMPERIAL_ROW_1 = (
    ROOK, NIGHTRIDER, LION, FALCON, QUEEN, KING,
    AMAZON, ELEPHANT, LION, NIGHTRIDER, BISHOP, ROOK,
)
IMPERIAL_ROW_2 = (
    ZEBRA, CAMEL, GRASSHOPPER, PHOENIX, KNIGHT, CENTAUR,
    CENTAUR, KNIGHT, PHOENIX, GRASSHOPPER, CAMEL, ZEBRA,
)

IMPERIAL_ROYAL_NAMES = {
    WHITE: {KING: "Rey Balduino", QUEEN: "Reina Leonor"},
    BLACK: {KING: "Rey Vladimir", QUEEN: "Reina Carmila"},
    RED: {KING: "Rey Leónidas", QUEEN: "Reina Gorgo"},
    GREEN: {KING: "Rey Artur", QUEEN: "Reina Morgana"},
}


def create_imperial_game(
    player_color: str = WHITE,
    enemy_color: str = BLACK,
) -> Game:
    """Crea una batalla en el Gran Tablero Imperial 12x12 con las 10 nuevas piezas."""
    if enemy_color == player_color:
        enemy_color = BLACK if player_color != BLACK else WHITE

    game = Game(turn_order=(player_color, enemy_color), size=12)
    pid = 1

    for color, r_back, r_van, r_pawn in (
        (player_color, 11, 10, 9),
        (enemy_color, 0, 1, 2),
    ):
        royals = IMPERIAL_ROYAL_NAMES.get(color, IMPERIAL_ROYAL_NAMES[WHITE])
        labels_map = KIND_LABEL.get(color, KIND_LABEL[WHITE])

        for col, kind in enumerate(IMPERIAL_ROW_1):
            name = royals.get(kind, PIECE_DISPLAY_NAME[kind])
            title = labels_map[kind]
            game.place(Piece(color, kind, pid, name, title), r_back, col)
            pid += 1

        for col, kind in enumerate(IMPERIAL_ROW_2):
            name = royals.get(kind, PIECE_DISPLAY_NAME[kind])
            title = labels_map[kind]
            game.place(Piece(color, kind, pid, name, title), r_van, col)
            pid += 1

        pawns = FACTION_PAWNS.get(color, FACTION_PAWNS[WHITE])
        for col in range(12):
            name, title = pawns[col % len(pawns)]
            game.place(Piece(color, PAWN, pid, name, title), r_pawn, col)
            pid += 1

    return game


def _front_contingent(
    color: str, elephant: bool = False,
) -> tuple[list[tuple[str, str, str]], list[tuple[str, str]]]:
    """Devuelve 4 oficiales (Torre, Reina, Rey, Alfil/Caballo/Elefante) y 4 peones."""
    back = FACTION_BACK.get(color, FACTION_BACK[WHITE])
    pawns = FACTION_PAWNS.get(color, FACTION_PAWNS[WHITE])
    flank = (
        FACTION_ELEPHANT.get(color, FACTION_ELEPHANT[WHITE])
        if elephant
        else back[1]
    )
    officers = [
        back[0],
        back[3],
        back[4],
        flank,
    ]
    return officers, list(pawns[:4])


def create_four_fronts_game(
    elephant: bool = False,
    player_color: str = WHITE,
) -> Game:
    """Crea una batalla simultánea de 4 reinos en los cuatro puntos cardinales."""
    base_order = list(ALL_COLORS)
    if player_color in base_order:
        idx = base_order.index(player_color)
        ordered = tuple(base_order[idx:] + base_order[:idx])
    else:
        ordered = ALL_COLORS

    south_c, west_c, north_c, east_c = ordered
    front_dirs = {
        south_c: (-1, 0),
        west_c: (0, 1),
        north_c: (1, 0),
        east_c: (0, -1),
    }
    game = Game(turn_order=ordered, front_dirs=front_dirs)

    for r, c in ((0, 0), (0, 7), (7, 0), (7, 7)):
        game.add_terrain("penasco", r, c)
    for r, c in ((1, 1), (1, 6), (6, 1), (6, 6)):
        game.add_terrain("ruinas", r, c)

    pid = 1
    for color, r_off, r_pawn, vertical in (
        (south_c, 7, 6, False),
        (west_c, 0, 1, True),
        (north_c, 0, 1, False),
        (east_c, 7, 6, True),
    ):
        officers, pawns = _front_contingent(color, elephant)
        for idx, (kind, name, title) in enumerate(officers):
            r, c = (2 + idx, r_off) if vertical else (r_off, 2 + idx)
            game.place(Piece(color, kind, pid, name, title), r, c)
            pid += 1
        for idx, (name, title) in enumerate(pawns):
            r, c = (2 + idx, r_pawn) if vertical else (r_pawn, 2 + idx)
            game.place(Piece(color, PAWN, pid, name, title), r, c)
            pid += 1

    return game


def piece_on_board(game: Game, piece: Optional[Piece]) -> Optional[tuple[int, int]]:
    if piece is None:
        return None
    n = game.size
    for r in range(n):
        for c in range(n):
            p = game.grid[r][c]
            if p is not None and p.pid == piece.pid:
                return r, c
    return None
