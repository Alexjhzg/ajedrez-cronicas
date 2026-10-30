"""Campañas salvajes: ejércitos aleatorios, terreno hostil y asaltos."""

from __future__ import annotations

import random
from collections import Counter, deque
from dataclasses import dataclass
from typing import Optional

from ..engine import (
    AMAZON, BISHOP, BLACK, CAMEL, CENTAUR, ELEPHANT, FALCON, GRASSHOPPER,
    GREEN, KING, KNIGHT, LION, NIGHTRIDER, PAWN, PHOENIX, QUEEN, RED, ROOK,
    WHITE, ZEBRA, Game, Piece,
)
from .factions import faction_name
from .geography import square_name
from .narrative import LoreEntry, to_roman

WILD_EVENT_EVERY = 6
MAX_TERRAIN = 24

TERRAIN_LABEL = {
    "bosque": "Bosque",
    "rio": "Río",
    "acantilado": "Acantilado",
    "penasco": "Peñasco",
    "ruinas": "Ruinas",
    "empalizada": "Empalizada",
    "escombros": "Escombros",
}

TERRAIN_SINGULAR = {
    "bosque": "bosque",
    "rio": "río",
    "acantilado": "acantilado",
    "penasco": "peñasco",
    "ruinas": "ruina",
    "empalizada": "empalizada",
    "escombros": "escombro",
}

TERRAIN_PLURAL = {
    "bosque": "bosques",
    "rio": "ríos",
    "acantilado": "acantilados",
    "penasco": "peñascos",
    "ruinas": "ruinas",
    "empalizada": "empalizadas",
    "escombros": "escombros",
}

TERRAIN_CONSEQUENCE = {
    "bosque": "Los troncos ocultan la visión y frenan los disparos a través de la espesura.",
    "rio": "El agua profunda frena el avance y acorta el alcance de las piezas que lo cruzan.",
    "acantilado": "La roca partida bloquea el avance y la visión.",
    "penasco": "El peñasco corta el camino y las líneas de tiro.",
    "ruinas": "Los muros caídos ofrecen cobertura: quien los ocupe solo puede ser abatido de cerca.",
    "empalizada": "La empalizada sella el paso con madera y acero.",
    "escombros": "Los escombros sepultan el camino bajo piedra y ceniza.",
}

THEMES = {
    "bosque": {
        "title": "El Bosque de los Susurros",
        "description": (
            "Los árboles de Aethelgard han bebido tanta sangre que ya recuerdan "
            "los nombres de los caídos. Las columnas de guerra avanzan entre "
            "troncos que cierran filas y raíces que devoran caminos."
        ),
    },
    "rio": {
        "title": "La Ribera de Ceniza",
        "description": (
            "El río fronterizo ha crecido con las lluvias de la guerra. Sus "
            "aguas turbias cortan la línea de tiro; solo quedan unos pocos "
            "vados para cruzar."
        ),
    },
    "acantilado": {
        "title": "Los Acantilados del Cuervo",
        "description": (
            "En los Acantilados del Cuervo, la roca se parte como una corona "
            "rota. Los ejércitos deben rodear desfiladeros y peñascos mientras "
            "los cuervos cuentan en silencio a los que caen."
        ),
    },
    "ruinas": {
        "title": "Las Ruinas del Trono",
        "description": (
            "Aquí se alzaba una ciudad antes de que Aethelgard tuviera nombre. "
            "Solo quedan muros partidos y empalizadas de fortuna: cada ruina es "
            "una trinchera y cada sombra, una emboscada."
        ),
    },
    "paso": {
        "title": "El Paso del Dragón",
        "description": (
            "El Paso del Dragón es la única ruta entre las calderas y el trono. "
            "Peñascos y acantilados estrangulan la marcha; quien domine sus "
            "estrechuras dominará la campaña."
        ),
    },
}

