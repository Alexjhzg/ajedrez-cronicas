"""Generación de la crónica viva de cada partida (duelos, 4 frentes e Imperio 12x12)."""

from __future__ import annotations

import random
from dataclasses import dataclass

from ..engine import (
    AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FALCON, GRASSHOPPER,
    GREEN, KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, QUEEN, RED, ROOK,
    WHITE, ZEBRA, Game, Move,
)
from .factions import FACTIONS, faction_name
from .geography import square_name

QUIET_FLAVOR = {
    PAWN: [
        "El barro mancha sus botas, pero no detiene su paso.",
        "El pueblo observa en silencio; cada escudero es una promesa.",
        "Un juramento susurrado acompaña sus pasos.",
    ],
    KNIGHT: [
        "Las alas del grifo agitan la ceniza del camino.",
        "El viento silba entre las plumas y la armadura.",
        "Desde las alturas, el jinete estudia el tablero como un mapa de guerra.",
    ],
    BISHOP: [
        "Un susurro arcano recorre las piedras a su paso.",
        "El aire huele a tormenta y a tinta antigua.",
        "Sus dedos trazan signos que la luz no debería conocer.",
    ],
    ROOK: [
        "La tierra tiembla bajo su peso milenario.",
        "Las almenas crujen, como si la fortaleza caminara.",
        "Cada paso deja una grieta en el empedrado.",
    ],
    QUEEN: [
        "La luz del reino se inclina ante su voluntad.",
        "Su sombra se alarga más de lo que la luna permite.",
        "Nadie osa mirarla dos veces.",
    ],
    KING: [
        "Los estandartes se inclinan al paso del soberano.",
        "El trono queda atrás, pero su peso lo acompaña.",
        "Los guardias redoblan la vigilancia.",
    ],
    FALCON: [
        "El halcón corta el viento en diagonal y cambia de rumbo en pleno vuelo.",
        "Sus alas proyectan una sombra veloz sobre las columnas enemigas.",
    ],
    ELEPHANT: [
        "Cada paso suyo hace temblar las losas del tablero.",
        "El coloso avanza con la paciencia de una montaña que ha decidido moverse.",
        "Los estandartes tiemblan cuando sus colmillos cruzan la penumbra.",
    ],
    AMAZON: [
        "La Amazonas avanza rodeada de un aura de fuego y tormenta; ningún ángulo le es ajeno.",
        "Las filas enemigas retroceden al sentir el paso de la guerrera suprema.",
    ],
    GRASSHOPPER: [
        "Con un impulso sobrenatural, salta por encima de la formación y aterriza en silencio.",
        "El viento silba cuando cruza de un salto la silueta de otra pieza.",
    ],
    NIGHTRIDER: [
        "El Noctámbulo encadena zancadas imposibles entre las sombras del campo.",
        "Su corcel fantasmal pisa tres veces el aire antes de tocar la piedra.",
    ],
    CENTAUR: [
        "Sus cascos de bronce resuenan con firmeza; domina cada palmo a su alrededor.",
        "Mitad caballero, mitad corcel de guerra, cierra el paso en la vanguardia.",
    ],
    CAMEL: [
        "El camello de guerra sortea las trincheras con una zancada larga e implacable.",
        "Avanza con paso largo y oblicuo, fiel al color de su estandarte.",
    ],
    LION: [
        "El león ruge, salta sobre la línea frontal y planea hasta su presa lejana.",
        "Su melena corta el aire mientras sobrevuela el obstáculo hacia la retaguardia.",
    ],
    ZEBRA: [
        "Con un salto oblicuo de gran abertura, flanquea las defensas sin esfuerzo.",
        "Cruza de un solo brinco las barreras que detendrían a cualquier corcel.",
    ],
    PHOENIX: [
        "Una estela de brasas sagradas marca su salto sobre el tablero.",
        "El ave inmortal se desliza con gracia arcana entre las líneas de batalla.",
    ],
}

