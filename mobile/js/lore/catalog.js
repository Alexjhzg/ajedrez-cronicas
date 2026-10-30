/**
 * Catálogo de facciones, geografía, personajes, biografías y tableros (8x8 y 12x12).
 */

import {
  ALL_COLORS,
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
  algebraic,
  createPiece,
} from "../engine.js";

export const FACTIONS = {
  [WHITE]: {
    name: "Orden del Alba",
    short: "el Alba",
    adjective: "alba",
    crest: "☀",
    culture: "Reino Cruzado",
    sovereigns: "Rey Balduino y Reina Leonor",
    motto: "Caballeros templarios, fortalezas blancas y honor solar.",
    lore: "Reino de caballeros templarios y fortalezas blancas liderado por el Rey Balduino y la Reina Leonor.",
  },
  [BLACK]: {
    name: "Legión del Eclipse",
    short: "el Eclipse",
    adjective: "umbría",
    crest: "☾",
    culture: "Corte de Valaquia",
    sovereigns: "Rey Vladimir y Reina Carmila",
    motto: "Castillos en la niebla, guardia nocturna y la Orden del Dragón.",
    lore: "Señores nocturnos de Valaquia que dominan desde castillos en la niebla bajo el Rey Vladimir y la Reina Carmila.",
  },
  [RED]: {
    name: "Forja Carmesí",
    short: "la Forja",
    adjective: "carmesí",
    crest: "⚔",
    culture: "Imperio Espartano",
    sovereigns: "Rey Leónidas y Reina Gorgo",
    motto: "Falanges de bronce, legiones de hierro y disciplina marcial.",
    lore: "Imperio marcial de falanges de bronce y legiones de hierro comandado por el Rey Leónidas y la Reina Gorgo.",
  },
  [GREEN]: {
    name: "Pacto de la Espesura",
    short: "el Pacto",
    adjective: "silvana",
    crest: "❖",
    culture: "Clanes Celtas",
    sovereigns: "Rey Vercingétorix y Reina Boudica",
    motto: "Guerreros de los clanes, druidas y bosques sagrados.",
    lore: "Confederación de clanes celtas y druidas de los bosques guiada por el Rey Vercingétorix y la Reina Boudica.",
  },
};

export const KIND_LABEL = {
  [WHITE]: {
    [KING]: "Rey Cruzado",
    [QUEEN]: "Reina del Alba",
    [ROOK]: "Bastión Templario",
    [BISHOP]: "Prelado",
    [KNIGHT]: "Caballero Templario",
    [PAWN]: "Cruzado",
    [FALCON]: "Halcón Real",
    [ELEPHANT]: "Elefante Real",
    [AMAZON]: "Paladina",
    [GRASSHOPPER]: "Saltador Solar",
    [NIGHTRIDER]: "Jinete Astral",
    [CENTAUR]: "Centauro Real",
    [CAMEL]: "Camello Cruzado",
    [LION]: "León Real",
    [ZEBRA]: "Corcel Blanco",
    [PHOENIX]: "Fénix Solar",
  },
  [BLACK]: {
    [KING]: "Rey de Valaquia",
    [QUEEN]: "Reina Nocturna",
    [ROOK]: "Castillo Gótico",
    [BISHOP]: "Conde Nocturno",
    [KNIGHT]: "Jinete Nocturno",
    [PAWN]: "Guardia Nocturno",
    [FALCON]: "Halcón Nocturno",
    [ELEPHANT]: "Elefante de Asedio",
    [AMAZON]: "Dama del Dragón",
    [GRASSHOPPER]: "Saltador Umbrío",
    [NIGHTRIDER]: "Jinete de la Niebla",
    [CENTAUR]: "Centauro Oscuro",
    [CAMEL]: "Camello Nocturno",
    [LION]: "León Negro",
    [ZEBRA]: "Corcel de Sombra",
    [PHOENIX]: "Fénix de Ceniza",
  },
  [RED]: {
    [KING]: "Rey de Esparta",
    [QUEEN]: "Reina de Esparta",
    [ROOK]: "Fortaleza de Bronce",
    [BISHOP]: "Oráculo de Guerra",
    [KNIGHT]: "Centurión",
    [PAWN]: "Espartano",
    [FALCON]: "Águila Imperial",
    [ELEPHANT]: "Elefante de Guerra",
    [AMAZON]: "Campeona Espartana",
    [GRASSHOPPER]: "Saltador de Bronce",
    [NIGHTRIDER]: "Jinete Pretoriano",
    [CENTAUR]: "Centauro de Bronce",
    [CAMEL]: "Camello Imperial",
    [LION]: "León de Esparta",
    [ZEBRA]: "Corcel Carmesí",
    [PHOENIX]: "Fénix de Fuego",
  },
  [GREEN]: {
    [KING]: "Rey de los Clanes",
    [QUEEN]: "Reina Guerrera",
    [ROOK]: "Bastión del Bosque",
    [BISHOP]: "Druida",
    [KNIGHT]: "Jinete Celta",
    [PAWN]: "Guerrero Celta",
    [FALCON]: "Halcón del Bosque",
    [ELEPHANT]: "Coloso del Bosque",
    [AMAZON]: "Guerrera Celta",
    [GRASSHOPPER]: "Saltador del Bosque",
    [NIGHTRIDER]: "Jinete Salvaje",
    [CENTAUR]: "Centauro del Bosque",
    [CAMEL]: "Corcel de las Colinas",
    [LION]: "León de las Tierras Altas",
    [ZEBRA]: "Corcel Pintado",
    [PHOENIX]: "Fénix del Bosque",
  },
};