_NON_ROYAL_POOLS = {
    ROOK: ["Torre"],
    BISHOP: ["Alfil"],
    ELEPHANT: ["Elefante"],
    FALCON: ["Halcón"],
    AMAZON: ["Amazonas"],
    GRASSHOPPER: ["Saltamontes"],
    NIGHTRIDER: ["Noctámbulo"],
    CENTAUR: ["Centauro"],
    CAMEL: ["Camello"],
    LION: ["León"],
    ZEBRA: ["Cebra"],
    PHOENIX: ["Fénix"],
    KNIGHT: ["Caballo"],
    PAWN: ["Peón"],
}

NAME_POOLS = {
    WHITE: {
        KING: ["Rey Balduino"],
        QUEEN: ["Reina Leonor"],
        **_NON_ROYAL_POOLS,
    },
    BLACK: {
        KING: ["Rey Vladimir"],
        QUEEN: ["Reina Carmila"],
        **_NON_ROYAL_POOLS,
    },
    RED: {
        KING: ["Rey Leónidas"],
        QUEEN: ["Reina Gorgo"],
        **_NON_ROYAL_POOLS,
    },
    GREEN: {
        KING: ["Rey Vercingétorix"],
        QUEEN: ["Reina Boudica"],
        **_NON_ROYAL_POOLS,
    },
}

TITLES = {
    WHITE: {
        KING: "Rey Cruzado del Alba",
        QUEEN: "Soberana de las Catedrales",
        ROOK: "Bastión Templario",
        BISHOP: "Prelado del Sol",
        ELEPHANT: "Coloso de Ultramar",
        FALCON: "Halcón Solar",
        AMAZON: "Paladina del Alba",
        GRASSHOPPER: "Saltamontes de Luz",
        NIGHTRIDER: "Noctámbulo Astral",
        CENTAUR: "Centauro Dorado",
        CAMEL: "Camello de Ultramar",
        LION: "León de Ricardo",
        ZEBRA: "Cebra de Antioquía",
        PHOENIX: "Fénix Sagrado",
        KNIGHT: "Caballero Hospitalario",
        PAWN: "Cruzado del Alba",
    },
    BLACK: {
        KING: "Voivoda del Eclipse",
        QUEEN: "Condesa de la Sangre Nocturna",
        ROOK: "Ciudadela de los Cárpatos",
        BISHOP: "Boyardo del Eclipse",
        ELEPHANT: "Coloso de Valaquia",
        FALCON: "Halcón de los Cárpatos",
        AMAZON: "Amazonas del Dragón",
        GRASSHOPPER: "Saltamontes del Vacío",
        NIGHTRIDER: "Noctámbulo de Transilvania",
        CENTAUR: "Centauro de Hueso",
        CAMEL: "Camello del Danubio",
        LION: "León de Valaquia",
        ZEBRA: "Cebra Espectral",
        PHOENIX: "Fénix de Ceniza",
        KNIGHT: "Húsar de la Noche",
        PAWN: "Guardia de la Empalizada",
    },
    RED: {
        KING: "Éforo de la Falange Carmesí",
        QUEEN: "Augusta de Hierro y Bronce",
        ROOK: "Castrum Pretoriano",
        BISHOP: "Augur de Marte",
        ELEPHANT: "Elefante Pírrico",
        FALCON: "Águila Imperial",
        AMAZON: "Campeona de Esparta",
        GRASSHOPPER: "Velite Saltador",
        NIGHTRIDER: "Explorador Pretoriano",
        CENTAUR: "Centauro de Lacedemonia",
        CAMEL: "Camello de Siria",
        LION: "León de las Termópilas",
        ZEBRA: "Cebra Numidia",
        PHOENIX: "Fénix de Vesta",
        KNIGHT: "Equite Cataphracto",
        PAWN: "Hoplita de la Falange",
    },
    GREEN: {
        KING: "Gran Caudillo de los Clanes",
        QUEEN: "Reina Guerrera de los Icenos",
        ROOK: "Dun Megalítico",
        BISHOP: "Archidruida del Robledal",
        ELEPHANT: "Behemot Pictórico",
        FALCON: "Halcón de Hibernia",
        AMAZON: "Morrigan de la Espesura",
        GRASSHOPPER: "Saltador de los Túmulos",
        NIGHTRIDER: "Jinete de la Cacería Salvaje",
        CENTAUR: "Centauro del Robledal",
        CAMEL: "Corcel de las Tierras Altas",
        LION: "Sabueso de Ulster",
        ZEBRA: "Corcel Pintado de Glasto",
        PHOENIX: "Ave de Beltane",
        KNIGHT: "Auriga de Guerra Celta",
        PAWN: "Guerrero Gaisata",
    },
}