CAPTURE_FLAVOR = {
    PAWN: [
        "El escudero clava su lanza con la furia de quien no tiene nada que perder.",
        "Un golpe torpe, pero certero, basta para abrir la primera herida.",
    ],
    KNIGHT: [
        "El grifo cae en picada y sus garras no perdonan.",
        "El jinete pasa como una sombra y deja el campo sembrado de acero.",
    ],
    BISHOP: [
        "Una palabra prohibida prende fuego al aire.",
        "El magíster dibuja un signo y la armadura enemiga se resquebraja.",
    ],
    ROOK: [
        "El impacto hace temblar el tablero entero.",
        "La fortaleza avanza como un alud de piedra y hierro.",
    ],
    QUEEN: [
        "Un solo gesto suyo basta para cambiar el destino de la batalla.",
        "La reina no pide permiso; el campo se rinde a su paso.",
    ],
    KING: [
        "El soberano no debería luchar, pero su acero es tan antiguo como su corona.",
        "El rey rompe la formación enemiga con una furia que nadie recordaba.",
    ],
    FALCON: [
        "El halcón desciende desde las nubes y abate a su presa antes de que alce el escudo.",
        "Un picado diagonal seguido de un quiebre imposible derriba al enemigo.",
    ],
    ELEPHANT: [
        "El impacto de sus colmillos parte el aire y la formación enemiga.",
        "La montaña de guerra embiste y no deja piedra sobre piedra.",
    ],
    AMAZON: [
        "La Amazonas desata una tormenta de lanza y espada que barre toda defensa.",
        "Ninguna armadura soporta el embate de la campeona imperial.",
    ],
    GRASSHOPPER: [
        "Salta por encima del escudo frontal y cae directamente sobre su objetivo.",
        "Una emboscada aérea fulminante justo detrás de la línea de choque.",
    ],
    NIGHTRIDER: [
        "Surge desde el otro extremo del campo en una cadena de saltos letales.",
        "El Noctámbulo atraviesa la penumbra y descarga su lanza sin previo aviso.",
    ],
    CENTAUR: [
        "El Centauro arrolla a su rival con el peso combinado de lanza y pezuñas.",
        "Nadie escapa a su radio de guardia; el golpe resuena en todo el valle.",
    ],
    CAMEL: [
        "Su salto alargado supera la muralla y sorprende al defensor por el flanco.",
        "Cruza tres losas de un brinco y derriba el estandarte enemigo.",
    ],
    LION: [
        "El León salta sobre la trinchera y se desploma como un meteoro sobre su presa.",
        "Sus garras desgarran la retaguardia enemiga tras un salto colosal.",
    ],
    ZEBRA: [
        "Un salto en ángulo abierto burla toda cobertura y abate al enemigo.",
        "La Cebra cae desde el flanco exterior rompiendo la formación.",
    ],
    PHOENIX: [
        "El Fénix envuelve a su enemigo en llamas al aterrizar de su salto diagonal.",
        "Un destello ígneo consume la casilla y renace entre las cenizas del caído.",
    ],
}

CHECK_PHRASES = [
    "El Rey enemigo palidece: ¡jaque!",
    "Las campanas de la torre redoblan: ¡el Rey está en jaque!",
    "Un escalofrío recorre el trono: ¡jaque!",
    "La guardia enemiga se rompe en gritos: ¡jaque!",
    "El acero brilla demasiado cerca de la corona: ¡jaque!",
]

PROMOTION_ROLE = {
    AMAZON: "una Amazonas Imperial",
    QUEEN: "una Dama de guerra",
    ELEPHANT: "un Elefante de Asedio",
    FALCON: "un Halcón de Guerra",
    ROOK: "una Torre viviente",
    BISHOP: "un Alfil consagrado",
    KNIGHT: "un Caballo de tormenta",
}

PROMOTED_TITLE = {
    AMAZON: "Amazonas Imperial",
    QUEEN: "Dama de Guerra",
    ELEPHANT: "Coloso de Asedio",
    FALCON: "Halcón Consagrado",
    ROOK: "Torre de Asedio",
    BISHOP: "Alfil Consagrado",
    KNIGHT: "Caballo de Tormenta",
}


@dataclass
class LoreEntry:
    heading: str
    text: str
    tag: str = "move"


def to_roman(number: int) -> str:
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = []
    for value, symbol in values:
        while number >= value:
            result.append(symbol)
            number -= value
    return "".join(result) or "I"