export function factionName(color) {
  return (FACTIONS[color] || FACTIONS[WHITE]).name;
}

export function rivalFactions(playerColor) {
  return ALL_COLORS.filter((c) => c !== playerColor);
}

const FILES = [
  "el Valle",
  "el Bosque",
  "el Río",
  "la Cañada",
  "la Colina",
  "el Puente",
  "las Ruinas",
  "el Torreón",
  "la Ciudadela",
  "el Santuario",
  "el Desfiladero",
  "la Cumbre",
];
const RANKS = [
  "del Alba",
  "de los Susurros",
  "de las Cenizas",
  "del Cuervo",
  "del Dragón",
  "de la Niebla",
  "de las Estrellas",
  "del Trono",
  "del Fénix",
  "de los Colosos",
  "de los Antiguos",
  "del Imperio",
];

export function squareName(r, c, size = 8) {
  const fIdx = Math.max(0, Math.min(FILES.length - 1, c));
  const rIdx = Math.max(0, Math.min(RANKS.length - 1, size - 1 - r));
  return `${FILES[fIdx]} ${RANKS[rIdx]}`;
}

export function locationLabel(r, c, size = 8) {
  return `${squareName(r, c, size)} · ${algebraic(r, c, size).toUpperCase()}`;
}

export const PIECE_DISPLAY_NAME = {
  [KING]: "Rey",
  [QUEEN]: "Reina",
  [ROOK]: "Torre",
  [BISHOP]: "Alfil",
  [KNIGHT]: "Caballo",
  [PAWN]: "Peón",
  [FALCON]: "Halcón",
  [ELEPHANT]: "Elefante",
  [AMAZON]: "Amazonas",
  [GRASSHOPPER]: "Saltamontes",
  [NIGHTRIDER]: "Noctámbulo",
  [CENTAUR]: "Centauro",
  [CAMEL]: "Camello",
  [LION]: "León",
  [ZEBRA]: "Cebra",
  [PHOENIX]: "Fénix",
};

export const WHITE_BACK = [
  [ROOK, "Torre", "Bastión Templario"],
  [KNIGHT, "Caballo", "Caballero Templario"],
  [BISHOP, "Alfil", "Prelado"],
  [QUEEN, "Reina Leonor", "Reina del Alba"],
  [KING, "Rey Balduino", "Rey Cruzado"],
  [BISHOP, "Alfil", "Prelado"],
  [KNIGHT, "Caballo", "Caballero Templario"],
  [ROOK, "Torre", "Bastión Templario"],
];

export const WHITE_ELEPHANT = [ELEPHANT, "Elefante", "Elefante Real"];
export const BLACK_ELEPHANT = [ELEPHANT, "Elefante", "Elefante de Asedio"];
export const RED_ELEPHANT = [ELEPHANT, "Elefante", "Elefante de Guerra"];
export const GREEN_ELEPHANT = [ELEPHANT, "Elefante", "Coloso del Bosque"];

export const WHITE_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Cruzado"]);

