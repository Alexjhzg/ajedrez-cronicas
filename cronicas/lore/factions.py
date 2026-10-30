"""Identidad de las cuatro facciones de Aethelgard y nombres de sus piezas."""

from __future__ import annotations

from ..engine import (
    ALL_COLORS, AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FALCON,
    GRASSHOPPER, GREEN, KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, QUEEN,
    RED, ROOK, WHITE, ZEBRA,
)

FACTIONS = {
    WHITE: {
        "name": "Orden del Alba",
        "short": "el Alba",
        "adjective": "alba",
        "crest": "☀",
        "culture": "Reino Cruzado",
        "sovereigns": "Rey Balduino y Reina Leonor",
        "motto": "Caballeros templarios, fortalezas blancas y honor solar.",
        "lore": "Reino de caballeros templarios y fortalezas blancas liderado por el Rey Balduino y la Reina Leonor.",
    },
    BLACK: {
        "name": "Legión del Eclipse",
        "short": "el Eclipse",
        "adjective": "umbría",
        "crest": "☾",
        "culture": "Corte de Valaquia",
        "sovereigns": "Rey Vladimir y Reina Carmila",
        "motto": "Castillos en la niebla, guardia nocturna y la Orden del Dragón.",
        "lore": "Señores nocturnos de Valaquia que dominan desde castillos en la niebla bajo el Rey Vladimir y la Reina Carmila.",
    },
    RED: {
        "name": "Forja Carmesí",
        "short": "la Forja",
        "adjective": "carmesí",
        "crest": "⚔",
        "culture": "Imperio Espartano",
        "sovereigns": "Rey Leónidas y Reina Gorgo",
        "motto": "Falanges de bronce, legiones de hierro y disciplina marcial.",
        "lore": "Imperio marcial de falanges de bronce y legiones de hierro comandado por el Rey Leónidas y la Reina Gorgo.",
    },
    GREEN: {
        "name": "Pacto de la Espesura",
        "short": "el Pacto",
        "adjective": "silvana",
        "crest": "❖",
        "culture": "Clanes Celtas",
        "sovereigns": "Rey Vercingétorix y Reina Boudica",
        "motto": "Guerreros de los clanes, druidas y bosques sagrados.",
        "lore": "Confederación de clanes celtas y druidas de los bosques guiada por el Rey Vercingétorix y la Reina Boudica.",
    },
}

KIND_LABEL = {
    WHITE: {
        KING: "Rey Cruzado",
        QUEEN: "Reina del Alba",
        ROOK: "Bastión Templario",
        BISHOP: "Prelado",
        KNIGHT: "Caballero Templario",
        PAWN: "Cruzado",
        FALCON: "Halcón Real",
        ELEPHANT: "Elefante Real",
        AMAZON: "Paladina",
        GRASSHOPPER: "Saltador Solar",
        NIGHTRIDER: "Jinete Astral",
        CENTAUR: "Centauro Real",
        CAMEL: "Camello Cruzado",
        LION: "León Real",
        ZEBRA: "Corcel Blanco",
        PHOENIX: "Fénix Solar",
    },
    BLACK: {
        KING: "Rey de Valaquia",
        QUEEN: "Reina Nocturna",
        ROOK: "Castillo Gótico",
        BISHOP: "Conde Nocturno",
        KNIGHT: "Jinete Nocturno",
        PAWN: "Guardia Nocturno",
        FALCON: "Halcón Nocturno",
        ELEPHANT: "Elefante de Asedio",
        AMAZON: "Dama del Dragón",
        GRASSHOPPER: "Saltador Umbrío",
        NIGHTRIDER: "Jinete de la Niebla",
        CENTAUR: "Centauro Oscuro",
        CAMEL: "Camello Nocturno",
        LION: "León Negro",
        ZEBRA: "Corcel de Sombra",
        PHOENIX: "Fénix de Ceniza",
    },
    RED: {
        KING: "Rey de Esparta",
        QUEEN: "Reina de Esparta",
        ROOK: "Fortaleza de Bronce",
        BISHOP: "Oráculo de Guerra",
        KNIGHT: "Centurión",
        PAWN: "Espartano",
        FALCON: "Águila Imperial",
        ELEPHANT: "Elefante de Guerra",
        AMAZON: "Campeona Espartana",
        GRASSHOPPER: "Saltador de Bronce",
        NIGHTRIDER: "Jinete Pretoriano",
        CENTAUR: "Centauro de Bronce",
        CAMEL: "Camello Imperial",
        LION: "León de Esparta",
        ZEBRA: "Corcel Carmesí",
        PHOENIX: "Fénix de Fuego",
    },
    GREEN: {
        KING: "Rey de los Clanes",
        QUEEN: "Reina Guerrera",
        ROOK: "Bastión del Bosque",
        BISHOP: "Druida",
        KNIGHT: "Jinete Celta",
        PAWN: "Guerrero Celta",
        FALCON: "Halcón del Bosque",
        ELEPHANT: "Coloso del Bosque",
        AMAZON: "Guerrera Celta",
        GRASSHOPPER: "Saltador del Bosque",
        NIGHTRIDER: "Jinete Salvaje",
        CENTAUR: "Centauro del Bosque",
        CAMEL: "Corcel de las Colinas",
        LION: "León de las Tierras Altas",
        ZEBRA: "Corcel Pintado",
        PHOENIX: "Fénix del Bosque",
    },
}


def faction_name(color: str) -> str:
    return FACTIONS.get(color, FACTIONS[WHITE])["name"]


def rival_factions(player_color: str) -> list[str]:
    return [c for c in ALL_COLORS if c != player_color]
