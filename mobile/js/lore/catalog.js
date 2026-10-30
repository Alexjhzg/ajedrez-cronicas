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
    culture: "Sacro Imperio y Cruzadas Franco-Normandas",
    sovereigns: "Rey Balduino y Reina Leonor",
    motto: "Catedrales de mármol blanco, órdenes templarias y el juramento del Sol Invicto.",
    lore:
      "Inspirada en los reinos cruzados franco-normandos y el Sacro Imperio. Sus ejércitos marchan desde ciudadelas de caliza blanca y catedrales góticas bajo el código de caballería templaria, liderados por el Rey Balduino y la Reina Leonor.",
  },
  [BLACK]: {
    name: "Legión del Eclipse",
    short: "el Eclipse",
    adjective: "umbría",
    crest: "☾",
    culture: "Principado de Valaquia y Transilvania Gótica",
    sovereigns: "Rey Vladimir y Reina Carmila",
    motto: "Ciudadelas escarpadas de los Cárpatos, la Orden del Dragón y los voivodas nocturnos.",
    lore:
      "Inspirada en la Valaquia histórica de la Orden del Dragón y los castillos góticos de Transilvania. Desde fortalezas alzadas sobre desfiladeros envueltos en niebla, el Rey Vladimir y la Reina Carmila defienden sus dominios con caballería nocturna y terror psicológico.",
  },
  [RED]: {
    name: "Forja Carmesí",
    short: "la Forja",
    adjective: "carmesí",
    crest: "⚔",
    culture: "Esparta Clásica e Imperio Romano",
    sovereigns: "Rey Leónidas y Reina Gorgo",
    motto: "Falanges de bronce, legiones de hierro y la ley de volver con el escudo o sobre él.",
    lore:
      "Inspirada en la disciplina militar de la Esparta clásica y la maquinaria bélica de las legiones de Roma. Bajo capas carmesíes y águilas de bronce, el Rey Leónidas y la Reina Gorgo gobiernan una ciudadanía forjada para la guerra en formación cerrada.",
  },
  [GREEN]: {
    name: "Pacto de la Espesura",
    short: "el Pacto",
    adjective: "silvana",
    crest: "❖",
    culture: "Confederación Celta de Galia, Britania e Hibernia",
    sovereigns: "Rey Vercingétorix y Reina Boudica",
    motto: "Robledales sagrados de los druidas, círculos megalíticos y clanes pintados con glasto.",
    lore:
      "Inspirado en las tribus celtas de la Galia, los clanes britanos e Hibernia. Reunidos en torno a nemetones sagrados y fortalezas de colina, el Rey Vercingétorix y la Reina Boudica lideran emboscadas relámpago entre bosques milenarios.",
  },
};