export const BLACK_BACK = [
  [ROOK, "Torre", "Castillo Gótico"],
  [KNIGHT, "Caballo", "Jinete Nocturno"],
  [BISHOP, "Alfil", "Conde Nocturno"],
  [QUEEN, "Reina Carmila", "Reina Nocturna"],
  [KING, "Rey Vladimir", "Rey de Valaquia"],
  [BISHOP, "Alfil", "Conde Nocturno"],
  [KNIGHT, "Caballo", "Jinete Nocturno"],
  [ROOK, "Torre", "Castillo Gótico"],
];

export const BLACK_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Guardia Nocturno"]);

export const RED_BACK = [
  [ROOK, "Torre", "Fortaleza de Bronce"],
  [KNIGHT, "Caballo", "Centurión"],
  [BISHOP, "Alfil", "Oráculo de Guerra"],
  [QUEEN, "Reina Gorgo", "Reina de Esparta"],
  [KING, "Rey Leónidas", "Rey de Esparta"],
  [BISHOP, "Alfil", "Oráculo de Guerra"],
  [KNIGHT, "Caballo", "Centurión"],
  [ROOK, "Torre", "Fortaleza de Bronce"],
];

export const GREEN_BACK = [
  [ROOK, "Torre", "Bastión del Bosque"],
  [KNIGHT, "Caballo", "Jinete Celta"],
  [BISHOP, "Alfil", "Druida"],
  [QUEEN, "Reina Boudica", "Reina Guerrera"],
  [KING, "Rey Vercingétorix", "Rey de los Clanes"],
  [BISHOP, "Alfil", "Druida"],
  [KNIGHT, "Caballo", "Jinete Celta"],
  [ROOK, "Torre", "Bastión del Bosque"],
];

export const RED_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Espartano"]);

export const GREEN_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Guerrero Celta"]);

export const FACTION_BACK = {
  [WHITE]: WHITE_BACK,
  [BLACK]: BLACK_BACK,
  [RED]: RED_BACK,
  [GREEN]: GREEN_BACK,
};

export const FACTION_ELEPHANT = {
  [WHITE]: WHITE_ELEPHANT,
  [BLACK]: BLACK_ELEPHANT,
  [RED]: RED_ELEPHANT,
  [GREEN]: GREEN_ELEPHANT,
};

export const FACTION_PAWNS = {
  [WHITE]: WHITE_PAWNS,
  [BLACK]: BLACK_PAWNS,
  [RED]: RED_PAWNS,
  [GREEN]: GREEN_PAWNS,
};

export const OFFICER_BIOS = {
  "Rey Balduino":
    "El Rey de la máscara de plata; lidera a los caballeros cruzados del Alba con fe y estrategia inquebrantables.",
  "Reina Leonor":
    "Soberana del Alba cuya diplomacia y temple dirigen las órdenes de caballería.",
  "Rey Vladimir":
    "Señor de Valaquia y de la Orden del Dragón; defiende sus montañas con mano de hierro y terror nocturno.",
  "Reina Carmila":
    "Soberana inmortal de los castillos envueltos en niebla, maestra de los secretos de la noche.",
  "Rey Leónidas":
    "Rey guerrero de Esparta que encabeza la falange de bronce sin retroceder jamás un paso.",
  "Reina Gorgo":
    "Reina de Esparta cuya voz gobierna la patria bajo la ley de volver con el escudo o sobre él.",
  "Rey Vercingétorix":
    "Gran caudillo que unificó a los clanes celtas para defender la libertad de los bosques.",
  "Reina Boudica":
    "Reina guerrera de los clanes que lidera la carga desde su carro de batalla.",
};

const PAWN_BIOS = {
  [WHITE]: "Soldado cruzado que marcha con escudo blanco y fe en la Orden del Alba.",
  [BLACK]: "Guardia nocturno de Valaquia que vigila los pasos de montaña entre la niebla.",
  [RED]: "Guerrero espartano que avanza en falange cerrada con escudo de bronce y lanza.",
  [GREEN]: "Guerrero de los clanes celtas que lucha con lanza y pintura de guerra azul.",
};

