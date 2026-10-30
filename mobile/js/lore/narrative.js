/**
 * Generación de la crónica viva de cada partida (duelos, 4 frentes e Imperio 12x12).
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
} from "../engine.js";
import { FACTIONS, factionName, squareName } from "./catalog.js";

const QUIET_FLAVOR = {
  [PAWN]: [
    "El barro mancha sus botas, pero no detiene su paso.",
    "El pueblo observa en silencio; cada escudero es una promesa.",
    "Un juramento susurrado acompaña sus pasos.",
  ],
  [KNIGHT]: [
    "Las alas del grifo agitan la ceniza del camino.",
    "El viento silba entre las plumas y la armadura.",
    "Desde las alturas, el jinete estudia el tablero como un mapa de guerra.",
  ],
  [BISHOP]: [
    "Un susurro arcano recorre las piedras a su paso.",
    "El aire huele a tormenta y a tinta antigua.",
    "Sus dedos trazan signos que la luz no debería conocer.",
  ],
  [ROOK]: [
    "La tierra tiembla bajo su peso milenario.",
    "Las almenas crujen, como si la fortaleza caminara.",
    "Cada paso deja una grieta en el empedrado.",
  ],
  [QUEEN]: [
    "La luz del reino se inclina ante su voluntad.",
    "Su sombra se alarga más de lo que la luna permite.",
    "Nadie osa mirarla dos veces.",
  ],
  [KING]: [
    "Los estandartes se inclinan al paso del soberano.",
    "El trono queda atrás, pero su peso lo acompaña.",
    "Los guardias redoblan la vigilancia.",
  ],
  [FALCON]: [
    "El halcón corta el viento en diagonal y cambia de rumbo en pleno vuelo.",
    "Sus alas proyectan una sombra veloz sobre las columnas enemigas.",
  ],
  [ELEPHANT]: [
    "Cada paso suyo hace temblar las losas del tablero.",
    "El coloso avanza como una torre y salta sobre los flancos con furia.",
  ],
  [AMAZON]: [
    "La valquiria domina cada línea y cada salto; el campo entero contiene el aliento.",
    "Su lanza brilla con la autoridad de una reina y la agilidad de un jinete.",
  ],
  [GRASSHOPPER]: [
    "Toma impulso sobre una silueta aliada y cae detrás como una flecha viva.",
    "Un resorte arcano lo proyecta justo al otro lado del obstáculo.",
  ],
  [NIGHTRIDER]: [
    "Su montura encadena galopes imposibles a través de la penumbra.",
    "El noctámbulo cruza el campo en una sucesión de saltos espectrales.",
  ],
  [CENTAUR]: [
    "Sus cascos golpean la piedra con la firmeza de un rey y el brío de un corcel.",
    "El centauro patrulla la vanguardia sin temer el acero cercano.",
  ],
  [CAMEL]: [
    "Su zancada larga de tres pasos cruza la arena sin cambiar jamás de color.",
    "El camello de guerra sortea las trincheras con paso inalterable.",
  ],
  [LION]: [
    "El león ruge, salta sobre la línea frontal y aterriza en la retaguardia.",
    "Su melena corta el aire mientras planea más allá del obstáculo.",
  ],
  [ZEBRA]: [
    "Un salto oblicuo de tres por dos desconcierta a los arqueros rivales.",
    "La cebra de guerra traza un ángulo imposible sobre el campo.",
  ],
  [PHOENIX]: [
    "Un destello de brasas marca su salto diagonal sobre las defensas.",
    "Las plumas incandescentes iluminan la niebla a su paso.",
  ],
};

const CAPTURE_FLAVOR = {
  [PAWN]: [
    "El escudero clava su lanza con la furia de quien no tiene nada que perder.",
    "Un golpe certero basta para abrir la primera herida.",
  ],
  [KNIGHT]: [
    "El grifo cae en picada y sus garras no perdonan.",
    "El jinete pasa como una sombra y deja el campo sembrado de acero.",
  ],
  [BISHOP]: [
    "Una palabra prohibida prende fuego al aire.",
    "El magíster dibuja un signo y la armadura enemiga se resquebraja.",
  ],
  [ROOK]: [
    "El impacto hace temblar el tablero entero.",
    "La fortaleza avanza como un alud de piedra y hierro.",
  ],
  [QUEEN]: [
    "Un solo gesto suyo basta para cambiar el destino de la batalla.",
    "La reina no pide permiso; el campo se rinde a su paso.",
  ],
  [KING]: [
    "El soberano no debería luchar, pero su acero es tan antiguo como su corona.",
    "El rey rompe la formación enemiga con una furia que nadie recordaba.",
  ],
  [FALCON]: [
    "Desciende desde las nubes en un giro letal que destroza el escudo rival.",
    "Sus garras arcanas abaten al enemigo antes de que pueda alzar la vista.",
  ],
  [ELEPHANT]: [
    "El impacto de sus colmillos parte el aire y la formación enemiga.",
    "La montaña de guerra embiste y no deja piedra sobre piedra.",
  ],
  [AMAZON]: [
    "Desata una tormenta de acero y fuego contra la que no existe defensa.",
    "La guerrera suprema ejecuta un golpe que resuena en todo Aethelgard.",
  ],
  [GRASSHOPPER]: [
    "Salta por encima del frente y cae directamente sobre su presa.",
    "Una emboscada acrobática derriba al defensor al otro lado del muro.",
  ],
  [NIGHTRIDER]: [
    "Su carga encadenada atraviesa medio tablero antes de abatir a su presa.",
    "Surge tras tres saltos consecutivos como un relámpago en la noche.",
  ],
  [CENTAUR]: [
    "Arrolla al rival con alabarda y cascos de bronce.",
    "Su embestida híbrida quiebra la guardia enemiga de un solo tajo.",
  ],
  [CAMEL]: [
    "Su zancada profunda sorprende al enemigo desde tres casillas de distancia.",
    "Cruza el flanco de un salto largo y derriba al defensor.",
  ],
  [LION]: [
    "Salta sobre la muralla humana y devora la línea trasera.",
    "Su rugido precede a un salto devastador que rompe la retaguardia.",
  ],
  [ZEBRA]: [
    "Su salto en ángulo abierto burla todos los escudos y golpea el flanco.",
    "Aparece desde una diagonal inesperada y derriba a su objetivo.",
  ],
  [PHOENIX]: [
    "Renace entre llamas sobre la casilla enemiga, reduciendo su guardia a cenizas.",
    "Un salto ígneo consume la posición rival en un instante.",
  ],
};

const CHECK_PHRASES = [
  "El Rey enemigo palidece: ¡jaque!",
  "Las campanas de la torre redoblan: ¡el Rey está en jaque!",
  "Un escalofrío recorre el trono: ¡jaque!",
  "La guardia enemiga se rompe en gritos: ¡jaque!",
  "El acero brilla demasiado cerca de la corona: ¡jaque!",
];

export const PROMOTION_ROLE = {
  [AMAZON]: "una Amazonas legendaria",
  [QUEEN]: "una Dama de guerra",
  [ELEPHANT]: "un Elefante de asedio",
  [FALCON]: "un Halcón de tormenta",
  [ROOK]: "una Torre viviente",
  [BISHOP]: "un Alfil consagrado",
  [KNIGHT]: "un Caballo de tormenta",
};

export const PROMOTED_TITLE = {
  [AMAZON]: "Amazonas Consagrada",
  [QUEEN]: "Dama de Guerra",
  [ELEPHANT]: "Elefante Consagrado",
  [FALCON]: "Halcón Consagrado",
  [ROOK]: "Torre de Asedio",
  [BISHOP]: "Alfil Consagrado",
  [KNIGHT]: "Caballo de Tormenta",
};

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

export function toRoman(number) {
  let n = number;
  const values = [
    [1000, "M"], [900, "CM"], [500, "D"], [400, "CD"],
    [100, "C"], [90, "XC"], [50, "L"], [40, "XL"],
    [10, "X"], [9, "IX"], [5, "V"], [4, "IV"], [1, "I"],
  ];
  const result = [];
  for (const [val, sym] of values) {
    while (n >= val) {
      result.push(sym);
      n -= val;
    }
  }
  return result.join("") || "I";
}

export function prologue(
  vsAi,
  difficulty = "",
  elephant = false,
  fog = false,
  playerColor = WHITE,
  enemyColor = BLACK,
) {
  const pInfo = FACTIONS[playerColor] || FACTIONS[WHITE];
  const eInfo = FACTIONS[enemyColor] || FACTIONS[BLACK];
  const pName = pInfo.name;
  const eName = eInfo.name;
  const officers = elephant
    ? "un oficial arcano, un elefante de guerra"
    : "dos oficiales arcanos";
  let text =
    "En la era en que las piedras recuerdan y los cuervos hablan, el reino de " +
    `Aethelgard se fractura en múltiples frentes. ${pName} (${pInfo.culture}, ` +
    `liderada por ${pInfo.sovereigns}) despliega sus estandartes en el sur ` +
    `mientras ${eName} (${eInfo.culture}, bajo ${eInfo.sovereigns}) marcha desde el norte.\n\n` +
    `Ocho unidades de vanguardia, ${officers}, dos jinetes, dos baluartes, una ` +
    "soberana y un monarca aguardan en cada bando. Cada paso será una página; " +
    "cada caída, una herida en la historia.";

  if (elephant) {
    text +=
      "\n\nUn Elefante de Guerra ocupa el lugar de un oficial arcano en cada bando: " +
      "combina el movimiento de la Torre con el salto del Caballo.";
  }
  if (fog) {
    text +=
      "\n\nUna niebla de guerra cubre el tablero. Solo verás las casillas que tus " +
      "propias piezas vigilen; lo que aceche fuera de su alcance permanecerá oculto.";
  }
  if (vsAi) {
    const oracle =
      {
        Escudero: `Al otro lado del tablero, un comandante novel guía a ${eName}.`,
        Caballero: `Al otro lado, un general curtido comanda a ${eName}.`,
        Archimago: `Al otro lado, un estratega que lee el porvenir dirige a ${eName}.`,
      }[difficulty] || "Al otro lado, el Oráculo Umbrío acecha.";
    text += `\n\n${oracle}\n\nQue comience la crónica.`;
  } else {
    text += "\n\nDos voluntades se enfrentan sobre el tablero.\n\nQue comience la crónica.";
  }
  return { heading: "Prólogo · Los estandartes enfrentados", text, tag: "prologue" };
}

export function imperialPrologue(
  vsAi,
  difficulty = "",
  fog = false,
  playerColor = WHITE,
  enemyColor = BLACK,
) {
  const pName = factionName(playerColor);
  const eName = factionName(enemyColor);
  let text =
    "Las crónicas mayores se abren sobre el Gran Tablero Imperial de 12x12 " +
    `casillas. ${pName} y ${eName} han convocado a las diez órdenes míticas ` +
    "del Códice de Aethelgard: Halcones, Elefantes, Amazonas, Saltamontes, " +
    "Noctámbulos, Centauros, Camellos, Leones, Cebras y Fénix.\n\n" +
    "Tres filas completas de treinta y seis piezas por bando aguardan la " +
    "señal de ataque. Los peones que alcancen la última fila podrán ascender " +
    "incluso al rango de Amazonas.";
  if (fog) {
    text +=
      "\n\nLa niebla de guerra cubre las doce columnas: explora con tus " +
      "saltadores antes de avanzar la línea real.";
  }
  if (vsAi) {
    text +=
      `\n\nEl Oráculo (${difficulty || "Caballero"}) comanda las legiones ` +
      `de ${eName}.\n\nQue comience la Crónica Imperial.`;
  } else {
    text += "\n\nDos imperios completos frente a frente.\n\nQue comience la Crónica Imperial.";
  }
  return { heading: "Prólogo · Gran Tablero Imperial (12x12)", text, tag: "prologue" };
}

export function fourFrontsPrologue(
  vsAi,
  difficulty = "",
  elephant = false,
  fog = false,
  playerColor = WHITE,
) {
  const pName = factionName(playerColor);
  let text =
    "Las trompetas de los cuatro puntos cardinales resuenan al unísono. " +
    "La Orden del Alba, la Forja Carmesí, la Legión del Eclipse y el Pacto " +
    "de la Espesura convergen sobre la encrucijada central de Aethelgard.\n\n" +
    `Comandas a ${pName} desde el frente sur. Tres ejércitos rivales ` +
    "asedian desde el oeste, el norte y el este. Cuando un monarca cae o se " +
    "queda sin movimientos legales, su frente entero se desmorona.";
  if (elephant) {
    text +=
      "\n\nCada uno de los cuatro reinos ha desplegado un coloso de guerra " +
      "en su flanco de vanguardia.";
  }
  if (fog) {
    text +=
      "\n\nLa niebla de guerra envuelve los cuatro frentes: solo verás " +
      "aquello que tus propias unidades alcancen a divisar.";
  }
  if (vsAi) {
    text +=
      `\n\nTres comandantes regidos por el Oráculo (${difficulty || "Caballero"}) ` +
      "disputan la corona al mismo tiempo.\n\nQue comience la Guerra de los Cuatro Frentes.";
  } else {
    text += "\n\nCuatro tronos, un solo campo.\n\nQue comience la Guerra de los Cuatro Frentes.";
  }
  return { heading: "Prólogo · Guerra de los Cuatro Frentes", text, tag: "prologue" };
}

export function narrateMove(move, game, check, mate, chapter) {
  const piece = move.moved;
  const size = game.size || 8;
  const dest = squareName(move.tr, move.tc, size);
  const origin = squareName(move.fr, move.fc, size);
  const mover = piece.name;
  const victim = move.captured ? move.captured.name : null;
  const flavor = pick(QUIET_FLAVOR[piece.kind] || QUIET_FLAVOR[PAWN]);
  const captureFlavor = pick(CAPTURE_FLAVOR[piece.kind] || CAPTURE_FLAVOR[PAWN]);
  const checkText = check && !mate ? ` ${pick(CHECK_PHRASES)}` : "";
  const fallen = move.eliminated_factions || [];
  const elimText = fallen.length
    ? ` ¡El frente de ${fallen.map(factionName).join(", ")} se derrumba y sus tropas abandonan el campo!`
    : "";

  if (mate) {
    const body = victim
      ? pick([
          `El acero de ${mover} encuentra a ${victim} en ${dest}. ${captureFlavor}${elimText} El último estandarte cae: ¡jaque mate!`,
          `En ${dest}, ${mover} derriba a ${victim} y cierra el cerco.${elimText} No hay escudo, ni huida, ni milagro: ¡jaque mate!`,
        ])
      : pick([
          `${mover} cierra el cerco en ${dest}.${elimText} No hay escudo, ni huida, ni milagro: ¡jaque mate!`,
          `En ${dest}, la última defensa se quiebra.${elimText} ${mover} alza su arma bajo un cielo que deja de respirar: ¡jaque mate!`,
        ]);
    return {
      heading: `Crónica ${toRoman(chapter)} · El último estandarte`,
      text: body,
      tag: "mate",
    };
  }

  if (move.promotion) {
    const role = PROMOTION_ROLE[move.promotion] || "un campeón consagrado";
    const captureLine = victim ? ` Antes de ascender, su acero derriba a ${victim}.` : "";
    const body = pick([
      `${mover} alcanza el altar de coronación en ${dest}. La piedra arde y renace como ${role}.${captureLine}${elimText}${checkText}`,
      `En ${dest}, el último escalón se ilumina. ${mover} deja atrás su juramento de escudero y se alza como ${role}.${captureLine}${elimText}${checkText}`,
    ]);
    return {
      heading: `Crónica ${toRoman(chapter)} · El ascenso de ${mover}`,
      text: body,
      tag: "promo",
    };
  }

  if (move.castle) {
    const row = move.tr;
    const rookCol = move.castle === "K" ? 5 : 3;
    const rook = game.grid[row][rookCol];
    const rookName = rook ? rook.name : "el centinela";
    const side = move.castle === "K" ? "flanco del rey" : "flanco de la reina";
    const body = pick([
      `${mover} ordena cerrar filas: se repliega hacia ${dest} mientras ${rookName} ocupa su puesto tras las murallas. ¡Enroque en el ${side}!`,
      `Las trompetas suenan dos veces. ${mover} se refugia en ${dest} y ${rookName} sella la muralla. ¡Enroque en el ${side}!`,
    ]);
    return {
      heading: `Crónica ${toRoman(chapter)} · Muros y coronas`,
      text: body,
      tag: "castle",
    };
  }

  if (move.is_en_passant && victim) {
    const body = `La niebla se abre: ${mover} sorprende a ${victim} en ${dest}, cortándole la retirada. ¡Emboscada en las aguas turbias!${elimText}${checkText}`;
    return {
      heading: `Crónica ${toRoman(chapter)} · Emboscada en la niebla`,
      text: body,
      tag: "capture",
    };
  }

  if (victim) {
    let vetNote = "";
    if (move.placed && move.placed.veteran && !piece.veteran) {
      vetNote = ` ¡${mover} alcanza el rango de Veterano tras su segunda victoria!`;
    }
    const body = pick([
      `¡${mover} se abalanza sobre ${victim} en ${dest}! ${captureFlavor} El primer grito de la guerra rompe el silencio.${vetNote}${elimText}${checkText}`,
      `En ${dest}, el acero de ${mover} encuentra a ${victim}. ${captureFlavor}${vetNote}${elimText}${checkText}`,
      `${mover} desafía a ${victim} y lo derriba en ${dest}. ${captureFlavor}${vetNote}${elimText}${checkText}`,
      `La tierra bebe sangre en ${dest}: ${mover} vence a ${victim}. ${captureFlavor}${vetNote}${elimText}${checkText}`,
    ]);
    const tag = check ? "check" : "capture";
    const heading = check ? "El trono tiembla" : `Sangre en ${dest}`;
    return {
      heading: `Crónica ${toRoman(chapter)} · ${heading}`,
      text: body,
      tag,
    };
  }

  if (check) {
    const body = pick([
      `${mover} avanza de ${origin} a ${dest}. ${flavor}${elimText}${checkText}`,
      `Las crónicas registran el paso de ${mover} por ${dest}. ${flavor}${elimText}${checkText}`,
      `${mover} toma posición en ${dest} sin derramar sangre… por ahora. ${flavor}${elimText}${checkText}`,
    ]);
    return {
      heading: `Crónica ${toRoman(chapter)} · El trono tiembla`,
      text: body,
      tag: "check",
    };
  }

  const body = pick([
    `${mover} parte de ${origin} y avanza hacia ${dest}. ${flavor}${elimText}`,
    `Las crónicas registran el paso de ${mover} por ${dest}. ${flavor}${elimText}`,
    `Bajo un cielo de ceniza, ${mover} toma posición en ${dest}. ${flavor}${elimText}`,
    `${mover} se interna en ${dest} sin derramar sangre… todavía. ${flavor}${elimText}`,
  ]);
  return {
    heading: `Crónica ${toRoman(chapter)} · El paso de ${mover}`,
    text: body,
    tag: "move",
  };
}

export function fogEntry(chapter) {
  const body = pick([
    "Algo se mueve más allá de la niebla. El tablero respira, pero no revela sus secretos.",
    "Un roce de acero y un paso apagado. Cuando la niebla se abre, solo queda la sospecha de una pieza en marcha.",
    "Las antorchas parpadean. En algún lugar del tablero, una voluntad oculta acaba de moverse.",
    "La niebla traga el sonido de una jugada. Ni el nombre ni el destino cruzan hasta tu lado del campo.",
  ]);
  return {
    heading: `Crónica ${toRoman(chapter)} · Voces en la niebla`,
    text: body,
    tag: "fog",
  };
}

export function ambientEntry(size = 8) {
  const r = Math.floor(Math.random() * size);
  const c = Math.floor(Math.random() * size);
  const loc = squareName(r, c, size);
  const line = pick([
    `Los cuervos sobrevuelan ${loc}. Nada ha muerto aún… esta noche.`,
    `Bajo ${loc}, una raíz antigua bebe la sangre derramada.`,
    `Los estandartes ondean sobre ${loc}; el viento huele a hierro.`,
    `Un bardo canta en ${loc}. Su canción habla de reyes que caerán.`,
    `En ${loc}, la luna se oculta tras una nube que no debería existir.`,
    `Alguien ha encendido una vela en ${loc}. Nadie sabe quién.`,
  ]);
  return { heading: "Eco del reino", text: line, tag: "ambient" };
}

const VICTORY_EPILOGUES = {
  [WHITE]: {
    heading: "Epílogo · El Trono de la Luz",
    text:
      "El último estandarte rival cae. Las órdenes templarias de la Orden del " +
      "Alba recuperan el Trono de Aethelgard bajo el Rey Balduino y la Reina " +
      "Leonor, y las campanas de las catedrales blancas resuenan durante cien " +
      "inviernos.",
  },
  [BLACK]: {
    heading: "Epílogo · La Era del Eclipse",
    text:
      "Las defensas enemigas se quiebran entre la niebla de los Cárpatos. El " +
      "Rey Vladimir y la Reina Carmila alzan el estandarte de la Orden del " +
      "Dragón sobre el Trono de Aethelgard; esa noche, el sol no se atreve a " +
      "salir.",
  },
  [RED]: {
    heading: "Epílogo · El Imperio del Bronce y el Hierro",
    text:
      "Las falanges espartanas y las legiones de la Forja Carmesí marchan " +
      "victoriosas sobre el campo conquistado. El Rey Leónidas y la Reina " +
      "Gorgo alzan sus escudos sobre el Trono de Aethelgard e inauguran la " +
      "Era Marcial.",
  },
  [GREEN]: {
    heading: "Epílogo · El Triunfo de los Clanes",
    text:
      "Los robledales sagrados y los círculos megalíticos reclaman las piedras " +
      "del trono. El Rey Vercingétorix y la Reina Boudica devuelven Aethelgard " +
      "a la Confederación Celta del Pacto de la Espesura, donde ningún imperio " +
      "volverá a someter la tierra.",
  },
};

export function epilogue(result) {
  const rtype = result.type;
  const winner = result.winner;
  if (rtype === "checkmate" && VICTORY_EPILOGUES[winner]) {
    return { ...VICTORY_EPILOGUES[winner], tag: "epilogue" };
  }
  if (rtype === "surrender") {
    const loserName = factionName(result.loser || WHITE);
    const winnerName = winner ? factionName(winner) : "el ejército rival";
    const text =
      `${loserName} dobla su estandarte. No hay más cadáveres que contar, ` +
      `solo el silencio de una rendición. ${winnerName} avanza sin ` +
      "encontrar resistencia y el trono queda a su merced.";
    return { heading: "Epílogo · El estandarte doblado", text, tag: "epilogue" };
  }
  if (rtype === "stalemate") {
    return {
      heading: "Epílogo · El equilibrio imposible",
      text:
        "Ningún bando puede dar un paso sin condenarse. Las espadas quedan " +
        "suspendidas en el aire y los reyes se miran sin parpadear. Los dioses " +
        "declaran tablas; Aethelgard respira, pero no olvida.",
      tag: "epilogue",
    };
  }
  if (rtype === "material") {
    return {
      heading: "Epílogo · Las espadas guardadas",
      text:
        "Quedan tan pocas fuerzas sobre el tablero que ninguna victoria sería " +
        "posible. Los generales guardan el acero y firman una tregua bajo la " +
        "lluvia. Aethelgard gana tiempo; el Eclipse, paciencia.",
      tag: "epilogue",
    };
  }
  return {
    heading: "Epílogo · Cincuenta inviernos",
    text:
      "Cincuenta inviernos sin que caiga una sola corona. El tablero se cubre de " +
      "polvo y los ejércitos envejecen mirándose. Los dioses declaran tablas para " +
      "que la historia pueda seguir su curso.",
    tag: "epilogue",
  };
}

const VICTORY_TITLES = {
  [WHITE]: ["VICTORIA DEL ALBA", "El Trono de la Luz vuelve a brillar"],
  [BLACK]: ["VICTORIA DEL ECLIPSE", "La ceniza cubre Aethelgard"],
  [RED]: ["VICTORIA DE LA FORJA", "El fuego carmesí domina Aethelgard"],
  [GREEN]: ["VICTORIA DEL PACTO", "El bosque ancestral reclama el trono"],
};

/** Devuelve [título, subtítulo, color lógico]. */
export function resultTitle(result) {
  const winner = result.winner;
  const rtype = result.type;
  if (rtype === "checkmate" || rtype === "surrender") {
    const key = VICTORY_TITLES[winner] ? winner : BLACK;
    return [...VICTORY_TITLES[key], key];
  }
  if (rtype === "stalemate") {
    return ["TABLAS", "El equilibrio detiene la guerra", "draw"];
  }
  if (rtype === "fifty") {
    return ["TABLAS", "Cincuenta inviernos sin sangre", "draw"];
  }
  return ["TABLAS", "Las espadas se guardan", "draw"];
}

export function resultIcon(result) {
  const faction = FACTIONS[result.winner];
  return faction ? faction.crest : "⚖";
}