ARMY_LABEL = {
    AMAZON: ("amazonas", "amazonas"),
    QUEEN: ("dama", "damas"),
    ELEPHANT: ("elefante", "elefantes"),
    FALCON: ("halcón", "halcones"),
    LION: ("león", "leones"),
    NIGHTRIDER: ("noctámbulo", "noctámbulos"),
    ROOK: ("torre", "torres"),
    CENTAUR: ("centauro", "centauros"),
    BISHOP: ("alfil", "alfiles"),
    PHOENIX: ("fénix", "fénix"),
    KNIGHT: ("jinete", "jinetes"),
    GRASSHOPPER: ("saltamontes", "saltamontes"),
    CAMEL: ("camello", "camellos"),
    ZEBRA: ("cebra", "cebras"),
    PAWN: ("escudero", "escuderos"),
}

EVENT_SPECS = {
    "bosque": (
        ("La espesura avanza", "bosque", "Los árboles se cierran sobre la marcha"),
        ("Asalto de los leñadores", "empalizada", "Un asalto deja una empalizada clavada en el barro"),
        ("Alud de piedra", "penasco", "Las laderas se desprenden sobre la columna"),
    ),
    "rio": (
        ("Crecida repentina", "rio", "El río se desborda y reclama una nueva orilla"),
        ("Asalto al vado", "escombros", "Un asalto deja el vado cubierto de escombros"),
        ("Derrumbamiento", "ruinas", "Un muro antiguo cae sobre la ribera"),
    ),
    "acantilado": (
        ("Desprendimiento", "acantilado", "La montaña se rompe y derrama roca sobre el camino"),
        ("Roca caída", "penasco", "Un peñasco rueda desde la altura y se clava en el tablero"),
        ("Asalto de la cumbre", "empalizada", "Los defensores levantan una empalizada en la cima"),
    ),
    "ruinas": (
        ("El muro cae", "ruinas", "Un tramo de muralla se desploma entre polvo y ceniza"),
        ("Asalto a la brecha", "escombros", "El asalto deja escombros y armas rotas en la brecha"),
        ("Empalizada de fortuna", "empalizada", "Los ingenieros alzan una empalizada con vigas robadas"),
    ),
    "paso": (
        ("Alud del Dragón", "penasco", "El desfiladero vomita piedra sobre la vanguardia"),
        ("El paso se cierra", "acantilado", "La roca se quiebra y estrecha el paso"),
        ("Asalto de vanguardia", "empalizada", "La vanguardia clava una empalizada para cortar la ruta"),
    ),
}


@dataclass
class WildScenario:
    game: Game
    theme: str
    title: str
    description: str
    terrain_summary: str
    army_summary: str


def terrain_label(kind: str) -> str:
    return TERRAIN_LABEL.get(kind, kind.title())


def _add(
    terrain: dict[tuple[int, int], str], kind: str, r: int, c: int,
) -> None:
    if 2 <= r <= 5 and 0 <= c < 8:
        terrain[(r, c)] = kind


def _trim(
    terrain: dict[tuple[int, int], str],
    limit: int,
    rng: random.Random,
) -> dict[tuple[int, int], str]:
    if len(terrain) <= limit:
        return terrain
    keep = set(rng.sample(list(terrain), limit))
    return {pos: kind for pos, kind in terrain.items() if pos in keep}


def _forest_terrain(rng: random.Random) -> dict[tuple[int, int], str]:
    terrain: dict[tuple[int, int], str] = {}
    for _ in range(rng.randint(5, 7)):
        cr, cc = rng.randint(2, 5), rng.randrange(8)
        offsets = [(0, 0)]
        for _ in range(rng.randint(1, 2)):
            offsets.append(rng.choice((
                (-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, -1),
            )))
        for dr, dc in offsets:
            _add(terrain, "bosque", cr + dr, cc + dc)
    for _ in range(rng.randint(1, 3)):
        _add(terrain, "penasco", rng.randint(2, 5), rng.randrange(8))
    return _trim(terrain, 15, rng)


