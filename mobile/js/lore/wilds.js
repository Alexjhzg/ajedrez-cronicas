/**
 * Generación de campañas en Tierra Salvaje y Sucesos de Guerra Interactivos.
 */

import {
  AMAZON,
  BISHOP,
  BLACK,
  CAMEL,
  CENTAUR,
  ELEPHANT,
  FALCON,
  GRASSHOPPER,
  GREEN,
  KING,
  KNIGHT,
  LION,
  NIGHTRIDER,
  PAWN,
  PHOENIX,
  QUEEN,
  RED,
  ROOK,
  WHITE,
  ZEBRA,
  Game,
  createPiece,
} from "../engine.js";
import { KIND_LABEL, createGame, factionName, squareName } from "./catalog.js";
import { toRoman } from "./narrative.js";

export const WILD_EVENT_EVERY = 6;
export const MAX_TERRAIN = 24;

export const TERRAIN_LABEL = {
  bosque: "Bosque",
  rio: "Río",
  acantilado: "Acantilado",
  penasco: "Peñasco",
  ruinas: "Ruinas",
  empalizada: "Empalizada",
  escombros: "Escombros",
};

const TERRAIN_SINGULAR = {
  bosque: "bosque",
  rio: "río",
  acantilado: "acantilado",
  penasco: "peñasco",
  ruinas: "ruina",
  empalizada: "empalizada",
  escombros: "escombro",
};

const TERRAIN_PLURAL = {
  bosque: "bosques",
  rio: "ríos",
  acantilado: "acantilados",
  penasco: "peñascos",
  ruinas: "ruinas",
  empalizada: "empalizadas",
  escombros: "escombros",
};

export const TERRAIN_CONSEQUENCE = {
  bosque: "Los troncos ocultan la visión y frenan los disparos a través de la espesura.",
  rio: "El agua profunda frena el avance y acorta el alcance de las piezas que lo cruzan.",
  acantilado: "La roca partida bloquea el avance y la visión.",
  penasco: "El peñasco corta el camino y las líneas de tiro.",
  ruinas: "Los muros caídos ofrecen cobertura: quien los ocupe solo puede ser abatido de cerca.",
  empalizada: "La empalizada sella el paso con madera y acero.",
  escombros: "Los escombros sepultan el camino bajo piedra y ceniza.",
};

export const THEMES = {
  bosque: {
    title: "El Bosque de los Susurros",
    description:
      "Los árboles de Aethelgard han bebido tanta sangre que ya recuerdan los nombres de los caídos. Las columnas del Alba y del Eclipse avanzan entre troncos que cierran filas y raíces que devoran caminos.",
  },
  rio: {
    title: "La Ribera de Ceniza",
    description:
      "El río que separa las tierras del Alba de la llanura del Eclipse ha crecido con las lluvias de la guerra. Sus aguas turbias cortan la línea de tiro; solo quedan unos pocos vados para cruzar.",
  },
  acantilado: {
    title: "Los Acantilados del Cuervo",
    description:
      "En los Acantilados del Cuervo, la roca se parte como una corona rota. Los ejércitos deben rodear desfiladeros y peñascos mientras los cuervos cuentan en silencio a los que caen.",
  },
  ruinas: {
    title: "Las Ruinas del Trono",
    description:
      "Aquí se alzaba una ciudad antes de que Aethelgard tuviera nombre. Solo quedan muros partidos y empalizadas de fortuna: cada ruina es una trinchera y cada sombra, una emboscada.",
  },
  paso: {
    title: "El Paso del Dragón",
    description:
      "El Paso del Dragón es la única ruta entre el norte y el trono. Peñascos y acantilados estrangulan la marcha; quien domine sus estrechuras dominará la campaña.",
  },
};

const NON_ROYAL_POOLS = {
  [ROOK]: ["Torre"],
  [BISHOP]: ["Alfil"],
  [ELEPHANT]: ["Elefante"],
  [FALCON]: ["Halcón"],
  [AMAZON]: ["Amazonas"],
  [GRASSHOPPER]: ["Saltamontes"],
  [NIGHTRIDER]: ["Noctámbulo"],
  [CENTAUR]: ["Centauro"],
  [CAMEL]: ["Camello"],
  [LION]: ["León"],
  [ZEBRA]: ["Cebra"],
  [PHOENIX]: ["Fénix"],
  [KNIGHT]: ["Caballo"],
  [PAWN]: ["Peón"],
};

