"""Oráculo Umbrío: evaluación y búsqueda alfa-beta (8x8 y 12x12, 2 y 4 frentes)."""

from __future__ import annotations

import random
import time
from typing import Optional

from .constants import (
    AMAZON, BISHOP, CAMEL, CENTAUR, ELEPHANT, FALCON, GRASSHOPPER, KING,
    KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, PIECE_VALUE, QUEEN, ROOK, ZEBRA,
)
from .game import Game
from .model import Move

# ----------------------------------------------------------------------
# Tablas de posición por pieza (normalizadas en 8x8 y escaladas a NxN)
# ----------------------------------------------------------------------
PAWN_PST = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]
KNIGHT_PST = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]
BISHOP_PST = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]
ROOK_PST = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0,
]
QUEEN_PST = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
]
KING_PST = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
]
HYBRID_PST = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 5, 10, 15, 15, 10, 5, -10,
    -10, 5, 15, 22, 22, 15, 5, -10,
    -10, 5, 15, 22, 22, 15, 5, -10,
    -10, 5, 10, 15, 15, 10, 5, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]
PST = {
    PAWN: PAWN_PST,
    KNIGHT: KNIGHT_PST,
    BISHOP: BISHOP_PST,
    ROOK: ROOK_PST,
    QUEEN: QUEEN_PST,
    KING: KING_PST,
    FALCON: HYBRID_PST,
    ELEPHANT: HYBRID_PST,
    AMAZON: QUEEN_PST,
    GRASSHOPPER: HYBRID_PST,
    NIGHTRIDER: KNIGHT_PST,
    CENTAUR: KNIGHT_PST,
    CAMEL: KNIGHT_PST,
    LION: HYBRID_PST,
    ZEBRA: KNIGHT_PST,
    PHOENIX: HYBRID_PST,
}

MATE_SCORE = 100000


class _Timeout(Exception):
    pass