const FAIRY_GENERIC_BIOS = {
  [FALCON]:
    "Híbrido de Alfil y Caballo. Corta las diagonales del campo y cambia el color de su casilla mediante un salto de presa.",
  [ELEPHANT]:
    "Híbrido pesado de Torre y Caballo. Combina la embestida en columna con el salto táctico sobre las trincheras.",
  [AMAZON]:
    "La guerrera suprema de Aethelgard: une el alcance total de la Reina con el salto del Caballo. Ninguna casilla cercana está a salvo.",
  [GRASSHOPPER]:
    "Saltador místico de las ocho direcciones: necesita apoyarse sobre una pieza para catapultarse a la casilla inmediatamente posterior.",
  [NIGHTRIDER]:
    "Jinete espectral de largo alcance: encadena múltiples saltos de Caballo en una misma línea recta durante un solo turno.",
  [CENTAUR]:
    "Guardia real híbrida de Rey y Caballo: domina el combate cercano en las ocho casillas adyacentes y salta sobre el frente sin temor al jaque.",
  [CAMEL]:
    "Saltador de estepa de zancada alargada (3x1): permanece siempre fiel al color de su casilla de origen.",
  [LION]:
    "Depredador real de largo alcance: salta sobre un obstáculo en cualquiera de las ocho direcciones y aterriza en cualquier casilla más allá.",
  [ZEBRA]:
    "Saltador exótico de flanco (3x2): sortea murallas y formaciones cerradas en ángulos imposibles.",
  [PHOENIX]:
    "Ave inmortal de fuego y ceniza: se desliza un paso en cruz o renace saltando dos casillas en diagonal sobre cualquier barrera.",
};

const GENERIC_BIOS = {
  [WHITE]: {
    [KING]: "Rey cruzado de la Orden del Alba.",
    [QUEEN]: "Reina soberana de las fortalezas blancas del Alba.",
    [ROOK]: "Bastión templario de piedra blanca que protege las líneas del reino.",
    [BISHOP]: "Prelado consejero que guía a las tropas con sabiduría sagrada.",
    [KNIGHT]: "Caballero templario pesado cuya carga rompe las filas enemigas.",
    ...FAIRY_GENERIC_BIOS,
  },
  [BLACK]: {
    [KING]: "Soberano nocturno de las montañas de Valaquia.",
    [QUEEN]: "Reina de las sombras y señora de los castillos góticos.",
    [ROOK]: "Castillo escarpado sobre los riscos que domina el paso.",
    [BISHOP]: "Conde nocturno versado en los secretos de la Orden del Dragón.",
    [KNIGHT]: "Jinete nocturno que ataca sin previo aviso desde la niebla.",
    ...FAIRY_GENERIC_BIOS,
  },
  [RED]: {
    [KING]: "Rey guerrero de las falanges de Esparta.",
    [QUEEN]: "Reina de hierro y bronce cuyo mandato guía a las legiones.",
    [ROOK]: "Fortaleza acorazada de bronce y hierro, imparable en línea recta.",
    [BISHOP]: "Oráculo marcial que lee los presagios antes del combate.",
    [KNIGHT]: "Centurión a caballo forjado para aplastar los flancos rivales.",
    ...FAIRY_GENERIC_BIOS,
  },
  [GREEN]: {
    [KING]: "Gran caudillo de los clanes libres del bosque.",
    [QUEEN]: "Reina guerrera cuyas órdenes despiertan la furia de las tribus.",
    [ROOK]: "Bastión de roble y piedra levantado por los antiguos clanes.",
    [BISHOP]: "Druida sabio de los bosques sagrados y círculos de piedra.",
    [KNIGHT]: "Jinete celta veloz capaz de sortear cualquier obstáculo.",
    ...FAIRY_GENERIC_BIOS,
  },
};

export const VETERAN_TRAITS = {
  [PAWN]: "Veterano (2+ bajas): puede avanzar lateralmente y embestir de frente.",
  [KNIGHT]: "Veterano (2+ bajas): puede dar un paso ortogonal corto.",
  [BISHOP]: "Veterano (2+ bajas): puede dar un paso ortogonal corto.",
  [ROOK]: "Veterano (2+ bajas): puede dar un paso diagonal corto.",
  [QUEEN]: "Veterano (2+ bajas): domina también el salto del jinete.",
  [FALCON]: "Veterano (2+ bajas): añade un paso ortogonal corto a su vuelo.",
  [ELEPHANT]: "Veterano (2+ bajas): añade un paso diagonal corto a su embestida.",
  [AMAZON]: "Veterano (2+ bajas): añade el salto diagonal 2x2 del Fénix.",
  [GRASSHOPPER]: "Veterano (2+ bajas): puede desplazarse un paso ortogonal sin obstáculo.",
  [NIGHTRIDER]: "Veterano (2+ bajas): puede dar un paso ortogonal corto.",
  [CENTAUR]: "Veterano (2+ bajas): añade el salto diagonal de dos casillas.",
  [CAMEL]: "Veterano (2+ bajas): puede cambiar el color de su casilla con un paso ortogonal.",
  [LION]: "Veterano (2+ bajas): puede dar un paso real sin necesidad de saltar.",
  [ZEBRA]: "Veterano (2+ bajas): añade un paso ortogonal corto.",
  [PHOENIX]: "Veterano (2+ bajas): domina los ocho pasos adyacentes además de su salto ígneo.",
};

