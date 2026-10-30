"""Estado y reglas completas de una partida (tableros 8x8 y 12x12, 2 o 4 frentes)."""

from __future__ import annotations

from typing import Optional

from .constants import (
    ALFIL_DELTAS, ALL_COLORS, AMAZON, BISHOP, BISHOP_DIRS, BLACK, CAMEL,
    CAMEL_DELTAS, CENTAUR, ELEPHANT, FALCON, FORTIFIED_TERRAIN, GRASSHOPPER,
    GREEN, IMPASSABLE_TERRAIN, KING, KING_DELTAS, KNIGHT, KNIGHT_DELTAS, LION,
    NIGHTRIDER, PAWN, PHOENIX, QUEEN, QUEEN_DIRS, RED, ROOK, ROOK_DIRS,
    SLOW_TERRAIN, VISION_BLOCKING_TERRAIN, WHITE, ZEBRA, ZEBRA_DELTAS,
)
from .model import Move, Piece

KNIGHT_COMPOUNDS = (KNIGHT, FALCON, ELEPHANT, AMAZON, CENTAUR)
BISHOP_SLIDERS = (BISHOP, QUEEN, FALCON, AMAZON)
ROOK_SLIDERS = (ROOK, QUEEN, ELEPHANT, AMAZON)


class Game:
    def __init__(
        self,
        turn_order: tuple[str, ...] = (WHITE, BLACK),
        front_dirs: Optional[dict[str, tuple[int, int]]] = None,
        size: int = 8,
    ) -> None:
        self.size = size
        self.grid: list[list[Optional[Piece]]] = [
            [None] * size for _ in range(size)
        ]
        self.terrain: dict[tuple[int, int], str] = {}
        self.turn_order: list[str] = list(turn_order)
        self.turn: str = self.turn_order[0]
        self.eliminated: set[str] = set()
        if front_dirs is not None:
            self.front_dirs: dict[str, tuple[int, int]] = dict(front_dirs)
        else:
            self.front_dirs = {
                self.turn_order[0]: (-1, 0),
                self.turn_order[-1]: (1, 0),
                WHITE: (-1, 0),
                BLACK: (1, 0),
                RED: (0, 1),
                GREEN: (0, -1),
            }
            if len(self.turn_order) == 2:
                self.front_dirs[self.turn_order[0]] = (-1, 0)
                self.front_dirs[self.turn_order[1]] = (1, 0)
        self.castling: dict[str, dict[str, bool]] = {
            c: {"K": False, "Q": False} for c in ALL_COLORS
        }
        self.ep: Optional[tuple[int, int]] = None
        self.halfmove = 0
        self.fullmove = 1
        self.history: list[Move] = []
        self.last_move: Optional[Move] = None

    @property
    def multi_front(self) -> bool:
        return len(self.turn_order) > 2

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.size and 0 <= c < self.size

    def active_colors(self) -> list[str]:
        return [c for c in self.turn_order if c not in self.eliminated]

    def enemy_colors(self, color: str) -> list[str]:
        return [c for c in self.turn_order if c != color and c not in self.eliminated]

    def next_active_color(self, current: Optional[str] = None) -> str:
        cur = current or self.turn
        active = self.active_colors()
        if not active:
            return cur
        if cur not in self.turn_order:
            return active[0]
        idx = self.turn_order.index(cur)
        for offset in range(1, len(self.turn_order) + 1):
            candidate = self.turn_order[(idx + offset) % len(self.turn_order)]
            if candidate not in self.eliminated:
                return candidate
        return active[0]

    def pawn_vector(self, color: str) -> tuple[int, int]:
        return self.front_dirs.get(color, (-1, 0) if color == WHITE else (1, 0))

    # ------------------------------------------------------------------
    # Tablero
    # ------------------------------------------------------------------
    def place(self, piece: Piece, r: int, c: int) -> None:
        self.grid[r][c] = piece

    def piece_at(self, r: int, c: int) -> Optional[Piece]:
        if self.in_bounds(r, c):
            return self.grid[r][c]
        return None

    def terrain_at(self, r: int, c: int) -> Optional[str]:
        return self.terrain.get((r, c))

    def is_blocked(self, r: int, c: int) -> bool:
        return self.terrain.get((r, c)) in IMPASSABLE_TERRAIN

    def is_vision_blocked(self, r: int, c: int) -> bool:
        return self.terrain.get((r, c)) in VISION_BLOCKING_TERRAIN

    def is_fortified(self, r: int, c: int) -> bool:
        return self.terrain.get((r, c)) in FORTIFIED_TERRAIN

    def is_slow(self, r: int, c: int) -> bool:
        return self.terrain.get((r, c)) in SLOW_TERRAIN

    def add_terrain(self, kind: str, r: int, c: int) -> bool:
        if not self.in_bounds(r, c):
            return False
        if (r, c) in self.terrain:
            return False
        if kind in IMPASSABLE_TERRAIN and self.grid[r][c] is not None:
            return False
        self.terrain[(r, c)] = kind
        if kind in IMPASSABLE_TERRAIN and self.ep == (r, c):
            self.ep = None
        return True

    def remove_terrain(self, r: int, c: int) -> bool:
        return self.terrain.pop((r, c), None) is not None

    def clone(self, search: bool = False) -> "Game":
        """Copia ligera: las piezas son inmutables, solo se copian las filas."""
        g = Game(tuple(self.turn_order), self.front_dirs, size=self.size)
        g.grid = [row[:] for row in self.grid]
        g.terrain = dict(self.terrain)
        g.turn = self.turn
        g.eliminated = set(self.eliminated)
        g.castling = {color: dict(rights) for color, rights in self.castling.items()}
        g.ep = self.ep
        g.halfmove = self.halfmove
        g.fullmove = self.fullmove
        if not search:
            g.history = list(self.history)
            g.last_move = self.last_move
        return g

    def find_king(self, color: str) -> Optional[tuple[int, int]]:
        n = self.size
        for r in range(n):
            row = self.grid[r]
            for c in range(n):
                p = row[c]
                if p and p.color == color and p.kind == KING:
                    return r, c
        return None

    def captured_pieces(self) -> list[Piece]:
        return [m.captured for m in self.history if m.captured is not None]

    # ------------------------------------------------------------------
    # Ataques y jaque
    # ------------------------------------------------------------------
    def is_attacked(self, r: int, c: int, by_color: str) -> bool:
        n = self.size
        fortified = self.is_fortified(r, c)
        fdr, fdc = self.pawn_vector(by_color)
        if fdr != 0:
            pawn_row = r - fdr
            if 0 <= pawn_row < n:
                for dc in (-1, 1):
                    pc = c + dc
                    if 0 <= pc < n:
                        p = self.grid[pawn_row][pc]
                        if p and p.color == by_color and p.kind == PAWN:
                            return True
        else:
            pawn_col = c - fdc
            if 0 <= pawn_col < n:
                for dr in (-1, 1):
                    pr = r + dr
                    if 0 <= pr < n:
                        p = self.grid[pr][pawn_col]
                        if p and p.color == by_color and p.kind == PAWN:
                            return True

        if not fortified:
            # 1. Saltadores tipo Caballo (2x1) y compuestos (Halcón, Elefante, Amazonas, Centauro) + Noctámbulo
            for dr, dc in KNIGHT_DELTAS:
                rr, cc = r + dr, c + dc
                steps = 1
                while 0 <= rr < n and 0 <= cc < n:
                    if self.is_blocked(rr, cc):
                        break
                    p = self.grid[rr][cc]
                    if p is not None:
                        if p.color == by_color:
                            if steps == 1 and (
                                p.kind in KNIGHT_COMPOUNDS
                                or (p.kind == QUEEN and p.veteran)
                            ):
                                return True
                            if p.kind == NIGHTRIDER:
                                if not (self.is_slow(rr, cc) and steps > 2):
                                    return True
                        break
                    if self.is_slow(rr, cc):
                        break
                    rr += dr
                    cc += dc
                    steps += 1

            # 2. Saltos diagonales 2x2 (Fénix)
            for dr, dc in ALFIL_DELTAS:
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    p = self.grid[rr][cc]
                    if p and p.color == by_color and p.kind == PHOENIX:
                        return True

            # 3. Saltos Camello (3x1)
            for dr, dc in CAMEL_DELTAS:
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    p = self.grid[rr][cc]
                    if p and p.color == by_color and p.kind == CAMEL:
                        return True

            # 4. Saltos Cebra (3x2)
            for dr, dc in ZEBRA_DELTAS:
                rr, cc = r + dr, c + dc
                if 0 <= rr < n and 0 <= cc < n:
                    p = self.grid[rr][cc]
                    if p and p.color == by_color and p.kind == ZEBRA:
                        return True

        # 5. Adyacencia (1 paso: Rey, Centauro, Fénix ortogonal, y veteranos)
        for dr, dc in KING_DELTAS:
            rr, cc = r + dr, c + dc
            if 0 <= rr < n and 0 <= cc < n:
                p = self.grid[rr][cc]
                if p and p.color == by_color:
                    if p.kind in (KING, CENTAUR):
                        return True
                    if p.kind == PHOENIX and (
                        abs(dr) + abs(dc) == 1 or p.veteran
                    ):
                        return True
                    if p.veteran and (
                        (p.kind == PAWN and (dr, dc) == (-fdr, -fdc))
                        or (p.kind in (KNIGHT, BISHOP, CAMEL, ZEBRA, NIGHTRIDER, GRASSHOPPER) and abs(dr) + abs(dc) == 1)
                        or (p.kind == ROOK and abs(dr) == 1 and abs(dc) == 1)
                    ):
                        return True

        # 6. Deslizantes (Alfil, Torre, Reina, Halcón, Elefante, Amazonas)
        for directions, kinds in (
            (BISHOP_DIRS, BISHOP_SLIDERS),
            (ROOK_DIRS, ROOK_SLIDERS),
        ):
            for dr, dc in directions:
                rr, cc = r + dr, c + dc
                steps = 1
                while 0 <= rr < n and 0 <= cc < n:
                    if self.is_blocked(rr, cc):
                        break
                    p = self.grid[rr][cc]
                    if p is not None:
                        if p.color == by_color and p.kind in kinds:
                            if not (fortified and steps > 1):
                                if not (self.is_slow(rr, cc) and steps > 2):
                                    return True
                        break
                    if self.is_vision_blocked(rr, cc) or self.is_slow(rr, cc):
                        break
                    rr += dr
                    cc += dc
                    steps += 1

        # 7. Saltadores con obstáculo (Saltamontes y León) en las 8 direcciones de Reina
        if not fortified:
            for dr, dc in QUEEN_DIRS:
                rr, cc = r + dr, c + dc
                hurdle_found = False
                dist_from_target = 1
                while 0 <= rr < n and 0 <= cc < n:
                    if self.is_blocked(rr, cc):
                        break
                    p = self.grid[rr][cc]
                    if not hurdle_found:
                        if p is not None:
                            hurdle_found = True
                            # Saltamontes: solo si el obstáculo estaba inmediatamente al lado del objetivo (dist_from_target == 1)
                            # y el Saltamontes está detrás del obstáculo mirando hacia el objetivo
                    else:
                        if p is not None:
                            if p.color == by_color:
                                if p.kind == LION:
                                    return True
                                if p.kind == GRASSHOPPER and dist_from_target == 2:
                                    return True
                            break
                    rr += dr
                    cc += dc
                    dist_from_target += 1

        return False

    def is_threatened(self, r: int, c: int, defender_color: str) -> bool:
        return any(
            self.is_attacked(r, c, enemy) for enemy in self.enemy_colors(defender_color)
        )

    def in_check(self, color: str) -> bool:
        king = self.find_king(color)
        if king is None:
            return False
        return self.is_threatened(king[0], king[1], color)

    # ------------------------------------------------------------------
    # Generación de movimientos
    # ------------------------------------------------------------------
    def pseudo_moves(self, color: Optional[str] = None) -> list[Move]:
        color = color or self.turn
        n = self.size
        moves: list[Move] = []
        for r in range(n):
            for c in range(n):
                piece = self.grid[r][c]
                if piece is None or piece.color != color:
                    continue
                kind = piece.kind
                if kind == PAWN:
                    self._pawn_moves(r, c, piece, moves)
                elif kind == KNIGHT:
                    deltas = KNIGHT_DELTAS + (ROOK_DIRS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
                elif kind == BISHOP:
                    self._slide_moves(r, c, piece, moves, BISHOP_DIRS)
                    if piece.veteran:
                        self._step_moves(r, c, piece, moves, ROOK_DIRS)
                elif kind == ROOK:
                    self._slide_moves(r, c, piece, moves, ROOK_DIRS)
                    if piece.veteran:
                        self._step_moves(r, c, piece, moves, BISHOP_DIRS)
                elif kind == QUEEN:
                    self._slide_moves(r, c, piece, moves, QUEEN_DIRS)
                    if piece.veteran:
                        self._step_moves(r, c, piece, moves, KNIGHT_DELTAS)
                elif kind == KING:
                    self._step_moves(r, c, piece, moves, KING_DELTAS)
                    if not self.multi_front:
                        self._castle_moves(r, c, piece, moves)
                elif kind == FALCON:
                    # 1. Halcón: Alfil + Caballo
                    self._slide_moves(r, c, piece, moves, BISHOP_DIRS)
                    deltas = KNIGHT_DELTAS + (ROOK_DIRS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
                elif kind == ELEPHANT:
                    # 2. Elefante: Torre + Caballo
                    self._slide_moves(r, c, piece, moves, ROOK_DIRS)
                    deltas = KNIGHT_DELTAS + (BISHOP_DIRS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
                elif kind == AMAZON:
                    # 3. Amazonas: Reina + Caballo
                    self._slide_moves(r, c, piece, moves, QUEEN_DIRS)
                    deltas = KNIGHT_DELTAS + (ALFIL_DELTAS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
                elif kind == GRASSHOPPER:
                    # 4. Saltamontes: Salto sobre 1 pieza y aterriza inmediatamente detrás
                    self._grasshopper_moves(r, c, piece, moves)
                    if piece.veteran:
                        self._step_moves(r, c, piece, moves, ROOK_DIRS)
                elif kind == NIGHTRIDER:
                    # 5. Noctámbulo: Saltos repetidos de Caballo en línea recta
                    self._nightrider_moves(r, c, piece, moves)
                    if piece.veteran:
                        self._step_moves(r, c, piece, moves, ROOK_DIRS)
                elif kind == CENTAUR:
                    # 6. Centauro: Rey + Caballo
                    deltas = KING_DELTAS + KNIGHT_DELTAS + (ALFIL_DELTAS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
                elif kind == CAMEL:
                    # 7. Camello: Salto 3x1
                    deltas = CAMEL_DELTAS + (ROOK_DIRS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
                elif kind == LION:
                    # 8. León: Salta sobre 1 pieza y aterriza en cualquier casilla posterior
                    self._lion_moves(r, c, piece, moves)
                    if piece.veteran:
                        self._step_moves(r, c, piece, moves, KING_DELTAS)
                elif kind == ZEBRA:
                    # 9. Cebra: Salto 3x2
                    deltas = ZEBRA_DELTAS + (ROOK_DIRS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
                elif kind == PHOENIX:
                    # 10. Fénix: 1 paso ortogonal + salto diagonal 2x2
                    deltas = ROOK_DIRS + ALFIL_DELTAS + (BISHOP_DIRS if piece.veteran else ())
                    self._step_moves(r, c, piece, moves, deltas)
        return moves

    def _pawn_moves(self, r: int, c: int, piece: Piece, out: list[Move]) -> None:
        n = self.size
        fdr, fdc = self.pawn_vector(piece.color)
        nr, nc_fwd = r + fdr, c + fdc
        if not (0 <= nr < n and 0 <= nc_fwd < n):
            return

        if fdr != 0:
            # En tablero 8x8 los peones salen de fila 6/1; en 12x12 salen de fila 9/2 (o 10/1)
            start_line = (
                (r in (n - 2, n - 3)) if fdr == -1 else (r in (1, 2))
            )
            is_promo = (nr == (0 if fdr == -1 else n - 1))
            side_deltas = ((0, -1), (0, 1))
        else:
            start_line = (
                (c in (1, 2)) if fdc == 1 else (c in (n - 2, n - 3))
            )
            is_promo = (nc_fwd == (n - 1 if fdc == 1 else 0))
            side_deltas = ((-1, 0), (1, 0))

        promo_options = (
            (AMAZON, QUEEN, ELEPHANT, FALCON, ROOK, KNIGHT)
            if n >= 12
            else (QUEEN, ELEPHANT, FALCON, ROOK, BISHOP, KNIGHT)
        )

        def add_pawn_move(tr: int, tc: int, ep: bool = False) -> None:
            if is_promo:
                for promo in promo_options:
                    out.append(Move(r, c, tr, tc, promotion=promo))
            else:
                out.append(Move(r, c, tr, tc, is_en_passant=ep))

        if not self.is_blocked(nr, nc_fwd) and self.grid[nr][nc_fwd] is None:
            add_pawn_move(nr, nc_fwd)
            if not is_promo and start_line:
                r2, c2 = r + 2 * fdr, c + 2 * fdc
                if (
                    0 <= r2 < n
                    and 0 <= c2 < n
                    and not self.is_slow(r, c)
                    and not self.is_slow(nr, nc_fwd)
                    and not self.is_blocked(r2, c2)
                    and self.grid[r2][c2] is None
                ):
                    out.append(Move(r, c, r2, c2))
        elif (
            piece.veteran
            and not self.is_blocked(nr, nc_fwd)
            and self.grid[nr][nc_fwd] is not None
            and self.grid[nr][nc_fwd].color != piece.color
        ):
            add_pawn_move(nr, nc_fwd)

        if piece.veteran:
            for sdr, sdc in side_deltas:
                sr, sc = r + sdr, c + sdc
                if (
                    0 <= sr < n
                    and 0 <= sc < n
                    and not self.is_blocked(sr, sc)
                    and self.grid[sr][sc] is None
                ):
                    out.append(Move(r, c, sr, sc))

        for sdr, sdc in side_deltas:
            cr, cc = nr + sdr, nc_fwd + sdc
            if not (0 <= cr < n and 0 <= cc < n) or self.is_blocked(cr, cc):
                continue
            target = self.grid[cr][cc]
            if target is not None and target.color != piece.color:
                add_pawn_move(cr, cc)
            elif target is None and self.ep == (cr, cc) and not self.multi_front:
                add_pawn_move(cr, cc, ep=True)

    def _step_moves(
        self, r: int, c: int, piece: Piece, out: list[Move], deltas,
    ) -> None:
        n = self.size
        for dr, dc in deltas:
            rr, cc = r + dr, c + dc
            if not (0 <= rr < n and 0 <= cc < n):
                continue
            if self.is_blocked(rr, cc):
                continue
            target = self.grid[rr][cc]
            if target is None:
                out.append(Move(r, c, rr, cc))
            elif target.color != piece.color:
                dist = max(abs(dr), abs(dc))
                if self.is_fortified(rr, cc) and dist > 1:
                    continue
                out.append(Move(r, c, rr, cc))

    def _slide_moves(
        self, r: int, c: int, piece: Piece, out: list[Move], directions,
    ) -> None:
        n = self.size
        max_steps = 2 if self.is_slow(r, c) else n
        for dr, dc in directions:
            rr, cc = r + dr, c + dc
            steps = 1
            while 0 <= rr < n and 0 <= cc < n and steps <= max_steps:
                if self.is_blocked(rr, cc):
                    break
                target = self.grid[rr][cc]
                if target is None:
                    out.append(Move(r, c, rr, cc))
                    if self.is_vision_blocked(rr, cc) or self.is_slow(rr, cc):
                        break
                else:
                    if target.color != piece.color:
                        if not (self.is_fortified(rr, cc) and steps > 1):
                            out.append(Move(r, c, rr, cc))
                    break
                rr += dr
                cc += dc
                steps += 1

    def _nightrider_moves(
        self, r: int, c: int, piece: Piece, out: list[Move],
    ) -> None:
        n = self.size
        max_steps = 2 if self.is_slow(r, c) else n
        for dr, dc in KNIGHT_DELTAS:
            rr, cc = r + dr, c + dc
            steps = 1
            while 0 <= rr < n and 0 <= cc < n and steps <= max_steps:
                if self.is_blocked(rr, cc):
                    break
                target = self.grid[rr][cc]
                if target is None:
                    out.append(Move(r, c, rr, cc))
                    if self.is_slow(rr, cc):
                        break
                else:
                    if target.color != piece.color and not self.is_fortified(rr, cc):
                        out.append(Move(r, c, rr, cc))
                    break
                rr += dr
                cc += dc
                steps += 1

    def _grasshopper_moves(
        self, r: int, c: int, piece: Piece, out: list[Move],
    ) -> None:
        n = self.size
        for dr, dc in QUEEN_DIRS:
            rr, cc = r + dr, c + dc
            while 0 <= rr < n and 0 <= cc < n:
                if self.is_blocked(rr, cc):
                    break
                if self.grid[rr][cc] is not None:
                    lr, lc = rr + dr, cc + dc
                    if 0 <= lr < n and 0 <= lc < n and not self.is_blocked(lr, lc):
                        target = self.grid[lr][lc]
                        if target is None:
                            out.append(Move(r, c, lr, lc))
                        elif target.color != piece.color and not self.is_fortified(lr, lc):
                            out.append(Move(r, c, lr, lc))
                    break
                rr += dr
                cc += dc

    def _lion_moves(
        self, r: int, c: int, piece: Piece, out: list[Move],
    ) -> None:
        n = self.size
        for dr, dc in QUEEN_DIRS:
            rr, cc = r + dr, c + dc
            hurdle_found = False
            while 0 <= rr < n and 0 <= cc < n:
                if self.is_blocked(rr, cc):
                    break
                p = self.grid[rr][cc]
                if not hurdle_found:
                    if p is not None:
                        hurdle_found = True
                else:
                    if p is None:
                        out.append(Move(r, c, rr, cc))
                    else:
                        if p.color != piece.color and not self.is_fortified(rr, cc):
                            out.append(Move(r, c, rr, cc))
                        break
                rr += dr
                cc += dc

    def _castle_moves(self, r: int, c: int, piece: Piece, out: list[Move]) -> None:
        if piece.kind != KING or self.size != 8:
            return
        fdr, _fdc = self.pawn_vector(piece.color)
        home_row = 7 if fdr == -1 else 0
        if (r, c) != (home_row, 4):
            return
        rights = self.castling.get(piece.color, {"K": False, "Q": False})

        if rights.get("K"):
            corner = self.grid[home_row][7]
            if (
                corner
                and corner.kind == ROOK
                and corner.color == piece.color
                and self.grid[home_row][5] is None
                and self.grid[home_row][6] is None
                and not self.is_blocked(home_row, 5)
                and not self.is_blocked(home_row, 6)
                and not any(
                    self.is_threatened(home_row, col, piece.color)
                    for col in (4, 5, 6)
                )
            ):
                out.append(Move(r, c, home_row, 6, castle="K"))

        if rights.get("Q"):
            corner = self.grid[home_row][0]
            if (
                corner
                and corner.kind == ROOK
                and corner.color == piece.color
                and self.grid[home_row][1] is None
                and self.grid[home_row][2] is None
                and self.grid[home_row][3] is None
                and not any(
                    self.is_blocked(home_row, col) for col in (1, 2, 3)
                )
                and not any(
                    self.is_threatened(home_row, col, piece.color)
                    for col in (4, 3, 2)
                )
            ):
                out.append(Move(r, c, home_row, 2, castle="Q"))

    def legal_moves(self, color: Optional[str] = None) -> list[Move]:
        color = color or self.turn
        if color in self.eliminated:
            return []
        legal = []
        for move in self.pseudo_moves(color):
            if self._leaves_king_safe(move, color):
                legal.append(move)
        return legal

    def _leaves_king_safe(self, move: Move, color: str) -> bool:
        grid_backup = [row[:] for row in self.grid]
        castling_backup = {c: dict(v) for c, v in self.castling.items()}
        ep_backup = self.ep
        halfmove_backup = self.halfmove
        self._move_pieces(move)
        safe = not self.in_check(color)
        self.grid = grid_backup
        self.castling = castling_backup
        self.ep = ep_backup
        self.halfmove = halfmove_backup
        return safe

    def legal_moves_from(self, r: int, c: int) -> list[Move]:
        return [m for m in self.legal_moves(self.turn) if m.fr == r and m.fc == c]

    def visible_squares(self, color: str) -> set[tuple[int, int]]:
        """Casillas que un bando puede ver bajo la niebla de guerra."""
        n = self.size
        visible: set[tuple[int, int]] = set()
        for r in range(n):
            for c in range(n):
                piece = self.grid[r][c]
                if piece is not None and piece.color == color:
                    visible.add((r, c))
                    for dr, dc in KING_DELTAS:
                        rr, cc = r + dr, c + dc
                        if 0 <= rr < n and 0 <= cc < n:
                            visible.add((rr, cc))

        for move in self.pseudo_moves(color):
            visible.add((move.tr, move.tc))

        king = self.find_king(color)
        if king is not None and self.in_check(color):
            for enemy in self.enemy_colors(color):
                for move in self.pseudo_moves(enemy):
                    if (move.tr, move.tc) == king:
                        visible.add((move.fr, move.fc))
        return visible

    # ------------------------------------------------------------------
    # Aplicación de jugadas
    # ------------------------------------------------------------------
    def _move_pieces(self, move: Move) -> tuple[Piece, Optional[Piece], Optional[Piece]]:
        piece = self.grid[move.fr][move.fc]
        assert piece is not None
        captured = self.grid[move.tr][move.tc]
        placed: Optional[Piece] = None

        if move.is_en_passant:
            fdr, _fdc = self.pawn_vector(piece.color)
            cap_row = move.tr - fdr
            captured = self.grid[cap_row][move.tc]
            self.grid[cap_row][move.tc] = None

        self.grid[move.fr][move.fc] = None
        kills = piece.kills + (1 if captured is not None else 0)
        veteran = piece.veteran or (kills >= 2 and piece.kind != KING)
        if move.promotion:
            placed = Piece(
                piece.color, move.promotion, piece.pid, piece.name,
                piece.title, kills=kills, veteran=veteran,
            )
            self.grid[move.tr][move.tc] = placed
        elif kills != piece.kills or veteran != piece.veteran:
            placed = Piece(
                piece.color, piece.kind, piece.pid, piece.name,
                piece.title, kills=kills, veteran=veteran,
            )
            self.grid[move.tr][move.tc] = placed
        else:
            self.grid[move.tr][move.tc] = piece

        if move.castle:
            row = move.tr
            if move.castle == "K":
                rook_from, rook_to = 7, 5
            else:
                rook_from, rook_to = 0, 3
            rook = self.grid[row][rook_from]
            self.grid[row][rook_from] = None
            self.grid[row][rook_to] = rook

        if piece.color in self.castling:
            if piece.kind == KING:
                self.castling[piece.color]["K"] = False
                self.castling[piece.color]["Q"] = False
            elif piece.kind == ROOK:
                if move.fc == 0:
                    self.castling[piece.color]["Q"] = False
                elif move.fc == self.size - 1:
                    self.castling[piece.color]["K"] = False

        if captured is not None and captured.kind == ROOK and captured.color in self.castling:
            opponent = captured.color
            if move.tr in (0, self.size - 1):
                if move.tc == 0:
                    self.castling[opponent]["Q"] = False
                elif move.tc == self.size - 1:
                    self.castling[opponent]["K"] = False

        self.ep = None
        if piece.kind == PAWN and abs(move.tr - move.fr) == 2 and not self.multi_front:
            self.ep = ((move.fr + move.tr) // 2, move.fc)

        if piece.kind == PAWN or captured is not None:
            self.halfmove = 0
        else:
            self.halfmove += 1

        move.moved = piece
        move.captured = captured
        move.placed = placed
        return piece, captured, placed

    def _eliminate_faction(self, color: str) -> None:
        self.eliminated.add(color)
        n = self.size
        for r in range(n):
            for c in range(n):
                p = self.grid[r][c]
                if p is not None and p.color == color:
                    self.grid[r][c] = None

    def apply_move(self, move: Move) -> Move:
        mover_color = self.turn
        self._move_pieces(move)
        eliminated_now: list[str] = []

        if self.multi_front:
            for c in list(self.active_colors()):
                if c != mover_color and self.find_king(c) is None:
                    self._eliminate_faction(c)
                    eliminated_now.append(c)

            next_c = self.next_active_color(mover_color)
            while len(self.active_colors()) > 1 and not self.legal_moves(next_c):
                self._eliminate_faction(next_c)
                eliminated_now.append(next_c)
                next_c = self.next_active_color(mover_color)
            self.turn = next_c
        else:
            self.turn = self.next_active_color(mover_color)

        move.eliminated_factions = tuple(eliminated_now)
        if self.turn == self.turn_order[0]:
            self.fullmove += 1
        self.last_move = move
        self.history.append(move)
        return move

    # ------------------------------------------------------------------
    # Resultado de la partida
    # ------------------------------------------------------------------
    def insufficient_material(self) -> bool:
        if self.multi_front:
            return False
        n = self.size
        minors = []
        for r in range(n):
            for c in range(n):
                p = self.grid[r][c]
                if p is None or p.kind == KING:
                    continue
                if p.kind in (
                    PAWN, ROOK, QUEEN, FALCON, ELEPHANT, AMAZON,
                    CENTAUR, LION, NIGHTRIDER, PHOENIX,
                ):
                    return False
                minors.append(p)
        if len(minors) <= 1:
            return True
        colorbound = [p for p in minors if p.kind in (BISHOP, CAMEL)]
        if len(colorbound) == len(minors):
            colors = set()
            for r in range(n):
                for c in range(n):
                    p = self.grid[r][c]
                    if p and p.kind in (BISHOP, CAMEL):
                        colors.add((r + c) % 2)
            return len(colors) == 1
        return False

    def result(self) -> Optional[dict]:
        if self.multi_front:
            active = self.active_colors()
            if len(active) == 1:
                return {"type": "checkmate", "winner": active[0]}
            if self.turn_order[0] in self.eliminated:
                last_mover = (
                    self.last_move.moved.color
                    if self.last_move and self.last_move.moved
                    else active[0]
                )
                return {"type": "checkmate", "winner": last_mover}
            if self.halfmove >= 120:
                return {"type": "fifty", "winner": None}
            return None

        moves = self.legal_moves(self.turn)
        if not moves:
            if self.in_check(self.turn):
                winner = self.next_active_color(self.turn)
                return {"type": "checkmate", "winner": winner}
            return {"type": "stalemate", "winner": None}
        if self.halfmove >= 100:
            return {"type": "fifty", "winner": None}
        if self.insufficient_material():
            return {"type": "material", "winner": None}
        return None
