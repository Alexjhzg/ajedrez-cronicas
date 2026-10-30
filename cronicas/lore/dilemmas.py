"""Sucesos de Guerra Interactivos: dilemas tácticos y decisiones del comandante."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional

from ..engine import Game
from .geography import square_name
from .narrative import LoreEntry
from .wilds import (
    EVENT_SPECS, MAX_TERRAIN, TERRAIN_CONSEQUENCE, TERRAIN_LABEL,
    WildScenario, _event_candidates,
)


@dataclass
class WildChoice:
    label: str
    description: str
    kind: str
    r: int
    c: int
    opening: str


@dataclass
class WildDilemma:
    title: str
    prompt: str
    options: tuple[WildChoice, WildChoice]


def wild_dilemma(
    game: Game,
    scenario: WildScenario,
    rng: Optional[random.Random] = None,
) -> Optional[WildDilemma]:
    rng = rng or random.Random()
    if len(game.terrain) >= MAX_TERRAIN:
        return None
    candidates = _event_candidates(game)
    if len(candidates) < 2:
        return None
    (r1, c1), (r2, c2) = rng.sample(candidates, 2)
    specs = list(EVENT_SPECS.get(scenario.theme, EVENT_SPECS["ruinas"]))
    rng.shuffle(specs)
    title1, kind1, opening1 = specs[0]
    title2, kind2, opening2 = specs[1 % len(specs)]
    loc1 = square_name(r1, c1)
    loc2 = square_name(r2, c2)
    opt1 = WildChoice(
        label=f"{title1} en {loc1}",
        description=f"Añade {TERRAIN_LABEL[kind1]} en {loc1}. {TERRAIN_CONSEQUENCE[kind1]}",
        kind=kind1, r=r1, c=c1, opening=opening1,
    )
    opt2 = WildChoice(
        label=f"{title2} en {loc2}",
        description=f"Añade {TERRAIN_LABEL[kind2]} en {loc2}. {TERRAIN_CONSEQUENCE[kind2]}",
        kind=kind2, r=r2, c=c2, opening=opening2,
    )
    return WildDilemma(
        title=f"Encrucijada en {scenario.title}",
        prompt=(
            "El campo de batalla cede bajo el fragor del combate. "
            "Como comandante, decide qué rumbo toma el suceso de guerra:"
        ),
        options=(opt1, opt2),
    )


def apply_wild_choice(game: Game, choice: WildChoice) -> Optional[LoreEntry]:
    if not game.add_terrain(choice.kind, choice.r, choice.c):
        return None
    text = (
        f"{choice.opening} en {square_name(choice.r, choice.c)}. "
        f"{TERRAIN_CONSEQUENCE[choice.kind]} El terreno de la campaña ha cambiado."
    )
    return LoreEntry(f"Suceso de guerra · {choice.label}", text, "event")
