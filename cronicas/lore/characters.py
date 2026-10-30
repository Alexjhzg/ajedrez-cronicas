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
    (KNIGHT, "Caballo", "Caballero Hospitalario"),
    (BISHOP, "Alfil", "Prelado del Sol"),
    (QUEEN, "Reina Leonor", "Soberana de las Catedrales"),
    (KING, "Rey Balduino", "Rey Cruzado del Alba"),
    (BISHOP, "Alfil", "Prelada del Sol"),
    (KNIGHT, "Caballo", "Caballero Hospitalario"),
    (ROOK, "Torre", "Bastión Templario"),
]

BLACK_BACK = [
    (ROOK, "Torre", "Ciudadela de los Cárpatos"),
    (KNIGHT, "Caballo", "Húsar de la Noche"),
    (BISHOP, "Alfil", "Boyardo del Eclipse"),
    (QUEEN, "Reina Carmila", "Condesa de la Sangre Nocturna"),
    (KING, "Rey Vladimir", "Voivoda del Eclipse"),
    (BISHOP, "Alfil", "Boyardo del Eclipse"),
    (KNIGHT, "Caballo", "Húsar de la Noche"),
    (ROOK, "Torre", "Ciudadela de los Cárpatos"),
]

RED_BACK = [
    (ROOK, "Torre", "Castrum Pretoriano"),
    (KNIGHT, "Caballo", "Equite Cataphracto"),
    (BISHOP, "Alfil", "Augur de Marte"),
    (QUEEN, "Reina Gorgo", "Augusta de Hierro y Bronce"),
    (KING, "Rey Leónidas", "Éforo de la Falange Carmesí"),
    (BISHOP, "Alfil", "Augur de Belona"),
    (KNIGHT, "Caballo", "Equite Cataphracto"),
    (ROOK, "Torre", "Castrum Pretoriano"),
]

GREEN_BACK = [
    (ROOK, "Torre", "Dun Megalítico"),
    (KNIGHT, "Caballo", "Auriga de Guerra Celta"),
    (BISHOP, "Alfil", "Archidruida del Robledal"),
    (QUEEN, "Reina Boudica", "Reina Guerrera de los Icenos"),
    (KING, "Rey Vercingétorix", "Gran Caudillo de los Clanes"),
    (BISHOP, "Alfil", "Druidesa del Muérdago"),
    (KNIGHT, "Caballo", "Auriga de Guerra Celta"),
    (ROOK, "Torre", "Dun Megalítico"),
]

WHITE_ELEPHANT = (ELEPHANT, "Elefante", "Coloso de Ultramar")
BLACK_ELEPHANT = (ELEPHANT, "Elefante", "Coloso de Valaquia")
RED_ELEPHANT = (ELEPHANT, "Elefante", "Elefante Pírrico")
GREEN_ELEPHANT = (ELEPHANT, "Elefante", "Behemot Pictórico")

WHITE_PAWNS = [("Peón", "Cruzado del Alba")] * 12
BLACK_PAWNS = [("Peón", "Guardia de la Empalizada")] * 12
RED_PAWNS = [("Peón", "Hoplita de la Falange")] * 12
GREEN_PAWNS = [("Peón", "Guerrero Gaisata")] * 12

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
        "El Rey de la Máscara de Plata. Inspirado en los monarcas cruzados de "
        "Ultramar, gobierna desde las catedrales de mármol blanco del Alba; "
        "aunque su cuerpo sufre bajo la armadura, su fe y su genio táctico "
        "jamás han conocido la derrota."
    ),
    "Reina Leonor": (
        "Alta soberana franco-normanda de las cortes solares. Diplomática, "
        "mecenas de trovadores y estratega implacable que dirigió dos cruzadas; "
        "su palabra moviliza órdenes de caballería enteras."
    ),
    "Rey Vladimir": (
        "Voivoda supremo de las cumbres de Valaquia y caballero juramentado de "
        "la Orden del Dragón. Empaló los estandartes de los invasores en los "
        "pasos de los Cárpatos y pactó con la noche eterna para que ningún "
        "imperio someta su trono."
    ),
    "Reina Carmila": (
        "Condesa inmortal de las criptas de Estiria y Transilvania. Envuelta en "
        "terciopelo negro y niebla carmesí, conoce los secretos de la sangre "
        "antigua y desarma la voluntad de los generales enemigos antes del alba."
    ),
    "Rey Leónidas": (
        "Rey guerrero de linaje heráclida, criado en la agogé del acero y el "
        "escudo. Al frente de sus falanges carmesíes y legiones de hierro, "
        "jamás pregunta cuántos son los enemigos, sino dónde están formados."
    ),
    "Reina Gorgo": (
        "Soberana de Esparta y voz del Senado marcial. Su temple gobierna la "
        "patria mientras las legiones marchan; fue ella quien entregó el escudo "
        "real con el mandato inmortal: «Vuelve con él o sobre él»."
    ),
    "Rey Vercingétorix": (
        "Gran caudillo arverno que unificó a las tribus celtas de los bosques "
        "bajo el juramento del torque de oro. Maestro de la guerra de emboscadas "
        "y los duns fortificados, defiende la libertad ancestral de la espesura."
    ),
    "Reina Boudica": (
        "Reina guerrera de los clanes britanos. Conduce su carro de guerra con "
        "el cabello al viento y la piel trazada en azul de glasto; su grito de "
        "batalla ha reducido a cenizas las colonias de los imperios invasores."
    ),
}