def _river_terrain(rng: random.Random) -> dict[tuple[int, int], str]:
    terrain: dict[tuple[int, int], str] = {}
    if rng.random() < 0.55:
        col = rng.randint(2, 5)
        ford = rng.randint(2, 5)
        for r in range(2, 6):
            if r == ford:
                continue
            _add(terrain, "rio", r, col)
            if rng.random() < 0.4:
                _add(terrain, "rio", r, col + rng.choice((-1, 1)))
    else:
        row = rng.randint(2, 5)
        ford = rng.randrange(1, 7)
        for c in range(1, 7):
            if c == ford:
                continue
            _add(terrain, "rio", row, c)
            if rng.random() < 0.25:
                _add(terrain, "rio", row + rng.choice((-1, 1)), c)
    for _ in range(rng.randint(2, 4)):
        kind = rng.choice(("ruinas", "penasco", "empalizada", "escombros"))
        _add(terrain, kind, rng.randint(2, 5), rng.randrange(8))
    return _trim(terrain, 15, rng)


def _cliff_terrain(rng: random.Random) -> dict[tuple[int, int], str]:
    terrain: dict[tuple[int, int], str] = {}
    for _ in range(rng.randint(4, 6)):
        cr, cc = rng.randint(2, 5), rng.randrange(8)
        kind = rng.choice(("acantilado", "acantilado", "penasco"))
        for _ in range(rng.randint(1, 3)):
            _add(
                terrain, kind, cr + rng.choice((-1, 0, 1)),
                cc + rng.choice((-1, 0, 1)),
            )
    for _ in range(rng.randint(1, 2)):
        _add(terrain, "ruinas", rng.randint(2, 5), rng.randrange(8))
    return _trim(terrain, 15, rng)


def _ruin_terrain(rng: random.Random) -> dict[tuple[int, int], str]:
    terrain: dict[tuple[int, int], str] = {}
    for _ in range(rng.randint(3, 4)):
        r, c = rng.randint(2, 5), rng.randrange(1, 7)
        horizontal = rng.random() < 0.5
        for i in range(rng.randint(2, 3)):
            _add(
                terrain, "ruinas",
                r + (0 if horizontal else i),
                c + (i if horizontal else 0),
            )
    for _ in range(rng.randint(2, 3)):
        kind = rng.choice(("empalizada", "escombros", "penasco"))
        _add(terrain, kind, rng.randint(2, 5), rng.randrange(8))
    return _trim(terrain, 15, rng)


def _pass_terrain(rng: random.Random) -> dict[tuple[int, int], str]:
    terrain: dict[tuple[int, int], str] = {}
    for _ in range(rng.randint(4, 6)):
        cr, cc = rng.randint(2, 5), rng.randrange(8)
        kind = rng.choice(("penasco", "acantilado", "penasco"))
        for _ in range(rng.randint(1, 3)):
            _add(
                terrain, kind, cr + rng.choice((-1, 0, 1)),
                cc + rng.choice((-1, 0, 1)),
            )
    for _ in range(rng.randint(1, 2)):
        _add(terrain, "empalizada", rng.randint(2, 5), rng.randrange(8))
    return _trim(terrain, 15, rng)


TERRAIN_GENERATORS = {
    "bosque": _forest_terrain,
    "rio": _river_terrain,
    "acantilado": _cliff_terrain,
    "ruinas": _ruin_terrain,
    "paso": _pass_terrain,
}


def _connected(terrain: dict[tuple[int, int], str]) -> bool:
    queue = deque((7, c) for c in range(8))
    seen = set(queue)
    while queue:
        r, c = queue.popleft()
        if r == 0:
            return True
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if not (0 <= nr < 8 and 0 <= nc < 8):
                continue
            if (nr, nc) in terrain or (nr, nc) in seen:
                continue
            seen.add((nr, nc))
            queue.append((nr, nc))
    return False