def prologue(
    vs_ai: bool,
    difficulty: str = "",
    elephant: bool = False,
    fog: bool = False,
    player_color: str = WHITE,
    enemy_color: str = BLACK,
) -> LoreEntry:
    p_info = FACTIONS.get(player_color, FACTIONS[WHITE])
    e_info = FACTIONS.get(enemy_color, FACTIONS[BLACK])
    p_name = p_info["name"]
    e_name = e_info["name"]
    officers = (
        "un oficial arcano, un elefante de guerra" if elephant else "dos oficiales arcanos"
    )
    text = (
        "En la era en que las piedras recuerdan y los cuervos hablan, el reino de "
        f"Aethelgard se fractura en múltiples frentes. {p_name} ({p_info['culture']}, "
        f"liderada por {p_info['sovereigns']}) despliega sus estandartes en el sur "
        f"mientras {e_name} ({e_info['culture']}, bajo {e_info['sovereigns']}) "
        "marcha desde el norte.\n\n"
        f"Ocho unidades de vanguardia, {officers}, dos jinetes, dos baluartes, una "
        "soberana y un monarca aguardan en cada bando. Cada paso será una página; "
        "cada caída, una herida en la historia."
    )
    if elephant:
        text += (
            "\n\nUn Elefante de Guerra ocupa el lugar de un oficial arcano en cada "
            "bando: combina la embestida en línea recta de una torre con el salto "
            "del caballo."
        )
    if fog:
        text += (
            "\n\nUna niebla de guerra cubre el tablero. Solo verás las casillas "
            "que tus propias piezas vigilen; lo que aceche fuera de su alcance "
            "permanecerá oculto."
        )
    if vs_ai:
        oracle = {
            "Escudero": f"Al otro lado del tablero, un comandante novel guía a {e_name}.",
            "Caballero": f"Al otro lado, un general curtido comanda a {e_name}.",
            "Archimago": f"Al otro lado, un estratega que lee el porvenir dirige a {e_name}.",
        }.get(difficulty, "Al otro lado, el Oráculo Umbrío acecha.")
        text += f"\n\n{oracle}\n\nQue comience la crónica."
    else:
        text += "\n\nDos voluntades se enfrentan sobre el tablero.\n\nQue comience la crónica."
    return LoreEntry("Prólogo · Los estandartes enfrentados", text, "prologue")


def imperial_prologue(
    vs_ai: bool,
    difficulty: str = "",
    fog: bool = False,
    player_color: str = WHITE,
    enemy_color: str = BLACK,
) -> LoreEntry:
    p_name = faction_name(player_color)
    e_name = faction_name(enemy_color)
    text = (
        "Las crónicas mayores se abren sobre el Gran Tablero Imperial de 144 losas "
        f"(12x12). {p_name} y {e_name} convocan a las diez órdenes legendarias del "
        "Códice de Aethelgard.\n\n"
        "En la primera línea brillan Halcones (Alfil+Caballo), Elefantes (Torre+Caballo), "
        "la temida Amazonas (Reina+Caballo), Leones de artillería y Noctámbulos de "
        "salto perpetuo. Delante de ellos, Centauros, Fénix, Saltamontes, Camellos y "
        "Cebras escoltan la muralla de doce escuderos."
    )
    if fog:
        text += (
            "\n\nLa niebla de guerra envuelve la inmensidad del campo imperial: "
            "solo las casillas bajo el alcance de tus legiones serán visibles."
        )
    if vs_ai:
        text += (
            f"\n\nEl Oráculo Umbrío ({difficulty or 'Caballero'}) dirige las legiones "
            f"de {e_name}.\n\nQue comience la Gran Crónica Imperial."
        )
    else:
        text += "\n\nDos emperadores frente a frente.\n\nQue comience la Gran Crónica Imperial."
    return LoreEntry("Prólogo · El Gran Tablero Imperial (12x12)", text, "prologue")