def _pst_index(game: Game, color: str, r: int, c: int) -> int:
    n = game.size
    r8 = min(7, max(0, (r * 7) // max(1, n - 1))) if n != 8 else r
    c8 = min(7, max(0, (c * 7) // max(1, n - 1))) if n != 8 else c
    fdr, fdc = game.pawn_vector(color)
    if fdr == -1:
        return r8 * 8 + c8
    if fdr == 1:
        return (7 - r8) * 8 + c8
    if fdc == 1:
        return (7 - c8) * 8 + r8
    return c8 * 8 + r8


def evaluate(game: Game, perspective: Optional[str] = None) -> int:
    """Evaluación desde el punto de vista del bando indicado (por defecto game.turn)."""
    pov = perspective or game.turn
    n = game.size
    own_score = 0
    enemy_scores: dict[str, int] = {}
    for r in range(n):
        for c in range(n):
            piece = game.grid[r][c]
            if piece is None:
                continue
            table = PST.get(piece.kind, HYBRID_PST)
            bonus = 40 if piece.veteran else 0
            if game.is_fortified(r, c):
                bonus += 25
            val = (
                PIECE_VALUE.get(piece.kind, 300)
                + bonus
                + table[_pst_index(game, piece.color, r, c)]
            )
            if piece.color == pov:
                own_score += val
            else:
                enemy_scores[piece.color] = enemy_scores.get(piece.color, 0) + val

    if not enemy_scores:
        return own_score
    if not game.multi_front:
        return own_score - sum(enemy_scores.values())
    max_enemy = max(enemy_scores.values())
    avg_enemy = sum(enemy_scores.values()) // len(enemy_scores)
    return own_score - ((max_enemy + avg_enemy) // 2)


def _order_moves(game: Game, moves: list[Move]) -> list[Move]:
    def score(move: Move) -> int:
        value = 0
        target = game.grid[move.tr][move.tc]
        mover = game.grid[move.fr][move.fc]
        if target is not None and mover is not None:
            value += 10 * PIECE_VALUE.get(target.kind, 300) - PIECE_VALUE.get(mover.kind, 300)
        if move.is_en_passant:
            value += 1000
        if move.promotion:
            value += PIECE_VALUE.get(move.promotion, 900)
        if move.castle:
            value += 60
        return -value

    return sorted(moves, key=score)


class _Search:
    def __init__(self, deadline: float) -> None:
        self.deadline = deadline
        self.nodes = 0

    def negamax(self, game: Game, depth: int, alpha: int, beta: int, ply: int) -> int:
        self.nodes += 1
        if self.nodes % 256 == 0 and time.monotonic() > self.deadline:
            raise _Timeout

        if depth <= 0 and not game.in_check(game.turn):
            return evaluate(game)

        moves = game.legal_moves(game.turn)
        if not moves:
            if game.in_check(game.turn):
                return -(MATE_SCORE - ply)
            return 0
        if depth <= 0:
            return evaluate(game)

        best = -MATE_SCORE * 2
        ordered = _order_moves(game, moves)
        if game.size >= 12 and len(ordered) > 36:
            ordered = ordered[:36]
        for move in ordered:
            child = game.clone(search=True)
            mover = child.turn
            child.apply_move(move)
            if child.multi_front:
                value = evaluate(child, mover)
            else:
                value = -self.negamax(child, depth - 1, -beta, -alpha, ply + 1)
            if value > best:
                best = value
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return best


def find_best_move(
    game: Game,
    depth: int = 2,
    randomness: float = 0.0,
    time_limit: float = 2.0,
    rng: Optional[random.Random] = None,
) -> Optional[Move]:
    rng = rng or random.Random()
    moves = game.legal_moves(game.turn)
    if not moves:
        return None

    deadline = time.monotonic() + time_limit
    search = _Search(deadline)
    scored: list[tuple[int, Move]] = []
    best_score = -MATE_SCORE * 2
    if game.multi_front:
        max_d = 1
    elif game.size >= 12:
        max_d = min(2, max(1, depth))
    else:
        max_d = max(1, depth)

    for d in range(1, max_d + 1):
        current_scored: list[tuple[int, Move]] = []
        current_best = -MATE_SCORE * 2
        timed_out = False
        ordered = (
            [m for _s, m in scored]
            if scored
            else _order_moves(game, moves)
        )
        for move in ordered:
            child = game.clone(search=True)
            mover = child.turn
            child.apply_move(move)
            try:
                if child.multi_front:
                    next_moves = child.legal_moves(child.turn)[:8]
                    if next_moves:
                        worst_reply = min(
                            (
                                evaluate(
                                    (lambda g, m: (g.apply_move(m), g)[1])(child.clone(search=True), nm),
                                    mover,
                                )
                                for nm in next_moves
                            ),
                            default=evaluate(child, mover),
                        )
                        value = worst_reply + (120 if move.captured else 0)
                    else:
                        value = evaluate(child, mover)
                else:
                    value = -search.negamax(child, d - 1, -MATE_SCORE * 2, MATE_SCORE * 2, 1)
            except _Timeout:
                timed_out = True
                break
            current_scored.append((value, move))
            if value > current_best:
                current_best = value

        if current_scored and (not timed_out or not scored):
            current_scored.sort(key=lambda item: item[0], reverse=True)
            scored = current_scored
            best_score = current_best
        if timed_out:
            break

    if not scored:
        return moves[0]

    scored.sort(key=lambda item: item[0], reverse=True)
    if best_score < -MATE_SCORE:
        best_score = scored[0][0]
    if randomness > 0 and rng.random() < randomness:
        margin = 90 if depth <= 1 else 45
        near_best = [m for s, m in scored if s >= best_score - margin]
        return rng.choice(near_best or [scored[0][1]])
    top = [m for s, m in scored if s == best_score] or [scored[0][1]]
    return rng.choice(top)
