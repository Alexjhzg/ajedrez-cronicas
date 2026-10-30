"""Reparto, títulos y biografías de los cuatro reinos y las 10 piezas del Códice."""

from __future__ import annotations

from ..engine import (
    AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FALCON, GRASSHOPPER,
    GREEN, KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, QUEEN, RED, ROOK,
    WHITE, ZEBRA, Piece,
)

PIECE_DISPLAY_NAME = {
    KING: "Rey",
    QUEEN: "Reina",
    ROOK: "Torre",
    BISHOP: "Alfil",
    KNIGHT: "Caballo",
    PAWN: "Peón",
    FALCON: "Halcón",
    ELEPHANT: "Elefante",
    AMAZON: "Amazonas",
    GRASSHOPPER: "Saltamontes",
    NIGHTRIDER: "Noctámbulo",
    CENTAUR: "Centauro",
    CAMEL: "Camello",
    LION: "León",
    ZEBRA: "Cebra",
    PHOENIX: "Fénix",
}

WHITE_BACK = [
    (ROOK, "Torre", "Bastión Templario"),
    (KNIGHT, "Caballo", "Caballero Templario"),
    (BISHOP, "Alfil", "Prelado"),
    (QUEEN, "Reina Leonor", "Reina del Alba"),
    (KING, "Rey Balduino", "Rey Cruzado"),
    (BISHOP, "Alfil", "Prelado"),
    (KNIGHT, "Caballo", "Caballero Templario"),
    (ROOK, "Torre", "Bastión Templario"),
]

BLACK_BACK = [
    (ROOK, "Torre", "Castillo Gótico"),
    (KNIGHT, "Caballo", "Jinete Nocturno"),
    (BISHOP, "Alfil", "Conde Nocturno"),
    (QUEEN, "Reina Carmila", "Reina Nocturna"),
    (KING, "Rey Vladimir", "Rey de Valaquia"),
    (BISHOP, "Alfil", "Conde Nocturno"),
    (KNIGHT, "Caballo", "Jinete Nocturno"),
    (ROOK, "Torre", "Castillo Gótico"),
]

RED_BACK = [
    (ROOK, "Torre", "Fortaleza de Bronce"),
    (KNIGHT, "Caballo", "Centurión"),
    (BISHOP, "Alfil", "Oráculo de Guerra"),
    (QUEEN, "Reina Gorgo", "Reina de Esparta"),
    (KING, "Rey Leónidas", "Rey de Esparta"),
    (BISHOP, "Alfil", "Oráculo de Guerra"),
    (KNIGHT, "Caballo", "Centurión"),
    (ROOK, "Torre", "Fortaleza de Bronce"),
]

GREEN_BACK = [
    (ROOK, "Torre", "Bastión del Bosque"),
    (KNIGHT, "Caballo", "Jinete Celta"),
    (BISHOP, "Alfil", "Druida"),
    (QUEEN, "Reina Morgana", "Reina de Avalon"),
    (KING, "Rey Artur", "Rey de Avalon"),
    (BISHOP, "Alfil", "Druida"),
    (KNIGHT, "Caballo", "Jinete Celta"),
    (ROOK, "Torre", "Bastión del Bosque"),
]

WHITE_ELEPHANT = (ELEPHANT, "Elefante", "Elefante Real")
BLACK_ELEPHANT = (ELEPHANT, "Elefante", "Elefante de Asedio")
RED_ELEPHANT = (ELEPHANT, "Elefante", "Elefante de Guerra")
GREEN_ELEPHANT = (ELEPHANT, "Elefante", "Coloso del Bosque")

WHITE_PAWNS = [("Peón", "Cruzado")] * 12
BLACK_PAWNS = [("Peón", "Guardia Nocturno")] * 12
RED_PAWNS = [("Peón", "Espartano")] * 12
GREEN_PAWNS = [("Peón", "Guerrero Celta")] * 12

FACTION_BACK = {
    WHITE: WHITE_BACK,
    BLACK: BLACK_BACK,
    RED: RED_BACK,
    GREEN: GREEN_BACK,
}

FACTION_ELEPHANT = {
    WHITE: WHITE_ELEPHANT,
    BLACK: BLACK_ELEPHANT,
    RED: RED_ELEPHANT,
    GREEN: GREEN_ELEPHANT,
}