def four_fronts_prologue(
    vs_ai: bool,
    difficulty: str = "",
    elephant: bool = False,
    fog: bool = False,
    player_color: str = WHITE,
) -> LoreEntry:
    p_name = faction_name(player_color)
    text = (
        "Las trompetas de los cuatro puntos cardinales resuenan al unísono. "
        "La Orden del Alba, la Forja Carmesí, la Legión del Eclipse y el Pacto "
        "de la Espesura convergen sobre la encrucijada central de Aethelgard.\n\n"
        f"Comandas a {p_name} desde el frente sur. Tres ejércitos rivales "
        "asedian desde el oeste, el norte y el este. Cuando un monarca cae o se "
        "queda sin movimientos legales, su frente entero se desmorona."
    )
    if elephant:
        text += (
            "\n\nCada uno de los cuatro reinos ha desplegado un coloso de guerra "
            "en su flanco de vanguardia."
        )
    if fog:
        text += (
            "\n\nLa niebla de guerra envuelve los cuatro frentes: solo verás "
            "aquello que tus propias unidades alcancen a divisar."
        )
    if vs_ai:
        text += (
            f"\n\nTres comandantes regidos por el Oráculo ({difficulty or 'Caballero'}) "
            "disputan la corona al mismo tiempo.\n\nQue comience la Guerra de los Cuatro Frentes."
        )
    else:
        text += "\n\nCuatro tronos, un solo campo.\n\nQue comience la Guerra de los Cuatro Frentes."
    return LoreEntry("Prólogo · Guerra de los Cuatro Frentes", text, "prologue")


def _check_sentence() -> str:
    return random.choice(CHECK_PHRASES)


