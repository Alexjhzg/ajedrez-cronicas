"""API pública del universo narrativo de Aethelgard."""

from .board import (
    create_four_fronts_game, create_game, create_imperial_game, piece_on_board,
)
from .characters import character_bio
from .crusade import (
    CRUSADE_STAGES, CrusadeState, apply_crusade_boon, create_crusade,
    create_crusade_stage, update_crusade_survivors,
)
from .dilemmas import WildChoice, WildDilemma, apply_wild_choice, wild_dilemma
from .factions import FACTIONS, KIND_LABEL, faction_name, rival_factions
from .geography import location_label, square_name
from .narrative import (
    PROMOTED_TITLE, PROMOTION_ROLE, LoreEntry, ambient_entry, epilogue,
    fog_entry, four_fronts_prologue, imperial_prologue, narrate_move,
    prologue, result_icon, result_title, to_roman,
)
from .wilds import (
    TERRAIN_CONSEQUENCE, TERRAIN_LABEL, WILD_EVENT_EVERY, WildScenario,
    create_wild_scenario, terrain_label, wild_event, wild_prologue,
)

__all__ = [
    "CRUSADE_STAGES", "FACTIONS", "KIND_LABEL", "PROMOTED_TITLE",
    "PROMOTION_ROLE", "TERRAIN_CONSEQUENCE", "TERRAIN_LABEL",
    "WILD_EVENT_EVERY", "CrusadeState", "LoreEntry", "WildChoice",
    "WildDilemma", "WildScenario", "ambient_entry", "apply_crusade_boon",
    "apply_wild_choice", "character_bio", "create_crusade",
    "create_crusade_stage", "create_four_fronts_game", "create_game",
    "create_imperial_game", "create_wild_scenario", "epilogue",
    "faction_name", "fog_entry", "four_fronts_prologue", "imperial_prologue",
    "location_label", "narrate_move", "piece_on_board", "prologue",
    "result_icon", "result_title", "rival_factions", "square_name",
    "terrain_label", "to_roman", "update_crusade_survivors", "wild_dilemma",
    "wild_event", "wild_prologue",
]