export function characterBio(piece) {
  if (!piece) return "";
  let base = OFFICER_BIOS[piece.name];
  if (!base) {
    const pawnBio = PAWN_BIOS[piece.color] || PAWN_BIOS[WHITE];
    const colorBios = GENERIC_BIOS[piece.color] || GENERIC_BIOS[WHITE];
    base = piece.kind === PAWN ? pawnBio : colorBios[piece.kind] || pawnBio;
  }
  if (piece.veteran && VETERAN_TRAITS[piece.kind]) {
    return `${base}\n★ ${VETERAN_TRAITS[piece.kind]}`;
  }
  if (piece.kills === 1 && piece.kind !== KING) {
    return `${base}\nBajas en combate: 1 (a 1 baja del rango Veterano).`;
  }
  return base;
}

export function createGame(elephant = false, playerColor = WHITE, enemyColor = BLACK) {
  if (enemyColor === playerColor) {
    enemyColor = playerColor !== BLACK ? BLACK : WHITE;
  }
  const game = new Game([playerColor, enemyColor]);
  let pid = 1;

  const playerBack = (FACTION_BACK[playerColor] || WHITE_BACK).map((x) => [...x]);
  const enemyBack = (FACTION_BACK[enemyColor] || BLACK_BACK).map((x) => [...x]);
  if (elephant) {
    playerBack[2] = [...(FACTION_ELEPHANT[playerColor] || WHITE_ELEPHANT)];
    enemyBack[2] = [...(FACTION_ELEPHANT[enemyColor] || BLACK_ELEPHANT)];
  }
  const playerPawns = (FACTION_PAWNS[playerColor] || WHITE_PAWNS).slice(0, 8);
  const enemyPawns = (FACTION_PAWNS[enemyColor] || BLACK_PAWNS).slice(0, 8);

  for (let col = 0; col < 8; col++) {
    const [kind, name, title] = playerBack[col];
    game.place(createPiece(playerColor, kind, pid++, name, title), 7, col);
  }
  for (let col = 0; col < 8; col++) {
    const [name, title] = playerPawns[col];
    game.place(createPiece(playerColor, PAWN, pid++, name, title), 6, col);
  }
  for (let col = 0; col < 8; col++) {
    const [kind, name, title] = enemyBack[col];
    game.place(createPiece(enemyColor, kind, pid++, name, title), 0, col);
  }
  for (let col = 0; col < 8; col++) {
    const [name, title] = enemyPawns[col];
    game.place(createPiece(enemyColor, PAWN, pid++, name, title), 1, col);
  }

  game.castling[playerColor] = { K: true, Q: true };
  game.castling[enemyColor] = { K: true, Q: true };
  return game;
}

const IMPERIAL_ROW_1 = [
  ROOK,
  NIGHTRIDER,
  LION,
  FALCON,
  QUEEN,
  KING,
  AMAZON,
  ELEPHANT,
  LION,
  NIGHTRIDER,
  BISHOP,
  ROOK,
];

const IMPERIAL_ROW_2 = [
  ZEBRA,
  CAMEL,
  GRASSHOPPER,
  PHOENIX,
  KNIGHT,
  CENTAUR,
  CENTAUR,
  KNIGHT,
  PHOENIX,
  GRASSHOPPER,
  CAMEL,
  ZEBRA,
];

const IMPERIAL_ROYAL_NAMES = {
  [WHITE]: { [KING]: "Rey Balduino", [QUEEN]: "Reina Leonor" },
  [BLACK]: { [KING]: "Rey Vladimir", [QUEEN]: "Reina Carmila" },
  [RED]: { [KING]: "Rey Leónidas", [QUEEN]: "Reina Gorgo" },
  [GREEN]: { [KING]: "Rey Vercingétorix", [QUEEN]: "Reina Boudica" },
};