export const KIND_LABEL = {
  [WHITE]: {
    [KING]: "Rey Cruzado del Alba",
    [QUEEN]: "Soberana de las Catedrales",
    [ROOK]: "Bastión Templario",
    [BISHOP]: "Prelado del Sol",
    [KNIGHT]: "Caballero Hospitalario",
    [PAWN]: "Cruzado del Alba",
    [FALCON]: "Halcón Solar",
    [ELEPHANT]: "Coloso de Ultramar",
    [AMAZON]: "Paladina del Alba",
    [GRASSHOPPER]: "Saltamontes de Luz",
    [NIGHTRIDER]: "Noctámbulo Astral",
    [CENTAUR]: "Centauro Dorado",
    [CAMEL]: "Camello de Ultramar",
    [LION]: "León de Ricardo",
    [ZEBRA]: "Cebra de Antioquía",
    [PHOENIX]: "Fénix Sagrado",
  },
  [BLACK]: {
    [KING]: "Voivoda del Eclipse",
    [QUEEN]: "Condesa de la Sangre Nocturna",
    [ROOK]: "Ciudadela de los Cárpatos",
    [BISHOP]: "Boyardo del Eclipse",
    [KNIGHT]: "Húsar de la Noche",
    [PAWN]: "Guardia de la Empalizada",
    [FALCON]: "Halcón de los Cárpatos",
    [ELEPHANT]: "Coloso de Valaquia",
    [AMAZON]: "Amazonas del Dragón",
    [GRASSHOPPER]: "Saltamontes del Vacío",
    [NIGHTRIDER]: "Noctámbulo de Transilvania",
    [CENTAUR]: "Centauro de Hueso",
    [CAMEL]: "Camello del Danubio",
    [LION]: "León de Valaquia",
    [ZEBRA]: "Cebra Espectral",
    [PHOENIX]: "Fénix de Ceniza",
  },
  [RED]: {
    [KING]: "Éforo de la Falange Carmesí",
    [QUEEN]: "Augusta de Hierro y Bronce",
    [ROOK]: "Castrum Pretoriano",
    [BISHOP]: "Augur de Marte",
    [KNIGHT]: "Equite Cataphracto",
    [PAWN]: "Hoplita de la Falange",
    [FALCON]: "Águila Imperial",
    [ELEPHANT]: "Elefante Pírrico",
    [AMAZON]: "Campeona de Esparta",
    [GRASSHOPPER]: "Velite Saltador",
    [NIGHTRIDER]: "Explorador Pretoriano",
    [CENTAUR]: "Centauro de Lacedemonia",
    [CAMEL]: "Camello de Siria",
    [LION]: "León de las Termópilas",
    [ZEBRA]: "Cebra Numidia",
    [PHOENIX]: "Fénix de Vesta",
  },
  [GREEN]: {
    [KING]: "Gran Caudillo de los Clanes",
    [QUEEN]: "Reina Guerrera de los Icenos",
    [ROOK]: "Dun Megalítico",
    [BISHOP]: "Archidruida del Robledal",
    [KNIGHT]: "Auriga de Guerra Celta",
    [PAWN]: "Guerrero Gaisata",
    [FALCON]: "Halcón de Hibernia",
    [ELEPHANT]: "Behemot Pictórico",
    [AMAZON]: "Morrigan de la Espesura",
    [GRASSHOPPER]: "Saltador de los Túmulos",
    [NIGHTRIDER]: "Jinete de la Cacería Salvaje",
    [CENTAUR]: "Centauro del Robledal",
    [CAMEL]: "Corcel de las Tierras Altas",
    [LION]: "Sabueso de Ulster",
    [ZEBRA]: "Corcel Pintado de Glasto",
    [PHOENIX]: "Ave de Beltane",
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
  [KNIGHT, "Caballo", "Caballero Hospitalario"],
  [BISHOP, "Alfil", "Prelado del Sol"],
  [QUEEN, "Reina Leonor", "Soberana de las Catedrales"],
  [KING, "Rey Balduino", "Rey Cruzado del Alba"],
  [BISHOP, "Alfil", "Prelada del Sol"],
  [KNIGHT, "Caballo", "Caballero Hospitalario"],
  [ROOK, "Torre", "Bastión Templario"],
];

export const WHITE_ELEPHANT = [ELEPHANT, "Elefante", "Coloso de Ultramar"];
export const BLACK_ELEPHANT = [ELEPHANT, "Elefante", "Coloso de Valaquia"];
export const RED_ELEPHANT = [ELEPHANT, "Elefante", "Elefante Pírrico"];
export const GREEN_ELEPHANT = [ELEPHANT, "Elefante", "Behemot Pictórico"];

export const WHITE_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Cruzado del Alba"]);

export const BLACK_BACK = [
  [ROOK, "Torre", "Ciudadela de los Cárpatos"],
  [KNIGHT, "Caballo", "Húsar de la Noche"],
  [BISHOP, "Alfil", "Boyardo del Eclipse"],
  [QUEEN, "Reina Carmila", "Condesa de la Sangre Nocturna"],
  [KING, "Rey Vladimir", "Voivoda del Eclipse"],
  [BISHOP, "Alfil", "Boyardo del Eclipse"],
  [KNIGHT, "Caballo", "Húsar de la Noche"],
  [ROOK, "Torre", "Ciudadela de los Cárpatos"],
];

export const BLACK_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Guardia de la Empalizada"]);

export const RED_BACK = [
  [ROOK, "Torre", "Castrum Pretoriano"],
  [KNIGHT, "Caballo", "Equite Cataphracto"],
  [BISHOP, "Alfil", "Augur de Marte"],
  [QUEEN, "Reina Gorgo", "Augusta de Hierro y Bronce"],
  [KING, "Rey Leónidas", "Éforo de la Falange Carmesí"],
  [BISHOP, "Alfil", "Augur de Belona"],
  [KNIGHT, "Caballo", "Equite Cataphracto"],
  [ROOK, "Torre", "Castrum Pretoriano"],
];

export const GREEN_BACK = [
  [ROOK, "Torre", "Dun Megalítico"],
  [KNIGHT, "Caballo", "Auriga de Guerra Celta"],
  [BISHOP, "Alfil", "Archidruida del Robledal"],
  [QUEEN, "Reina Boudica", "Reina Guerrera de los Icenos"],
  [KING, "Rey Vercingétorix", "Gran Caudillo de los Clanes"],
  [BISHOP, "Alfil", "Druidesa del Muérdago"],
  [KNIGHT, "Caballo", "Auriga de Guerra Celta"],
  [ROOK, "Torre", "Dun Megalítico"],
];

export const RED_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Hoplita de la Falange"]);

export const GREEN_PAWNS = Array.from({ length: 12 }, () => ["Peón", "Guerrero Gaisata"]);

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
    "El Rey de la Máscara de Plata. Inspirado en los monarcas cruzados de Ultramar, gobierna desde las catedrales de mármol blanco del Alba; aunque su cuerpo sufre bajo la armadura, su fe y su genio táctico jamás han conocido la derrota.",
  "Reina Leonor":
    "Alta soberana franco-normanda de las cortes solares. Diplomática, mecenas de trovadores y estratega implacable que dirigió dos cruzadas; su palabra moviliza órdenes de caballería enteras.",
  "Rey Vladimir":
    "Voivoda supremo de las cumbres de Valaquia y caballero juramentado de la Orden del Dragón. Empaló los estandartes de los invasores en los pasos de los Cárpatos y pactó con la noche eterna para que ningún imperio someta su trono.",
  "Reina Carmila":
    "Condesa inmortal de las criptas de Estiria y Transilvania. Envuelta en terciopelo negro y niebla carmesí, conoce los secretos de la sangre antigua y desarma la voluntad de los generales enemigos antes del alba.",
  "Rey Leónidas":
    "Rey guerrero de linaje heráclida, criado en la agogé del acero y el escudo. Al frente de sus falanges carmesíes y legiones de hierro, jamás pregunta cuántos son los enemigos, sino dónde están formados.",
  "Reina Gorgo":
    "Soberana de Esparta y voz del Senado marcial. Su temple gobierna la patria mientras las legiones marchan; fue ella quien entregó el escudo real con el mandato inmortal: «Vuelve con él o sobre él».",
  "Rey Vercingétorix":
    "Gran caudillo arverno que unificó a las tribus celtas de los bosques bajo el juramento del torque de oro. Maestro de la guerra de emboscadas y los duns fortificados, defiende la libertad ancestral de la espesura.",
  "Reina Boudica":
    "Reina guerrera de los clanes britanos. Conduce su carro de guerra con el cabello al viento y la piel trazada en azul de glasto; su grito de batalla ha reducido a cenizas las colonias de los imperios invasores.",
};