export const NAME_POOLS = {
  [WHITE]: {
    [KING]: ["Rey Balduino"],
    [QUEEN]: ["Reina Leonor"],
    ...NON_ROYAL_POOLS,
  },
  [BLACK]: {
    [KING]: ["Rey Vladimir"],
    [QUEEN]: ["Reina Carmila"],
    ...NON_ROYAL_POOLS,
  },
  [RED]: {
    [KING]: ["Rey Leónidas"],
    [QUEEN]: ["Reina Gorgo"],
    ...NON_ROYAL_POOLS,
  },
  [GREEN]: {
    [KING]: ["Rey Artur"],
    [QUEEN]: ["Reina Morgana"],
    ...NON_ROYAL_POOLS,
  },
};

export const TITLES = KIND_LABEL;

const ARMY_LABEL = {
  [AMAZON]: ["amazonas", "amazonas"],
  [QUEEN]: ["dama", "damas"],
  [ELEPHANT]: ["elefante", "elefantes"],
  [FALCON]: ["halcón", "halcones"],
  [LION]: ["león", "leones"],
  [CENTAUR]: ["centauro", "centauros"],
  [NIGHTRIDER]: ["noctámbulo", "noctámbulos"],
  [ROOK]: ["torre", "torres"],
  [BISHOP]: ["alfil", "alfiles"],
  [KNIGHT]: ["jinete", "jinetes"],
  [PHOENIX]: ["fénix", "fénix"],
  [GRASSHOPPER]: ["saltamontes", "saltamontes"],
  [CAMEL]: ["camello", "camellos"],
  [ZEBRA]: ["cebra", "cebras"],
  [PAWN]: ["escudero", "escuderos"],
};

export const EVENT_SPECS = {
  bosque: [
    ["La espesura avanza", "bosque", "Los árboles se cierran sobre la marcha"],
    ["Asalto de los leñadores", "empalizada", "Un asalto deja una empalizada clavada en el barro"],
    ["Alud de piedra", "penasco", "Las laderas se desprenden sobre la columna"],
  ],
  rio: [
    ["Crecida repentina", "rio", "El río se desborda y reclama una nueva orilla"],
    ["Asalto al vado", "escombros", "Un asalto deja el vado cubierto de escombros"],
    ["Derrumbamiento", "ruinas", "Un muro antiguo cae sobre la ribera"],
  ],
  acantilado: [
    ["Desprendimiento", "acantilado", "La montaña se rompe y derrama roca sobre el camino"],
    ["Roca caída", "penasco", "Un peñasco rueda desde la altura y se clava en el tablero"],
    ["Asalto de la cumbre", "empalizada", "Los defensores levantan una empalizada en la cima"],
  ],
  ruinas: [
    ["El muro cae", "ruinas", "Un tramo de muralla se desploma entre polvo y ceniza"],
    ["Asalto a la brecha", "escombros", "El asalto deja escombros y armas rotas en la brecha"],
    ["Empalizada de fortuna", "empalizada", "Los ingenieros alzan una empalizada con vigas robadas"],
  ],
  paso: [
    ["Alud del Dragón", "penasco", "El desfiladero vomita piedra sobre la vanguardia"],
    ["El paso se cierra", "acantilado", "La roca se quiebra y estrecha el paso"],
    ["Asalto de vanguardia", "empalizada", "La vanguardia clava una empalizada para cortar la ruta"],
  ],
};

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

export function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function addT(map, kind, r, c) {
  if (r >= 2 && r <= 5 && c >= 0 && c < 8) {
    map.set(`${r},${c}`, kind);
  }
}

function trimT(map, limit) {
  if (map.size <= limit) return map;
  const entries = shuffle(Array.from(map.entries())).slice(0, limit);
  return new Map(entries);
}