/**
 * Crea una partida en el Gran Tablero Imperial de 12x12 con las 10 nuevas piezas.
 */
export function createImperialGame(playerColor = WHITE, enemyColor = BLACK) {
  if (enemyColor === playerColor) {
    enemyColor = playerColor !== BLACK ? BLACK : WHITE;
  }
  const game = new Game([playerColor, enemyColor], null, 12);
  let pid = 1;

  function placeArmy(color, rowMajor, rowVanguard, rowPawns) {
    const royals = IMPERIAL_ROYAL_NAMES[color] || IMPERIAL_ROYAL_NAMES[WHITE];
    const labels = KIND_LABEL[color] || KIND_LABEL[WHITE];

    for (let col = 0; col < 12; col++) {
      const kind = IMPERIAL_ROW_1[col];
      const name = royals[kind] || PIECE_DISPLAY_NAME[kind];
      const title = labels[kind] || "Oficial";
      game.place(createPiece(color, kind, pid++, name, title), rowMajor, col);
    }

    for (let col = 0; col < 12; col++) {
      const kind = IMPERIAL_ROW_2[col];
      const name = royals[kind] || PIECE_DISPLAY_NAME[kind];
      const title = labels[kind] || "Vanguardia";
      game.place(createPiece(color, kind, pid++, name, title), rowVanguard, col);
    }

    const pawns = FACTION_PAWNS[color] || WHITE_PAWNS;
    for (let col = 0; col < 12; col++) {
      const [name, title] = pawns[col % pawns.length];
      game.place(createPiece(color, PAWN, pid++, name, title), rowPawns, col);
    }
  }

  placeArmy(playerColor, 11, 10, 9);
  placeArmy(enemyColor, 0, 1, 2);
  return game;
}

/** Devuelve 4 oficiales (Torre, Reina, Rey, Jinete/Elefante) y 4 peones. */
function frontContingent(color, elephant = false) {
  const back = FACTION_BACK[color] || WHITE_BACK;
  const pawns = FACTION_PAWNS[color] || WHITE_PAWNS;
  const flank = elephant ? FACTION_ELEPHANT[color] || WHITE_ELEPHANT : back[1];
  const officers = [back[0], back[3], back[4], flank];
  return [officers, pawns.slice(0, 4)];
}

/** Crea una batalla simultánea de 4 reinos en los cuatro puntos cardinales. */
export function createFourFrontsGame(elephant = false, playerColor = WHITE) {
  const base = [...ALL_COLORS];
  const idx = base.indexOf(playerColor);
  const ordered = idx >= 0 ? [...base.slice(idx), ...base.slice(0, idx)] : base;
  const [southC, westC, northC, eastC] = ordered;
  const frontDirs = {
    [southC]: [-1, 0],
    [westC]: [0, 1],
    [northC]: [1, 0],
    [eastC]: [0, -1],
  };
  const game = new Game(ordered, frontDirs);

  for (const [r, c] of [[0, 0], [0, 7], [7, 0], [7, 7]]) {
    game.addTerrain("penasco", r, c);
  }
  for (const [r, c] of [[1, 1], [1, 6], [6, 1], [6, 6]]) {
    game.addTerrain("ruinas", r, c);
  }

  let pid = 1;
  const layout = [
    [southC, (i) => [7, 2 + i], (i) => [6, 2 + i]],
    [westC, (i) => [2 + i, 0], (i) => [2 + i, 1]],
    [northC, (i) => [0, 2 + i], (i) => [1, 2 + i]],
    [eastC, (i) => [2 + i, 7], (i) => [2 + i, 6]],
  ];
  for (const [color, officerSq, pawnSq] of layout) {
    const [officers, pawns] = frontContingent(color, elephant);
    officers.forEach(([kind, name, title], i) => {
      const [r, c] = officerSq(i);
      game.place(createPiece(color, kind, pid++, name, title), r, c);
    });
    pawns.forEach(([name, title], i) => {
      const [r, c] = pawnSq(i);
      game.place(createPiece(color, PAWN, pid++, name, title), r, c);
    });
  }
  return game;
}

export function pieceOnBoard(game, piece) {
  if (!piece) return null;
  const n = game.size || 8;
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const p = game.grid[r][c];
      if (p && p.pid === piece.pid) return [r, c];
    }
  }
  return null;
}
