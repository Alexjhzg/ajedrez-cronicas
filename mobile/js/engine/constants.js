/**
 * Constantes compartidas por las reglas, terrenos y el motor de IA.
 */

export const WHITE = "w"; // Orden del Alba
export const BLACK = "b"; // Legión del Eclipse
export const RED = "c";   // Forja Carmesí
export const GREEN = "v"; // Reino de Avalon

export const ALL_COLORS = [WHITE, RED, BLACK, GREEN];

export const PAWN = "p";
export const KNIGHT = "n";
export const BISHOP = "b";
export const ROOK = "r";
export const QUEEN = "q";
export const KING = "k";

// 10 Piezas del Códice Expandido (Fairy Chess / Crónicas de Aethelgard)
export const FALCON = "h";      // 1. Halcón (Alfil + Caballo)
export const ELEPHANT = "e";    // 2. Elefante (Torre + Caballo)
export const AMAZON = "a";      // 3. Amazonas (Reina + Caballo)
export const GRASSHOPPER = "s"; // 4. Saltamontes (Salto obligatorio sobre 1 pieza)
export const NIGHTRIDER = "g";  // 5. Noctámbulo (Saltos repetidos de Caballo)
export const CENTAUR = "u";     // 6. Centauro (Rey + Caballo)
export const CAMEL = "m";       // 7. Camello (Salto L de 3x1)
export const LION = "l";        // 8. León (Salto sobre 1 pieza y aterriza más allá)
export const ZEBRA = "z";       // 9. Cebra (Salto L de 3x2)
export const PHOENIX = "f";     // 10. Fénix (1 paso ortogonal + salto diagonal 2x2)

export const FAIRY_KINDS = [
  FALCON,
  ELEPHANT,
  AMAZON,
  GRASSHOPPER,
  NIGHTRIDER,
  CENTAUR,
  CAMEL,
  LION,
  ZEBRA,
  PHOENIX,
];

export const PIECE_VALUE = {
  [PAWN]: 100,
  [ZEBRA]: 230,
  [CAMEL]: 260,
  [GRASSHOPPER]: 280,
  [PHOENIX]: 310,
  [KNIGHT]: 320,
  [BISHOP]: 330,
  [ROOK]: 500,
  [NIGHTRIDER]: 540,
  [CENTAUR]: 560,
  [LION]: 680,
  [FALCON]: 720,
  [ELEPHANT]: 850,
  [QUEEN]: 900,
  [AMAZON]: 1250,
  [KING]: 20000,
};

export const PIECE_LETTER_ES = {
  [KING]: "R",
  [QUEEN]: "D",
  [ROOK]: "T",
  [BISHOP]: "A",
  [KNIGHT]: "C",
  [FALCON]: "H",
  [ELEPHANT]: "E",
  [AMAZON]: "M",
  [GRASSHOPPER]: "S",
  [NIGHTRIDER]: "N",
  [CENTAUR]: "U",
  [CAMEL]: "J",
  [LION]: "L",
  [ZEBRA]: "Z",
  [PHOENIX]: "F",
  [PAWN]: "",
};

export const FILE_LETTERS = "abcdefghijkl";

export const KNIGHT_DELTAS = [
  [-2, -1], [-2, 1], [-1, -2], [-1, 2],
  [1, -2], [1, 2], [2, -1], [2, 1],
];
export const CAMEL_DELTAS = [
  [-3, -1], [-3, 1], [-1, -3], [-1, 3],
  [1, -3], [1, 3], [3, -1], [3, 1],
];
export const ZEBRA_DELTAS = [
  [-3, -2], [-3, 2], [-2, -3], [-2, 3],
  [2, -3], [2, 3], [3, -2], [3, 2],
];
export const KING_DELTAS = [
  [-1, -1], [-1, 0], [-1, 1],
  [0, -1], [0, 1],
  [1, -1], [1, 0], [1, 1],
];
export const BISHOP_DIRS = [[-1, -1], [-1, 1], [1, -1], [1, 1]];
export const ROOK_DIRS = [[-1, 0], [1, 0], [0, -1], [0, 1]];
export const QUEEN_DIRS = [...BISHOP_DIRS, ...ROOK_DIRS];
export const ALFIL_DELTAS = [[-2, -2], [-2, 2], [2, -2], [2, 2]];
export const ELEPHANT_DELTAS = ALFIL_DELTAS;

export const IMPASSABLE_TERRAIN = new Set([
  "acantilado", "penasco", "empalizada", "escombros",
]);
export const PASSABLE_TERRAIN = new Set(["bosque", "rio", "ruinas"]);
export const VISION_BLOCKING_TERRAIN = new Set([
  "bosque", "acantilado", "penasco", "empalizada", "escombros",
]);
export const FORTIFIED_TERRAIN = new Set(["ruinas"]);
export const SLOW_TERRAIN = new Set(["rio"]);

export function other(color) {
  return color === WHITE ? BLACK : WHITE;
}