function generateTerrainByTheme(theme) {
  const map = new Map();
  if (theme === "bosque") {
    for (let i = 0; i < randInt(5, 7); i++) {
      const cr = randInt(2, 5);
      const cc = randInt(0, 7);
      const offsets = [[0, 0]];
      for (let j = 0; j < randInt(1, 2); j++) {
        offsets.push(pick([[-1, 0], [1, 0], [0, -1], [0, 1], [1, 1], [-1, -1]]));
      }
      for (const [dr, dc] of offsets) addT(map, "bosque", cr + dr, cc + dc);
    }
    for (let i = 0; i < randInt(1, 3); i++) {
      addT(map, "penasco", randInt(2, 5), randInt(0, 7));
    }
  } else if (theme === "rio") {
    if (Math.random() < 0.55) {
      const col = randInt(2, 5);
      const ford = randInt(2, 5);
      for (let r = 2; r < 6; r++) {
        if (r === ford) continue;
        addT(map, "rio", r, col);
        if (Math.random() < 0.4) addT(map, "rio", r, col + pick([-1, 1]));
      }
    } else {
      const row = randInt(2, 5);
      const ford = randInt(1, 6);
      for (let c = 1; c < 7; c++) {
        if (c === ford) continue;
        addT(map, "rio", row, c);
        if (Math.random() < 0.25) addT(map, "rio", row + pick([-1, 1]), c);
      }
    }
    for (let i = 0; i < randInt(2, 4); i++) {
      addT(map, pick(["ruinas", "penasco", "empalizada", "escombros"]), randInt(2, 5), randInt(0, 7));
    }
  } else if (theme === "acantilado") {
    for (let i = 0; i < randInt(4, 6); i++) {
      const cr = randInt(2, 5);
      const cc = randInt(0, 7);
      const kind = pick(["acantilado", "acantilado", "penasco"]);
      for (let j = 0; j < randInt(1, 3); j++) {
        addT(map, kind, cr + pick([-1, 0, 1]), cc + pick([-1, 0, 1]));
      }
    }
    for (let i = 0; i < randInt(1, 2); i++) {
      addT(map, "ruinas", randInt(2, 5), randInt(0, 7));
    }
  } else if (theme === "ruinas") {
    for (let i = 0; i < randInt(3, 4); i++) {
      const r = randInt(2, 5);
      const c = randInt(1, 6);
      const horizontal = Math.random() < 0.5;
      const len = randInt(2, 3);
      for (let k = 0; k < len; k++) {
        addT(map, "ruinas", r + (horizontal ? 0 : k), c + (horizontal ? k : 0));
      }
    }
    for (let i = 0; i < randInt(2, 3); i++) {
      addT(map, pick(["empalizada", "escombros", "penasco"]), randInt(2, 5), randInt(0, 7));
    }
  } else {
    for (let i = 0; i < randInt(4, 6); i++) {
      const cr = randInt(2, 5);
      const cc = randInt(0, 7);
      const kind = pick(["penasco", "acantilado", "penasco"]);
      for (let j = 0; j < randInt(1, 3); j++) {
        addT(map, kind, cr + pick([-1, 0, 1]), cc + pick([-1, 0, 1]));
      }
    }
    for (let i = 0; i < randInt(1, 2); i++) {
      addT(map, "empalizada", randInt(2, 5), randInt(0, 7));
    }
  }
  return trimT(map, 15);
}

function isConnected(terrainMap) {
  const queue = [];
  const seen = new Set();
  for (let c = 0; c < 8; c++) {
    queue.push([7, c]);
    seen.add(`7,${c}`);
  }
  while (queue.length > 0) {
    const [r, c] = queue.shift();
    if (r === 0) return true;
    for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
      const nr = r + dr;
      const nc = c + dc;
      if (nr < 0 || nr >= 8 || nc < 0 || nc >= 8) continue;
      const key = `${nr},${nc}`;
      if (terrainMap.has(key) || seen.has(key)) continue;
      seen.add(key);
      queue.push([nr, nc]);
    }
  }
  return false;
}

export function generateTerrain(theme) {
  let fallback = new Map();
  for (let i = 0; i < 60; i++) {
    const t = generateTerrainByTheme(theme);
    fallback = t;
    if (t.size >= 6 && isConnected(t)) return t;
  }
  return fallback;
}

export function armyKinds(elephant = false) {
  const queens = pick([0, 1, 1]);
  const rooks = randInt(1, 2);
  const bishops = randInt(1, 2);
  const elephants = elephant ? randInt(1, 2) : 0;
  const knights = randInt(1, 2);
  const fairyPool = [
    FALCON,
    CENTAUR,
    PHOENIX,
    NIGHTRIDER,
    LION,
    GRASSHOPPER,
    CAMEL,
    ZEBRA,
  ];
  const fairyCount = randInt(2, 3);
  const fairies = Array.from({ length: fairyCount }, () => pick(fairyPool));
  const pawns = Math.max(
    4,
    15 - queens - rooks - bishops - elephants - knights - fairies.length
  );
  const kinds = [
    KING,
    ...Array(queens).fill(QUEEN),
    ...Array(rooks).fill(ROOK),
    ...Array(bishops).fill(BISHOP),
    ...Array(elephants).fill(ELEPHANT),
    ...Array(knights).fill(KNIGHT),
    ...fairies,
    ...Array(pawns).fill(PAWN),
  ].slice(0, 16);
  return shuffle(kinds);
}