def narrate_move(
    move: Move,
    game: Game,
    check: bool,
    mate: bool,
    chapter: int,
) -> LoreEntry:
    piece = move.moved
    assert piece is not None
    dest = square_name(move.tr, move.tc, game.size)
    origin = square_name(move.fr, move.fc, game.size)
    mover = piece.name
    victim = move.captured.name if move.captured else None
    flavor = random.choice(QUIET_FLAVOR.get(piece.kind, QUIET_FLAVOR[PAWN]))
    capture_flavor = random.choice(CAPTURE_FLAVOR.get(piece.kind, CAPTURE_FLAVOR[PAWN]))
    check_text = f" {_check_sentence()}" if check and not mate else ""

    elim_text = ""
    if getattr(move, "eliminated_factions", ()):
        names = [faction_name(c) for c in move.eliminated_factions]
        elim_text = f" ¡El frente de {', '.join(names)} se derrumba y sus tropas abandonan el campo!"

    if mate:
        if victim:
            body = random.choice([
                f"El acero de {mover} encuentra a {victim} en {dest}. "
                f"{capture_flavor}{elim_text} El último estandarte cae: ¡jaque mate!",
                f"En {dest}, {mover} derriba a {victim} y cierra el cerco.{elim_text} "
                f"No hay escudo, ni huida, ni milagro: ¡jaque mate!",
            ])
        else:
            body = random.choice([
                f"{mover} cierra el cerco en {dest}.{elim_text} No hay escudo, ni huida, "
                f"ni milagro: ¡jaque mate!",
                f"En {dest}, la última defensa se quiebra.{elim_text} {mover} alza su arma "
                f"bajo un cielo que deja de respirar: ¡jaque mate!",
            ])
        return LoreEntry(f"Crónica {to_roman(chapter)} · El último estandarte", body, "mate")

    if move.promotion:
        role = PROMOTION_ROLE.get(move.promotion, "un campeón consagrado")
        capture_line = (
            f" Antes de ascender, su acero derriba a {victim}." if victim else ""
        )
        body = random.choice([
            f"{mover} alcanza el altar de coronación en {dest}. La piedra arde y "
            f"renace como {role}.{capture_line}{elim_text}{check_text}",
            f"En {dest}, el último escalón se ilumina. {mover} deja atrás su juramento "
            f"de escudero y se alza como {role}.{capture_line}{elim_text}{check_text}",
        ])
        return LoreEntry(f"Crónica {to_roman(chapter)} · El ascenso de {mover}", body, "promo")

    if move.castle:
        row = move.tr
        rook_col = 5 if move.castle == "K" else 3
        rook = game.grid[row][rook_col]
        rook_name = rook.name if rook else "el centinela"
        side = "flanco del rey" if move.castle == "K" else "flanco de la reina"
        body = random.choice([
            f"{mover} ordena cerrar filas: se repliega hacia {dest} mientras "
            f"{rook_name} ocupa su puesto tras las murallas. ¡Enroque en el {side}!",
            f"Las trompetas suenan dos veces. {mover} se refugia en {dest} y "
            f"{rook_name} sella la muralla. ¡Enroque en el {side}!",
        ])
        return LoreEntry(f"Crónica {to_roman(chapter)} · Muros y coronas", body, "castle")

    if move.is_en_passant and victim:
        body = (
            f"La niebla se abre: {mover} sorprende a {victim} en {dest}, "
            f"cortándole la retirada. ¡Emboscada en las aguas turbias!{elim_text}{check_text}"
        )
        return LoreEntry(f"Crónica {to_roman(chapter)} · Emboscada en la niebla", body, "capture")

    if victim:
        vet_note = ""
        if (
            move.placed is not None
            and move.placed.veteran
            and not piece.veteran
        ):
            vet_note = (
                f" ¡{mover} alcanza el rango de Veterano tras su segunda victoria!"
            )
        body = random.choice([
            f"¡{mover} se abalanza sobre {victim} en {dest}! {capture_flavor} "
            f"El primer grito de la guerra rompe el silencio.{vet_note}{elim_text}{check_text}",
            f"En {dest}, el acero de {mover} encuentra a {victim}. "
            f"{capture_flavor}{vet_note}{elim_text}{check_text}",
            f"{mover} desafía a {victim} y lo derriba en {dest}. "
            f"{capture_flavor}{vet_note}{elim_text}{check_text}",
            f"La tierra bebe sangre en {dest}: {mover} vence a {victim}. "
            f"{capture_flavor}{vet_note}{elim_text}{check_text}",
        ])
        tag = "check" if check else "capture"
        heading = "El trono tiembla" if check else f"Sangre en {dest}"
        return LoreEntry(f"Crónica {to_roman(chapter)} · {heading}", body, tag)

    if check:
        body = random.choice([
            f"{mover} avanza de {origin} a {dest}. {flavor}{elim_text}{check_text}",
            f"Las crónicas registran el paso de {mover} por {dest}. {flavor}{elim_text}{check_text}",
            f"{mover} toma posición en {dest} sin derramar sangre… por ahora. "
            f"{flavor}{elim_text}{check_text}",
        ])
        return LoreEntry(f"Crónica {to_roman(chapter)} · El trono tiembla", body, "check")

    body = random.choice([
        f"{mover} parte de {origin} y avanza hacia {dest}. {flavor}{elim_text}",
        f"Las crónicas registran el paso de {mover} por {dest}. {flavor}{elim_text}",
        f"Bajo un cielo de ceniza, {mover} toma posición en {dest}. {flavor}{elim_text}",
        f"{mover} se interna en {dest} sin derramar sangre… todavía. {flavor}{elim_text}",
    ])
    return LoreEntry(f"Crónica {to_roman(chapter)} · El paso de {mover}", body, "move")


def fog_entry(chapter: int) -> LoreEntry:
    body = random.choice([
        "Algo se mueve más allá de la niebla. El tablero respira, pero no revela "
        "sus secretos.",
        "Un roce de acero y un paso apagado. Cuando la niebla se abre, solo queda "
        "la sospecha de una pieza en marcha.",
        "Las antorchas parpadean. En algún lugar del tablero, una voluntad oculta "
        "acaba de moverse.",
        "La niebla traga el sonido de una jugada. Ni el nombre ni el destino "
        "cruzan hasta tu lado del campo.",
    ])
    return LoreEntry(f"Crónica {to_roman(chapter)} · Voces en la niebla", body, "fog")


def ambient_entry(size: int = 8) -> LoreEntry:
    r, c = random.randrange(size), random.randrange(size)
    loc = square_name(r, c, size)
    line = random.choice([
        f"Los cuervos sobrevuelan {loc}. Nada ha muerto aún… esta noche.",
        f"Bajo {loc}, una raíz antigua bebe la sangre derramada.",
        f"Los estandartes ondean sobre {loc}; el viento huele a hierro.",
        f"Un bardo canta en {loc}. Su canción habla de reyes que caerán.",
        f"En {loc}, la luna se oculta tras una nube que no debería existir.",
        f"Alguien ha encendido una vela en {loc}. Nadie sabe quién.",
    ])
    return LoreEntry("Eco del reino", line, "ambient")