def _generate_terrain(
    theme: str, rng: random.Random,
) -> dict[tuple[int, int], str]:
    generator = TERRAIN_GENERATORS[theme]
    fallback: dict[tuple[int, int], str] = {}
    for _ in range(60):
        terrain = generator(rng)
        fallback = terrain
        if len(terrain) >= 6 and _connected(terrain):
            return terrain
    return fallback


def _army_kinds(rng: random.Random, elephant: bool = False) -> list[str]:
    queens = rng.choice((0, 1, 1))
    rooks = rng.randint(1, 2)
    bishops = rng.randint(1, 2)
    elephants = rng.randint(1, 2) if elephant else 0
    knights = rng.randint(1, 2)
    fairy_pool = (
        FALCON, CENTAUR, PHOENIX, NIGHTRIDER, LION, GRASSHOPPER, CAMEL, ZEBRA,
    )
    fairy_count = rng.randint(2, 3)
    fairies = [rng.choice(fairy_pool) for _ in range(fairy_count)]
    pawns = max(
        4,
        15 - queens - rooks - bishops - elephants - knights - len(fairies),
    )
    kinds = (
        [KING]
        + [QUEEN] * queens
        + [ROOK] * rooks
        + [BISHOP] * bishops
        + [ELEPHANT] * elephants
        + [KNIGHT] * knights
        + fairies
        + [PAWN] * pawns
    )[:16]
    rng.shuffle(kinds)
    return kinds


def _make_pieces(
    color: str,
    kinds: list[str],
    rng: random.Random,
    start_pid: int,
) -> tuple[list[Piece], int]:
    pieces: list[Piece] = []
    pid = start_pid
    color_pools = NAME_POOLS.get(color, NAME_POOLS[WHITE])
    color_titles = TITLES.get(color, TITLES[WHITE])
    for kind in kinds:
        pool = color_pools[kind]
        name = rng.choice(pool)
        pieces.append(Piece(color, kind, pid, name, color_titles[kind]))
        pid += 1
    return pieces, pid


def _build_game(
    composition: list[str],
    terrain: dict[tuple[int, int], str],
    rng: random.Random,
    player_color: str = WHITE,
    enemy_color: str = BLACK,
) -> Optional[Game]:
    if enemy_color == player_color:
        enemy_color = BLACK if player_color != BLACK else WHITE
    game = Game(turn_order=(player_color, enemy_color))
    for (r, c), kind in terrain.items():
        game.add_terrain(kind, r, c)

    pid = 1
    for color, rows in ((player_color, (6, 7)), (enemy_color, (0, 1))):
        kinds = list(composition)
        rng.shuffle(kinds)
        pieces, pid = _make_pieces(color, kinds, rng, pid)
        slots = [
            (r, c) for r in rows for c in range(8)
            if not game.is_blocked(r, c)
        ]
        if len(slots) < len(pieces):
            return None
        rng.shuffle(slots)
        for piece, (r, c) in zip(pieces, slots):
            game.place(piece, r, c)
    return game


def _is_playable(game: Game) -> bool:
    for c in game.turn_order:
        if game.in_check(c):
            return False
        if not game.legal_moves(c):
            return False
    if game.result() is not None:
        return False
    return True


def _terrain_summary(terrain: dict[tuple[int, int], str]) -> str:
    counts = Counter(terrain.values())
    parts = []
    for kind, count in counts.most_common():
        label = TERRAIN_SINGULAR[kind] if count == 1 else TERRAIN_PLURAL[kind]
        parts.append(f"{count} {label}")
    return ", ".join(parts) if parts else "sin obstáculos"


def _army_summary(composition: list[str]) -> str:
    counts = Counter(kind for kind in composition if kind != KING)
    parts = []
    for kind in ARMY_LABEL:
        count = counts.get(kind, 0)
        if count:
            label = ARMY_LABEL[kind][0] if count == 1 else ARMY_LABEL[kind][1]
            parts.append(f"{count} {label}")
    return ", ".join(parts)