export function makePieces(color, kinds, startPid) {
  const pieces = [];
  let pid = startPid;
  const colorPools = NAME_POOLS[color] || NAME_POOLS[WHITE];
  const colorTitles = TITLES[color] || TITLES[WHITE];
  for (const kind of kinds) {
    const pool = colorPools[kind] || colorPools[PAWN];
    const name = pick(pool);
    pieces.push(createPiece(color, kind, pid++, name, colorTitles[kind] || "Campeón"));
  }
  return [pieces, pid];
}

export function terrainSummary(terrainMap) {
  const counts = {};
  for (const kind of terrainMap.values()) {
    counts[kind] = (counts[kind] || 0) + 1;
  }
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);
  if (entries.length === 0) return "sin obstáculos";
  return entries
    .map(([kind, count]) => `${count} ${count === 1 ? TERRAIN_SINGULAR[kind] : TERRAIN_PLURAL[kind]}`)
    .join(", ");
}

export function armySummary(composition) {
  const counts = {};
  for (const k of composition) {
    if (k !== KING) counts[k] = (counts[k] || 0) + 1;
  }
  const parts = [];
  for (const kind of Object.keys(ARMY_LABEL)) {
    const count = counts[kind] || 0;
    if (count > 0) {
      parts.push(`${count} ${count === 1 ? ARMY_LABEL[kind][0] : ARMY_LABEL[kind][1]}`);
    }
  }
  return parts.join(", ");
}

export function isPlayable(game) {
  for (const c of game.turn_order) {
    if (game.inCheck(c)) return false;
    if (game.legalMoves(c).length === 0) return false;
  }
  if (game.result() !== null) return false;
  return true;
}

export function createWildScenario(elephant = false, playerColor = WHITE, enemyColor = BLACK) {
  if (enemyColor === playerColor) {
    enemyColor = playerColor !== BLACK ? BLACK : WHITE;
  }
  const theme = pick(Object.keys(THEMES));
  const composition = armyKinds(elephant);
  let game = null;
  let terrain = new Map();

  for (let attempt = 0; attempt < 120; attempt++) {
    terrain = generateTerrain(theme);
    const candidate = new Game([playerColor, enemyColor]);
    for (const [key, kind] of terrain.entries()) {
      const [r, c] = key.split(",").map(Number);
      candidate.addTerrain(kind, r, c);
    }
    let pid = 1;
    let ok = true;
    for (const [color, rows] of [
      [playerColor, [6, 7]],
      [enemyColor, [0, 1]],
    ]) {
      const kinds = shuffle([...composition]);
      const [pieces, nextPid] = makePieces(color, kinds, pid);
      pid = nextPid;
      const slots = [];
      for (const r of rows) {
        for (let c = 0; c < 8; c++) {
          if (!candidate.isBlocked(r, c)) slots.push([r, c]);
        }
      }
      if (slots.length < pieces.length) {
        ok = false;
        break;
      }
      shuffle(slots);
      for (let i = 0; i < pieces.length; i++) {
        candidate.place(pieces[i], slots[i][0], slots[i][1]);
      }
    }
    if (ok && isPlayable(candidate)) {
      game = candidate;
      break;
    }
  }

  if (!game) {
    game = createGame(elephant, playerColor, enemyColor);
  }

  const meta = THEMES[theme];
  return {
    game,
    theme,
    title: meta.title,
    description: meta.description,
    terrain_summary: terrainSummary(terrain),
    army_summary: armySummary(composition),
  };
}