def epilogue(result: dict) -> LoreEntry:
    rtype = result.get("type")
    winner = result.get("winner")

    if rtype == "checkmate" and winner == WHITE:
        return LoreEntry(
            "Epílogo · El Trono de la Luz",
            "El último estandarte rival cae. La Orden del Alba recupera el Trono "
            "bajo el Rey Balduino y la Reina Leonor.",
            "epilogue",
        )
    if rtype == "checkmate" and winner == BLACK:
        return LoreEntry(
            "Epílogo · La Era del Eclipse",
            "Las defensas enemigas se quiebran en la niebla. El Rey Vladimir y "
            "la Reina Carmila reclaman el Trono para la Legión del Eclipse.",
            "epilogue",
        )
    if rtype == "checkmate" and winner == RED:
        return LoreEntry(
            "Epílogo · El Imperio de Esparta",
            "Las falanges de la Forja Carmesí conquistan el campo. El Rey "
            "Leónidas y la Reina Gorgo alzan sus escudos sobre el Trono.",
            "epilogue",
        )
    if rtype == "checkmate" and winner == GREEN:
        return LoreEntry(
            "Epílogo · El Triunfo de los Clanes",
            "Los clanes celtas reclaman las piedras del trono bajo el Rey "
            "Vercingétorix y la Reina Boudica.",
            "epilogue",
        )
    if rtype == "surrender":
        loser = result.get("loser", WHITE)
        loser_name = faction_name(loser)
        winner_name = faction_name(winner) if winner else "el ejército rival"
        text = (
            f"{loser_name} dobla su estandarte. No hay más cadáveres que contar, "
            f"solo el silencio de una rendición. {winner_name} avanza sin "
            "encontrar resistencia y el trono queda a su merced."
        )
        return LoreEntry("Epílogo · El estandarte doblado", text, "epilogue")
    if rtype == "stalemate":
        return LoreEntry(
            "Epílogo · El equilibrio imposible",
            "Ningún bando puede dar un paso sin condenarse. Las espadas quedan "
            "suspendidas en el aire y los reyes se miran sin parpadear. Los dioses "
            "declaran tablas; Aethelgard respira, pero no olvida.",
            "epilogue",
        )
    if rtype == "material":
        return LoreEntry(
            "Epílogo · Las espadas guardadas",
            "Quedan tan pocas fuerzas sobre el tablero que ninguna victoria sería "
            "posible. Los generales guardan el acero y firman una tregua bajo la "
            "lluvia. Aethelgard gana tiempo; el Eclipse, paciencia.",
            "epilogue",
        )
    return LoreEntry(
        "Epílogo · Cincuenta inviernos",
        "Cincuenta inviernos sin que caiga una sola corona. El tablero se cubre de "
        "polvo y los ejércitos envejecen mirándose. Los dioses declaran tablas para "
        "que la historia pueda seguir su curso.",
        "epilogue",
    )


def result_title(result: dict) -> tuple[str, str, str]:
    """Devuelve (título, subtítulo, color_lógico)."""
    winner = result.get("winner")
    rtype = result.get("type")
    if rtype in ("checkmate", "surrender"):
        if winner == WHITE:
            return "VICTORIA DEL ALBA", "El Trono de la Luz vuelve a brillar", WHITE
        if winner == RED:
            return "VICTORIA DE LA FORJA", "El fuego carmesí domina Aethelgard", RED
        if winner == GREEN:
            return "VICTORIA DEL PACTO", "El bosque ancestral reclama el trono", GREEN
        return "VICTORIA DEL ECLIPSE", "La ceniza cubre Aethelgard", BLACK
    if rtype == "stalemate":
        return "TABLAS", "El equilibrio detiene la guerra", "draw"
    if rtype == "fifty":
        return "TABLAS", "Cincuenta inviernos sin sangre", "draw"
    return "TABLAS", "Las espadas se guardan", "draw"


def result_icon(result: dict) -> str:
    winner = result.get("winner")
    if winner in FACTIONS:
        return FACTIONS[winner]["crest"]
    return "⚖"