FACTION_PAWNS = {
    WHITE: WHITE_PAWNS,
    BLACK: BLACK_PAWNS,
    RED: RED_PAWNS,
    GREEN: GREEN_PAWNS,
}

OFFICER_BIOS = {
    "Rey Balduino": (
        "El Rey de la máscara de plata; lidera a los caballeros cruzados del Alba "
        "con fe y estrategia inquebrantables."
    ),
    "Reina Leonor": (
        "Soberana del Alba cuya diplomacia y temple dirigen las órdenes de caballería."
    ),
    "Rey Vladimir": (
        "Señor de Valaquia y de la Orden del Dragón; defiende sus montañas con "
        "mano de hierro y terror nocturno."
    ),
    "Reina Carmila": (
        "Soberana inmortal de los castillos envueltos en niebla, maestra de los "
        "secretos de la noche."
    ),
    "Rey Leónidas": (
        "Rey guerrero de Esparta que encabeza la falange de bronce sin retroceder "
        "jamás un paso."
    ),
    "Reina Gorgo": (
        "Reina de Esparta cuya voz gobierna la patria bajo la ley de volver con "
        "el escudo o sobre él."
    ),
    "Rey Artur": (
        "Monarca legendario de Avalon que empuña la espada sagrada en defensa del reino."
    ),
    "Reina Morgana": (
        "Soberana y hechicera de las nieblas de Avalon, señora de los secretos antiguos."
    ),
}

PAWN_BIOS = {
    WHITE: "Soldado cruzado que marcha con escudo blanco y fe en la Orden del Alba.",
    BLACK: "Guardia nocturno de Valaquia que vigila los pasos de montaña entre la niebla.",
    RED: "Guerrero espartano que avanza en falange cerrada con escudo de bronce y lanza.",
    GREEN: "Guerrero de los clanes celtas que lucha con lanza y pintura de guerra azul.",
}

FAIRY_GENERIC_BIOS = {
    FALCON: (
        "Halcón de Guerra (Híbrido Alfil + Caballo): domina todas las diagonales "
        "y ejecuta saltos de caballo para cambiar el color de su casilla."
    ),
    ELEPHANT: (
        "Elefante de Asedio (Híbrido Torre + Caballo): combina el barrido en "
        "línea recta de una torre con el salto en L del caballo."
    ),
    AMAZON: (
        "Amazonas Imperial (Híbrido Reina + Caballo): la fuerza más destructiva "
        "de Aethelgard. Combina los movimientos de Torre, Alfil y Caballo."
    ),
    GRASSHOPPER: (
        "Saltamontes Místico (Salto obligatorio): se desplaza en las 8 direcciones "
        "de la Reina saltando exactamente sobre una pieza para aterrizar justo detrás."
    ),
    NIGHTRIDER: (
        "Noctámbulo (Saltador de largo alcance): encadena múltiples saltos de "
        "caballo en una misma línea recta durante un solo turno."
    ),
    CENTAUR: (
        "Centauro de Guardia (Híbrido Rey + Caballo): da un paso en cualquiera "
        "de las 8 direcciones o salta como caballo sin las ataduras del Rey."
    ),
    CAMEL: (
        "Camello de Guerra (Saltador 3x1): ejecuta una L alargada de 3x1 casillas, "
        "permaneciendo siempre en el mismo color de casilla."
    ),
    LION: (
        "León Real (Artillería de salto libre): salta sobre una pieza en las 8 "
        "direcciones de la Reina y aterriza en cualquier casilla posterior de la línea."
    ),
    ZEBRA: (
        "Cebra de Flanqueo (Saltador exótico 3x2): salta barreras defensivas "
        "mediante una L abierta de 3x2 casillas."
    ),
    PHOENIX: (
        "Fénix Inmortal (Paso ortogonal + Salto 2x2): se desplaza un paso en "
        "línea recta o salta exactamente dos casillas en diagonal."
    ),
}