PAWN_BIOS = {
    WHITE: (
        "Cruzado juramentado de las encomiendas franco-normandas. Marcha con "
        "tabardo blanco y escudo solar, soñando con ser armado caballero en el "
        "altar mayor de la catedral."
    ),
    BLACK: (
        "Guardia fronterizo de los pasos de Valaquia. Avanza entre la niebla de "
        "los Cárpatos con alabarda y antorcha apagada, fiel hasta la muerte al "
        "Voivoda del Eclipse."
    ),
    RED: (
        "Hoplita y legionario de primera línea. Avanza tras el muro de escudos "
        "de bronce y hierro (phalanx y testudo) con lanza larga y espada corta."
    ),
    GREEN: (
        "Guerrero gaisata de los clanes celtas, con el cuerpo pintado en "
        "espirales de glasto azul, escudo ovalado y venablo de fresno."
    ),
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
        KING: (
            "Rey cruzado del Alba. Mientras su corona resista sobre el tablero, "
            "las órdenes templarias y hospitalarias no retrocederán."
        ),
        QUEEN: (
            "Soberana franco-normanda de la Orden del Alba. Donde ella alza su "
            "estandarte solar, las caballerías abren paso."
        ),
        ROOK: (
            "Bastión templario de piedra caliza alzado como el Krak de los "
            "Caballeros. Sus almenas góticas protegen las líneas del reino."
        ),
        BISHOP: (
            "Prelado del Sacro Imperio versado en los códices iluminados y la "
            "geometría sagrada de las grandes catedrales."
        ),
        KNIGHT: (
            "Caballero hospitalario en armadura de placas y barda blanca. Su "
            "carga frontal lanza en ristre quiebra cualquier línea."
        ),
        **FAIRY_GENERIC_BIOS,
    },
    BLACK: {
        KING: (
            "Voivoda del Eclipse. Su corona de hierro negro gobierna los pasos "
            "montañosos de Valaquia y Transilvania."
        ),
        QUEEN: (
            "Condesa nocturna de los Cárpatos. Teje el destino con niebla y "
            "sangre antigua desde las criptas del castillo."
        ),
        ROOK: (
            "Ciudadela escarpada sobre los riscos de Transilvania, inspirada en "
            "el Castillo de Poenari. Sus torres vigilan los desfiladeros."
        ),
        BISHOP: (
            "Boyardo y cronista oculto de la corte de Valaquia. Domina los "
            "secretos de la Orden del Dragón y el terror nocturno."
        ),
        KNIGHT: (
            "Húsar nocturno de los Cárpatos. Cabalga corceles negros a través "
            "de la niebla sin ser visto hasta el instante del choque."
        ),
        **FAIRY_GENERIC_BIOS,
    },
    RED: {
        KING: (
            "Rey espartano de la Forja Carmesí. Su escudo de bronce y su lanza "
            "dictan la ley marcial de la falange."
        ),
        QUEEN: (
            "Augusta de Esparta y Roma. Su voz en el Senado y en el campo "
            "recuerda que un guerrero vuelve con su escudo o sobre él."
        ),
        ROOK: (
            "Castrum pretoriano y torre de asedio romana recubierta de bronce "
            "y hierro, imparable en línea recta."
        ),
        BISHOP: (
            "Augur marcial del colegio de Marte. Lee los auspicios de guerra y "
            "dirige el fuego de los onagros y escorpiones."
        ),
        KNIGHT: (
            "Equite cataphracto con coraza escamada y penacho carmesí, forjado "
            "para aplastar los flancos enemigos."
        ),
        **FAIRY_GENERIC_BIOS,
    },
    GREEN: {
        KING: (
            "Gran caudillo de la Confederación Celta, guardián del torque de "
            "oro y de los robledales sagrados."
        ),
        QUEEN: (
            "Reina guerrera de los clanes britanos cuyos cánticos de batalla "
            "despiertan la furia de las tribus."
        ),
        ROOK: (
            "Dun megalítico y muralla gala (murus gallicus) de roble y piedra "
            "viva que resiste el hierro y el fuego."
        ),
        BISHOP: (
            "Archidruida de los círculos megalíticos que custodia los nemetones "
            "y canaliza la fuerza ancestral de la tierra."
        ),
        KNIGHT: (
            "Auriga de carro de guerra celta y jinete galo capaz de sortear "
            "cualquier obstáculo del bosque."
        ),
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