export function wildPrologue(scenario, vsAi, difficulty = "", fog = false) {
  const enemyC =
    scenario.game && scenario.game.turn_order && scenario.game.turn_order.length
      ? scenario.game.turn_order[scenario.game.turn_order.length - 1]
      : BLACK;
  const enemyName = factionName(enemyC);
  let text =
    `${scenario.description}\n\n` +
    `El terreno de esta campaña: ${scenario.terrain_summary}. Bosques, ríos, ` +
    "peñascos y ruinas moldean el paso y las líneas de tiro. " +
    `Las fuerzas en conflicto (${scenario.army_summary}) chocan frente a ${enemyName}. ` +
    "Cada seis jugadas, un suceso de guerra pondrá a prueba tu mando.";
  if (fog) {
    text +=
      "\n\nUna niebla de guerra cubre el tablero. Solo verás las casillas que tus propias piezas vigilen.";
  }
  const oracle = vsAi
    ? {
        Escudero: `Al otro lado, un comandante ambicioso dirige a ${enemyName}.`,
        Caballero: `Al otro lado, un general curtido comanda a ${enemyName}.`,
        Archimago: `Al otro lado, un archimago que lee el porvenir guía a ${enemyName}.`,
      }[difficulty] || "Al otro lado, el Oráculo Umbrío acecha."
    : "Dos voluntades se enfrentan sobre la tierra rota.";
  text += `\n\n${oracle}\n\nQue comience la crónica salvaje.`;
  return { heading: `Prólogo · ${scenario.title}`, text, tag: "prologue" };
}

function eventCandidates(game) {
  const kings = game.turn_order.map((c) => game.findKing(c)).filter(Boolean);
  const candidates = [];
  for (let r = 2; r < 6; r++) {
    for (let c = 0; c < 8; c++) {
      if (game.grid[r][c] !== null || game.terrainAt(r, c) !== null) continue;
      if (game.ep && game.ep[0] === r && game.ep[1] === c) continue;
      if (kings.some(([kr, kc]) => Math.max(Math.abs(r - kr), Math.abs(c - kc)) <= 1)) {
        continue;
      }
      candidates.push([r, c]);
    }
  }
  return candidates;
}

export function wildEvent(game, scenario) {
  if (game.terrain.size >= MAX_TERRAIN) return null;
  const candidates = eventCandidates(game);
  if (candidates.length === 0) return null;
  const [r, c] = pick(candidates);
  const specs = EVENT_SPECS[scenario.theme] || EVENT_SPECS.ruinas;
  const [title, kind, opening] = pick(specs);
  if (!game.addTerrain(kind, r, c)) return null;
  const text = `${opening} en ${squareName(r, c)}. ${TERRAIN_CONSEQUENCE[kind]} El terreno de la campaña ha cambiado.`;
  return { heading: `Suceso de guerra · ${title}`, text, tag: "event" };
}

export function wildDilemma(game, scenario) {
  if (game.terrain.size >= MAX_TERRAIN) return null;
  const candidates = eventCandidates(game);
  if (candidates.length < 2) return null;
  const shuffled = shuffle([...candidates]);
  const [r1, c1] = shuffled[0];
  const [r2, c2] = shuffled[1];
  const specs = shuffle([...(EVENT_SPECS[scenario.theme] || EVENT_SPECS.ruinas)]);
  const [title1, kind1, opening1] = specs[0];
  const [title2, kind2, opening2] = specs[1 % specs.length];
  const loc1 = squareName(r1, c1);
  const loc2 = squareName(r2, c2);

  return {
    title: `Encrucijada en ${scenario.title}`,
    prompt:
      "El campo de batalla cede bajo el fragor del combate. Como comandante, decide qué rumbo toma el suceso de guerra:",
    options: [
      {
        label: `${title1} en ${loc1}`,
        description: `Añade ${TERRAIN_LABEL[kind1]} en ${loc1}. ${TERRAIN_CONSEQUENCE[kind1]}`,
        kind: kind1,
        r: r1,
        c: c1,
        opening: opening1,
      },
      {
        label: `${title2} en ${loc2}`,
        description: `Añade ${TERRAIN_LABEL[kind2]} en ${loc2}. ${TERRAIN_CONSEQUENCE[kind2]}`,
        kind: kind2,
        r: r2,
        c: c2,
        opening: opening2,
      },
    ],
  };
}

export function applyWildChoice(game, choice) {
  if (!game.addTerrain(choice.kind, choice.r, choice.c)) return null;
  const text = `${choice.opening} en ${squareName(choice.r, choice.c)}. ${TERRAIN_CONSEQUENCE[choice.kind]} El terreno de la campaña ha cambiado.`;
  return {
    heading: `Suceso de guerra · ${choice.label}`,
    text,
    tag: "event",
  };
}
