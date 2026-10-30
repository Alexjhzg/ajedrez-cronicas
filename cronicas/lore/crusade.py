"""Modo Cruzada Encadenada Multi-Frente: progresión, rivales y refuerzos."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from ..engine import (
    BLACK, CENTAUR, ELEPHANT, FALCON, GREEN, KING, KNIGHT, LION, NIGHTRIDER,
    PAWN, PHOENIX, RED, WHITE, Game, Piece,
)
from .board import create_game
from .factions import faction_name, rival_factions
from .wilds import (
    NAME_POOLS, THEMES, TITLES, WildScenario, _army_kinds, _army_summary,
    _generate_terrain, _is_playable, _make_pieces, _terrain_summary,
    create_wild_scenario,
)

CRUSADE_STAGES = (
    ("bosque", "Etapa I · El Bosque de los Susurros", "Escudero"),
    ("rio", "Etapa II · La Ribera de Ceniza", "Caballero"),
    ("paso", "Etapa III · El Paso del Dragón", "Caballero"),
    ("ruinas", "Etapa IV · Las Ruinas del Trono", "Archimago"),
)


@dataclass
class CrusadeState:
    stage: int
    total_stages: int
    roster: list[Piece]
    next_pid: int
    victories: int = 0
    player_color: str = WHITE
    stage_rivals: tuple[str, ...] = (GREEN, RED, RED, BLACK)


def _build_stage_rivals(player_color: str) -> tuple[str, ...]:
    if player_color == WHITE:
        return (GREEN, RED, RED, BLACK)
    if player_color == BLACK:
        return (GREEN, RED, WHITE, WHITE)
    if player_color == RED:
        return (GREEN, WHITE, BLACK, BLACK)
    if player_color == GREEN:
        return (RED, WHITE, BLACK, BLACK)
    rivals = rival_factions(player_color)
    return (rivals[0], rivals[1], rivals[1], rivals[2])


def create_crusade(
    elephant: bool = False,
    player_color: str = WHITE,
) -> CrusadeState:
    rivals = _build_stage_rivals(player_color)
    base_game = create_game(
        elephant=elephant, player_color=player_color, enemy_color=rivals[0],
    )
    roster: list[Piece] = []
    max_pid = 1
    for r in (6, 7):
        for c in range(8):
            p = base_game.grid[r][c]
            if p is not None and p.color == player_color:
                roster.append(p)
                if p.pid >= max_pid:
                    max_pid = p.pid + 1
    return CrusadeState(
        stage=0,
        total_stages=len(CRUSADE_STAGES),
        roster=roster,
        next_pid=max_pid + 32,
        player_color=player_color,
        stage_rivals=rivals,
    )


def create_crusade_stage(
    crusade: CrusadeState,
    elephant: bool = False,
    rng: Optional[random.Random] = None,
) -> tuple[WildScenario, str]:
    rng = rng or random.Random()
    idx = min(crusade.stage, len(CRUSADE_STAGES) - 1)
    theme, stage_title, stage_diff = CRUSADE_STAGES[idx]
    player_c = crusade.player_color
    enemy_c = crusade.stage_rivals[min(idx, len(crusade.stage_rivals) - 1)]

    enemy_comp = _army_kinds(rng, elephant=elephant)
    terrain: dict[tuple[int, int], str] = {}
    game: Optional[Game] = None

    for _ in range(120):
        terrain = _generate_terrain(theme, rng)
        candidate = Game(turn_order=(player_c, enemy_c))
        for (r, c), kind in terrain.items():
            candidate.add_terrain(kind, r, c)

        player_slots = [
            (r, c) for r in (6, 7) for c in range(8)
            if not candidate.is_blocked(r, c)
        ]
        if len(player_slots) < len(crusade.roster):
            continue
        rng.shuffle(player_slots)
        for piece, (r, c) in zip(crusade.roster, player_slots):
            candidate.place(piece, r, c)

        enemy_kinds = list(enemy_comp)
        rng.shuffle(enemy_kinds)
        enemy_pieces, crusade.next_pid = _make_pieces(
            enemy_c, enemy_kinds, rng, crusade.next_pid,
        )
        enemy_slots = [
            (r, c) for r in (0, 1) for c in range(8)
            if not candidate.is_blocked(r, c)
        ]
        if len(enemy_slots) < len(enemy_pieces):
            continue
        rng.shuffle(enemy_slots)
        for piece, (r, c) in zip(enemy_pieces, enemy_slots):
            candidate.place(piece, r, c)

        if _is_playable(candidate):
            game = candidate
            break

    if game is None:
        scenario = create_wild_scenario(
            rng=rng, elephant=elephant,
            player_color=player_c, enemy_color=enemy_c,
        )
        return scenario, stage_diff

    meta = THEMES[theme]
    rival_label = faction_name(enemy_c)
    scenario = WildScenario(
        game=game,
        theme=theme,
        title=f"{stage_title} · Frente a {rival_label}",
        description=meta["description"],
        terrain_summary=_terrain_summary(terrain),
        army_summary=_army_summary([p.kind for p in crusade.roster]),
    )
    return scenario, stage_diff


def update_crusade_survivors(crusade: CrusadeState, game: Game) -> list[Piece]:
    player_c = crusade.player_color
    survivors: list[Piece] = []
    for r in range(game.size):
        for c in range(game.size):
            p = game.grid[r][c]
            if p is not None and p.color == player_c:
                survivors.append(p)
    if not any(p.kind == KING for p in survivors):
        king_name = NAME_POOLS.get(player_c, NAME_POOLS[WHITE])[KING][0]
        king_title = TITLES.get(player_c, TITLES[WHITE])[KING]
        survivors.insert(0, Piece(player_c, KING, 5, king_name, king_title))
    crusade.roster = survivors
    return survivors


def apply_crusade_boon(
    crusade: CrusadeState, boon: str, rng: Optional[random.Random] = None,
) -> str:
    rng = rng or random.Random()
    player_c = crusade.player_color
    if boon == "reinforce":
        added = []
        vanguard_kind = rng.choice((KNIGHT, CENTAUR, PHOENIX, FALCON))
        for kind in (vanguard_kind, PAWN, PAWN):
            if len(crusade.roster) >= 16:
                break
            pieces, crusade.next_pid = _make_pieces(
                player_c, [kind], rng, crusade.next_pid,
            )
            crusade.roster.extend(pieces)
            added.append(pieces[0].name)
        return (
            f"Se unen a la columna: {', '.join(added)}."
            if added else "Las filas ya están completas."
        )
    if boon == "elephant":
        if len(crusade.roster) < 16:
            pieces, crusade.next_pid = _make_pieces(
                player_c, [ELEPHANT], rng, crusade.next_pid,
            )
            crusade.roster[0:0] = pieces
            return f"{pieces[0].name} se une a la vanguardia como Elefante de Guerra."
        for idx, p in enumerate(crusade.roster):
            if p.kind == PAWN:
                pieces, crusade.next_pid = _make_pieces(
                    player_c, [ELEPHANT], rng, crusade.next_pid,
                )
                crusade.roster[idx] = pieces[0]
                return f"{pieces[0].name} reemplaza a un escudero en la vanguardia."
        return "Un Elefante de Guerra marcha junto al ejército."
    if boon == "mythic":
        mythic_kind = rng.choice((FALCON, LION, NIGHTRIDER, CENTAUR, PHOENIX))
        if len(crusade.roster) < 16:
            pieces, crusade.next_pid = _make_pieces(
                player_c, [mythic_kind], rng, crusade.next_pid,
            )
            crusade.roster[0:0] = pieces
            return f"{pieces[0].name} ({pieces[0].title}) responde al llamado de la Cruzada."
        for idx, p in enumerate(crusade.roster):
            if p.kind == PAWN:
                pieces, crusade.next_pid = _make_pieces(
                    player_c, [mythic_kind], rng, crusade.next_pid,
                )
                crusade.roster[idx] = pieces[0]
                return f"{pieces[0].name} ({pieces[0].title}) toma el puesto de vanguardia."
        return "Un campeón mítico marcha junto al ejército."
    if boon == "veteran":
        promoted = []
        for idx, p in enumerate(crusade.roster):
            if p.kind != KING and not p.veteran:
                crusade.roster[idx] = Piece(
                    p.color, p.kind, p.pid, p.name, p.title,
                    kills=max(2, p.kills), veteran=True,
                )
                promoted.append(p.name)
                if len(promoted) >= 2:
                    break
        return (
            f"Ascienden al rango de Veterano: {', '.join(promoted)}."
            if promoted else "Tus guerreros ya son veteranos curtidos."
        )
    return "El ejército descansa antes de la siguiente marcha."