const PAWN_BIOS = {
  [WHITE]:
    "Cruzado juramentado de las encomiendas franco-normandas. Marcha con tabardo blanco y escudo solar, soñando con ser armado caballero en el altar mayor de la catedral.",
  [BLACK]:
    "Guardia fronterizo de los pasos de Valaquia. Avanza entre la niebla de los Cárpatos con alabarda y antorcha apagada, fiel hasta la muerte al Voivoda del Eclipse.",
  [RED]:
    "Hoplita y legionario de primera línea. Avanza tras el muro de escudos de bronce y hierro (phalanx y testudo) con lanza larga y espada corta.",
  [GREEN]:
    "Guerrero gaisata de los clanes celtas, con el cuerpo pintado en espirales de glasto azul, escudo ovalado y venablo de fresno.",
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
    [KING]: "Rey cruzado del Alba. Mientras su corona resista sobre el tablero, las órdenes templarias y hospitalarias no retrocederán.",
    [QUEEN]: "Soberana franco-normanda de la Orden del Alba. Donde ella alza su estandarte solar, las caballerías abren paso.",
    [ROOK]: "Bastión templario de piedra caliza alzado como el Krak de los Caballeros. Sus almenas góticas protegen las líneas del reino.",
    [BISHOP]: "Prelado del Sacro Imperio versado en los códices iluminados y la geometría sagrada de las grandes catedrales.",
    [KNIGHT]: "Caballero hospitalario en armadura de placas y barda blanca. Su carga frontal lanza en ristre quiebra cualquier línea.",
    ...FAIRY_GENERIC_BIOS,
  },
  [BLACK]: {
    [KING]: "Voivoda del Eclipse. Su corona de hierro negro gobierna los pasos montañosos de Valaquia y Transilvania.",
    [QUEEN]: "Condesa nocturna de los Cárpatos. Teje el destino con niebla y sangre antigua desde las criptas del castillo.",
    [ROOK]: "Ciudadela escarpada sobre los riscos de Transilvania, inspirada en el Castillo de Poenari. Sus torres vigilan los desfiladeros.",
    [BISHOP]: "Boyardo y cronista oculto de la corte de Valaquia. Domina los secretos de la Orden del Dragón y el terror nocturno.",
    [KNIGHT]: "Húsar nocturno de los Cárpatos. Cabalga corceles negros a través de la niebla sin ser visto hasta el instante del choque.",
    ...FAIRY_GENERIC_BIOS,
  },
  [RED]: {
    [KING]: "Rey espartano de la Forja Carmesí. Su escudo de bronce y su lanza dictan la ley marcial de la falange.",
    [QUEEN]: "Augusta de Esparta y Roma. Su voz en el Senado y en el campo recuerda que un guerrero vuelve con su escudo o sobre él.",
    [ROOK]: "Castrum pretoriano y torre de asedio romana recubierta de bronce y hierro, imparable en línea recta.",
    [BISHOP]: "Augur marcial del colegio de Marte. Lee los auspicios de guerra y dirige el fuego de los onagros y escorpiones.",
    [KNIGHT]: "Equite cataphracto con coraza escamada y penacho carmesí, forjado para aplastar los flancos enemigos.",
    ...FAIRY_GENERIC_BIOS,
  },
  [GREEN]: {
    [KING]: "Gran caudillo de la Confederación Celta, guardián del torque de oro y de los robledales sagrados.",
    [QUEEN]: "Reina guerrera de los clanes britanos cuyos cánticos de batalla despiertan la furia de las tribus.",
    [ROOK]: "Dun megalítico y muralla gala (murus gallicus) de roble y piedra viva que resiste el hierro y el fuego.",
    [BISHOP]: "Archidruida de los círculos megalíticos que custodia los nemetones y canaliza la fuerza ancestral de la tierra.",
    [KNIGHT]: "Auriga de carro de guerra celta y jinete galo capaz de sortear cualquier obstáculo del bosque.",
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