def create_wild_scenario(
    rng: Optional[random.Random] = None,
    elephant: bool = False,
    player_color: str = WHITE,
    enemy_color: str = BLACK,
) -> WildScenario:
    rng = rng or random.Random()
    theme = rng.choice(tuple(THEMES))
    composition = _army_kinds(rng, elephant=elephant)

    game: Optional[Game] = None
    terrain: dict[tuple[int, int], str] = {}
    for _ in range(120):
        terrain = _generate_terrain(theme, rng)
        candidate = _build_game(composition, terrain, rng, player_color, enemy_color)
        if candidate is not None and _is_playable(candidate):
            game = candidate
            break

    if game is None:
        terrain = {}
        for _ in range(200):
            candidate = _build_game(composition, terrain, rng, player_color, enemy_color)
            if candidate is not None and _is_playable(candidate):
                game = candidate
                break
        if game is None:
            raise RuntimeError("No se pudo generar la campaña salvaje")

    meta = THEMES[theme]
    return WildScenario(
        game=game,
        theme=theme,
        title=meta["title"],
        description=meta["description"],
        terrain_summary=_terrain_summary(terrain),
        army_summary=_army_summary(composition),
    )


def wild_prologue(
    scenario: WildScenario,
    vs_ai: bool,
    difficulty: str = "",
    fog: bool = False,
) -> LoreEntry:
    enemy_c = scenario.game.turn_order[-1] if scenario.game.turn_order else BLACK
    enemy_name = faction_name(enemy_c)
    text = (
        f"{scenario.description}\n\n"
        f"El terreno de esta campaña: {scenario.terrain_summary}. Bosques, ríos, "
        "peñascos y ruinas bloquean el paso y cortan la línea de tiro. "
        f"Las fuerzas en conflicto ({scenario.army_summary}) chocan frente a "
        f"{enemy_name}. Cada seis jugadas, la guerra puede cambiar el tablero."
    )
    if fog:
        text += (
            "\n\nUna niebla de guerra cubre el tablero. Solo verás las casillas "
            "que tus propias piezas vigilen; lo que aceche fuera de su alcance "
            "permanecerá oculto."
        )
    text += "\n\n"
    if vs_ai:
        oracle = {
            "Escudero": f"Al otro lado, un comandante ambicioso dirige a {enemy_name}.",
            "Caballero": f"Al otro lado, un general curtido comanda a {enemy_name}.",
            "Archimago": f"Al otro lado, un archimago que lee el porvenir guía a {enemy_name}.",
        }.get(difficulty, "Al otro lado, el Oráculo Umbrío acecha.")
        text += f"{oracle}\n\nQue comience la crónica salvaje."
    else:
        text += "Dos voluntades se enfrentan sobre la tierra rota.\n\nQue comience la crónica salvaje."
    return LoreEntry(f"Prólogo · {scenario.title}", text, "prologue")


def _event_candidates(game: Game) -> list[tuple[int, int]]:
    kings = [
        pos for c in game.turn_order
        if (pos := game.find_king(c)) is not None
    ]
    candidates = []
    for r in range(2, 6):
        for c in range(8):
            if game.grid[r][c] is not None or (r, c) in game.terrain:
                continue
            if game.ep == (r, c):
                continue
            if any(
                max(abs(r - kr), abs(c - kc)) <= 1 for kr, kc in kings
            ):
                continue
            candidates.append((r, c))
    return candidates


def wild_event(
    game: Game,
    scenario: WildScenario,
    rng: Optional[random.Random] = None,
) -> Optional[LoreEntry]:
    rng = rng or random.Random()
    if len(game.terrain) >= MAX_TERRAIN:
        return None
    candidates = _event_candidates(game)
    if not candidates:
        return None
    r, c = rng.choice(candidates)
    specs = EVENT_SPECS.get(scenario.theme, EVENT_SPECS["ruinas"])
    title, kind, opening = rng.choice(specs)
    if not game.add_terrain(kind, r, c):
        return None
    text = (
        f"{opening} en {square_name(r, c)}. "
        f"{TERRAIN_CONSEQUENCE[kind]} El terreno de la campaña ha cambiado."
    )
    return LoreEntry(f"Suceso de guerra · {title}", text, "event")