GENERIC_BIOS = {
    WHITE: {
        KING: "Rey cruzado de la Orden del Alba.",
        QUEEN: "Reina soberana de las fortalezas blancas del Alba.",
        ROOK: "Bastión templario de piedra blanca que protege las líneas del reino.",
        BISHOP: "Prelado consejero que guía a las tropas con sabiduría sagrada.",
        KNIGHT: "Caballero templario pesado cuya carga rompe las filas enemigas.",
        **FAIRY_GENERIC_BIOS,
    },
    BLACK: {
        KING: "Soberano nocturno de las montañas de Valaquia.",
        QUEEN: "Reina de las sombras y señora de los castillos góticos.",
        ROOK: "Castillo escarpado sobre los riscos que domina el paso.",
        BISHOP: "Conde nocturno versado en los secretos de la Orden del Dragón.",
        KNIGHT: "Jinete nocturno que ataca sin previo aviso desde la niebla.",
        **FAIRY_GENERIC_BIOS,
    },
    RED: {
        KING: "Rey guerrero de las falanges de Esparta.",
        QUEEN: "Reina de hierro y bronce cuyo mandato guía a las legiones.",
        ROOK: "Fortaleza acorazada de bronce y hierro, imparable en línea recta.",
        BISHOP: "Oráculo marcial que lee los presagios antes del combate.",
        KNIGHT: "Centurión a caballo forjado para aplastar los flancos rivales.",
        **FAIRY_GENERIC_BIOS,
    },
    GREEN: {
        KING: "Gran caudillo de los clanes libres del bosque.",
        QUEEN: "Reina guerrera cuyas órdenes despiertan la furia de las tribus.",
        ROOK: "Bastión de roble y piedra levantado por los antiguos clanes.",
        BISHOP: "Druida sabio de los bosques sagrados y círculos de piedra.",
        KNIGHT: "Jinete celta veloz capaz de sortear cualquier obstáculo.",
        **FAIRY_GENERIC_BIOS,
    },
}

VETERAN_TRAITS = {
    PAWN: "Veterano (2+ bajas): puede avanzar lateralmente y embestir de frente.",
    KNIGHT: "Veterano (2+ bajas): puede dar un paso ortogonal corto.",
    BISHOP: "Veterano (2+ bajas): puede dar un paso ortogonal corto.",
    ROOK: "Veterano (2+ bajas): puede dar un paso diagonal corto.",
    QUEEN: "Veterano (2+ bajas): domina también el salto del jinete.",
    FALCON: "Veterano (2+ bajas): añade un paso ortogonal corto a su vuelo.",
    ELEPHANT: "Veterano (2+ bajas): añade un paso diagonal corto a su embestida.",
    AMAZON: "Veterano (2+ bajas): añade el salto arcano 2x2 a su repertorio.",
    GRASSHOPPER: "Veterano (2+ bajas): puede dar un paso ortogonal sin necesidad de saltar.",
    NIGHTRIDER: "Veterano (2+ bajas): puede dar un paso ortogonal corto.",
    CENTAUR: "Veterano (2+ bajas): añade el salto diagonal 2x2.",
    CAMEL: "Veterano (2+ bajas): puede cambiar el color de su casilla con un paso ortogonal.",
    LION: "Veterano (2+ bajas): puede dar un paso corto de Rey sin necesidad de saltar.",
    ZEBRA: "Veterano (2+ bajas): puede dar un paso ortogonal corto.",
    PHOENIX: "Veterano (2+ bajas): añade el paso diagonal corto de 1 casilla.",
}


def character_bio(piece: Piece) -> str:
    if piece.name in OFFICER_BIOS:
        base = OFFICER_BIOS[piece.name]
    elif piece.kind == PAWN:
        base = PAWN_BIOS.get(piece.color, PAWN_BIOS[WHITE])
    else:
        color_bios = GENERIC_BIOS.get(piece.color, GENERIC_BIOS[WHITE])
        base = color_bios.get(piece.kind, PAWN_BIOS.get(piece.color, PAWN_BIOS[WHITE]))
    if piece.veteran and piece.kind in VETERAN_TRAITS:
        return f"{base}\n★ {VETERAN_TRAITS[piece.kind]}"
    if piece.kills == 1 and piece.kind != KING:
        return f"{base}\nBajas en combate: 1 (a 1 baja del rango Veterano)."
    return base
