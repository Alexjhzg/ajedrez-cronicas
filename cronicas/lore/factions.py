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
        "culture": "Sacro Imperio y Cruzadas Franco-Normandas",
        "sovereigns": "Rey Balduino y Reina Leonor",
        "motto": "Catedrales de mármol blanco, órdenes templarias y el juramento del Sol Invicto.",
        "lore": (
            "Inspirada en los reinos cruzados franco-normandos y el Sacro Imperio. "
            "Sus ejércitos marchan desde ciudadelas de caliza blanca y catedrales góticas "
            "bajo el código de caballería templaria, liderados por el Rey Balduino y la Reina Leonor."
        ),
    },
    BLACK: {
        "name": "Legión del Eclipse",
        "short": "el Eclipse",
        "adjective": "umbría",
        "crest": "☾",
        "culture": "Principado de Valaquia y Transilvania Gótica",
        "sovereigns": "Rey Vladimir y Reina Carmila",
        "motto": "Ciudadelas escarpadas de los Cárpatos, la Orden del Dragón y los voivodas nocturnos.",
        "lore": (
            "Inspirada en la Valaquia histórica de la Orden del Dragón y los castillos "
            "góticos de Transilvania. Desde fortalezas alzadas sobre desfiladeros envueltos "
            "en niebla, el Rey Vladimir y la Reina Carmila defienden sus dominios con "
            "caballería nocturna y terror psicológico."
        ),
    },
    RED: {
        "name": "Forja Carmesí",
        "short": "la Forja",
        "adjective": "carmesí",
        "crest": "⚔",
        "culture": "Esparta Clásica e Imperio Romano",
        "sovereigns": "Rey Leónidas y Reina Gorgo",
        "motto": "Falanges de bronce, legiones de hierro y la ley de volver con el escudo o sobre él.",
        "lore": (
            "Inspirada en la disciplina militar de la Esparta clásica y la maquinaria "
            "bélica de las legiones de Roma. Bajo capas carmesíes y águilas de bronce, "
            "el Rey Leónidas y la Reina Gorgo gobiernan una ciudadanía forjada para la "
            "guerra en formación cerrada."
        ),
    },
    GREEN: {
        "name": "Pacto de la Espesura",
        "short": "el Pacto",
        "adjective": "silvana",
        "crest": "❖",
        "culture": "Confederación Celta de Galia, Britania e Hibernia",
        "sovereigns": "Rey Vercingétorix y Reina Boudica",
        "motto": "Robledales sagrados de los druidas, círculos megalíticos y clanes pintados con glasto.",
        "lore": (
            "Inspirado en las tribus celtas de la Galia, los clanes britanos e Hibernia. "
            "Reunidos en torno a nemetones sagrados y fortalezas de colina, el Rey "
            "Vercingétorix y la Reina Boudica lideran emboscadas relámpago entre "
            "bosques milenarios."
        ),
    },
}

KIND_LABEL = {
    WHITE: {
        KING: "Rey Cruzado del Alba",
        QUEEN: "Soberana de las Catedrales",
        ROOK: "Bastión Templario",
        BISHOP: "Prelado del Sol",
        KNIGHT: "Caballero Hospitalario",
        PAWN: "Cruzado del Alba",
        FALCON: "Halcón Solar",
        ELEPHANT: "Coloso de Ultramar",
        AMAZON: "Paladina del Alba",
        GRASSHOPPER: "Saltamontes de Luz",
        NIGHTRIDER: "Noctámbulo Astral",
        CENTAUR: "Centauro Dorado",
        CAMEL: "Camello de Ultramar",
        LION: "León de Ricardo",
        ZEBRA: "Cebra de Antioquía",
        PHOENIX: "Fénix Sagrado",
    },
    BLACK: {
        KING: "Voivoda del Eclipse",
        QUEEN: "Condesa de la Sangre Nocturna",
        ROOK: "Ciudadela de los Cárpatos",
        BISHOP: "Boyardo del Eclipse",
        KNIGHT: "Húsar de la Noche",
        PAWN: "Guardia de la Empalizada",
        FALCON: "Halcón de los Cárpatos",
        ELEPHANT: "Coloso de Valaquia",
        AMAZON: "Amazonas del Dragón",
        GRASSHOPPER: "Saltamontes del Vacío",
        NIGHTRIDER: "Noctámbulo de Transilvania",
        CENTAUR: "Centauro de Hueso",
        CAMEL: "Camello del Danubio",
        LION: "León de Valaquia",
        ZEBRA: "Cebra Espectral",
        PHOENIX: "Fénix de Ceniza",
    },
    RED: {
        KING: "Éforo de la Falange Carmesí",
        QUEEN: "Augusta de Hierro y Bronce",
        ROOK: "Castrum Pretoriano",
        BISHOP: "Augur de Marte",
        KNIGHT: "Equite Cataphracto",
        PAWN: "Hoplita de la Falange",
        FALCON: "Águila Imperial",
        ELEPHANT: "Elefante Pírrico",
        AMAZON: "Campeona de Esparta",
        GRASSHOPPER: "Velite Saltador",
        NIGHTRIDER: "Explorador Pretoriano",
        CENTAUR: "Centauro de Lacedemonia",
        CAMEL: "Camello de Siria",
        LION: "León de las Termópilas",
        ZEBRA: "Cebra Numidia",
        PHOENIX: "Fénix de Vesta",
    },
    GREEN: {
        KING: "Gran Caudillo de los Clanes",
        QUEEN: "Reina Guerrera de los Icenos",
        ROOK: "Dun Megalítico",
        BISHOP: "Archidruida del Robledal",
        KNIGHT: "Auriga de Guerra Celta",
        PAWN: "Guerrero Gaisata",
        FALCON: "Halcón de Hibernia",
        ELEPHANT: "Behemot Pictórico",
        AMAZON: "Morrigan de la Espesura",
        GRASSHOPPER: "Saltador de los Túmulos",
        NIGHTRIDER: "Jinete de la Cacería Salvaje",
        CENTAUR: "Centauro del Robledal",
        CAMEL: "Corcel de las Tierras Altas",
        LION: "Sabueso de Ulster",
        ZEBRA: "Corcel Pintado de Glasto",
        PHOENIX: "Ave de Beltane",
    },
}


def faction_name(color: str) -> str:
    return FACTIONS.get(color, FACTIONS[WHITE])["name"]


def rival_factions(player_color: str) -> list[str]:
    return [c for c in ALL_COLORS if c != player_color]
