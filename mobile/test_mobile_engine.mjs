import assert from "node:assert/strict";
import {
  ALL_COLORS,
  AMAZON,
  BLACK,
  CAMEL,
  CENTAUR,
  ELEPHANT,
  FAIRY_KINDS,
  FALCON,
  GRASSHOPPER,
  GREEN,
  KING,
  LION,
  NIGHTRIDER,
  PAWN,
  PHOENIX,
  RED,
  ROOK,
  WHITE,
  ZEBRA,
  Game,
  createPiece,
  evaluate,
  findBestMove,
  moveNotation,
} from "./js/engine.js";
import * as lore from "./js/lore.js";

// 1. Formación clásica y movimientos iniciales
const g1 = lore.createGame(false);
assert.equal(g1.legalMoves(WHITE).length, 20);
assert.equal(g1.legalMoves(BLACK).length, 20);
assert.equal(g1.pieceAt(7, 4).name, "Rey Balduino");
assert.equal(g1.pieceAt(7, 3).name, "Reina Leonor");
assert.equal(g1.pieceAt(0, 4).name, "Rey Vladimir");
assert.equal(g1.pieceAt(0, 3).name, "Reina Carmila");
assert.equal(g1.pieceAt(7, 0).name, "Torre");
assert.equal(g1.pieceAt(7, 1).name, "Caballo");
assert.equal(g1.pieceAt(7, 2).name, "Alfil");
assert.equal(g1.pieceAt(6, 0).name, "Peón");

// 2. Elefante de guerra (Torre + Caballo) y salto inicial
const g2 = lore.createGame(true);
const ele = g2.pieceAt(7, 2);
assert.equal(ele.kind, ELEPHANT);
const eleMoves = g2.legalMovesFrom(7, 2).map((m) => `${m.tr},${m.tc}`).sort();
assert.deepEqual(eleMoves, ["5,1", "5,3"]);

// 2b. Las 10 piezas míticas de Ajedrez Mágico
const gFairy = new Game();
gFairy.place(createPiece(WHITE, KING, 1, "Rey"), 7, 0);
gFairy.place(createPiece(BLACK, KING, 2, "Rey"), 0, 7);
gFairy.place(createPiece(WHITE, GRASSHOPPER, 3, "Saltamontes"), 4, 4);
gFairy.place(createPiece(WHITE, PAWN, 4, "Pilar"), 4, 6);
gFairy.place(createPiece(BLACK, PAWN, 5, "Sombra"), 2, 4);
const hopMoves = gFairy.legalMovesFrom(4, 4).map((m) => `${m.tr},${m.tc}`).sort();
assert.deepEqual(hopMoves, ["1,4", "4,7"]);

gFairy.place(createPiece(WHITE, LION, 3, "León"), 4, 4);
const lionMoves = gFairy.legalMovesFrom(4, 4).map((m) => `${m.tr},${m.tc}`).sort();
assert.deepEqual(lionMoves, ["0,4", "1,4", "4,7"]);

gFairy.place(createPiece(WHITE, PHOENIX, 3, "Fénix"), 4, 4);
assert.equal(gFairy.legalMovesFrom(4, 4).length, 8);

gFairy.place(createPiece(WHITE, CENTAUR, 3, "Centauro"), 4, 4);
assert.equal(gFairy.legalMovesFrom(4, 4).length, 16);

gFairy.place(createPiece(WHITE, CAMEL, 3, "Camello"), 4, 4);
assert.equal(gFairy.legalMovesFrom(4, 4).length, 8);

gFairy.place(createPiece(WHITE, ZEBRA, 3, "Cebra"), 4, 4);
assert.equal(gFairy.legalMovesFrom(4, 4).length, 8);

gFairy.place(createPiece(WHITE, FALCON, 3, "Halcón"), 4, 4);
assert.ok(gFairy.legalMovesFrom(4, 4).length > 14);

gFairy.place(createPiece(WHITE, AMAZON, 3, "Amazonas"), 4, 4);
assert.ok(gFairy.legalMovesFrom(4, 4).length > 20);

gFairy.place(createPiece(WHITE, NIGHTRIDER, 3, "Noctámbulo"), 7, 1);
const nrMoves = new Set(gFairy.legalMovesFrom(7, 1).map((m) => `${m.tr},${m.tc}`));
assert.equal(nrMoves.has("5,2"), true);
assert.equal(nrMoves.has("3,3"), true);
assert.equal(nrMoves.has("1,4"), true);

// 3. Terrenos diferenciados (peñasco impasable, bosque frena deslizamiento, ruinas fortificadas)
const g3 = new Game();
g3.place(createPiece(WHITE, KING, 1, "Rey"), 7, 4);
g3.place(createPiece(BLACK, KING, 2, "Rey"), 0, 4);
g3.place(createPiece(WHITE, ROOK, 3, "Bastión Aurum", "Centinela", 1, false), 4, 0);
g3.place(createPiece(BLACK, PAWN, 4, "Varok"), 4, 5);
g3.addTerrain("ruinas", 4, 5);

// Ruina protege contra captura lejana
const farTargets = new Set(g3.legalMovesFrom(4, 0).map((m) => `${m.tr},${m.tc}`));
assert.equal(farTargets.has("4,5"), false);

// Captura adyacente y ascenso a Veterano (kills: 1 -> 2)
g3.grid[4][0] = null;
g3.place(createPiece(WHITE, ROOK, 3, "Bastión Aurum", "Centinela", 1, false), 4, 4);
const adjMove = g3.legalMovesFrom(4, 4).find((m) => m.tr === 4 && m.tc === 5);
assert.ok(adjMove);
g3.applyMove(adjMove);
const vetRook = g3.pieceAt(4, 5);
assert.equal(vetRook.kills, 2);
assert.equal(vetRook.veteran, true);

// 4. Niebla de guerra
const vis = g1.visibleSquares(WHITE);
assert.equal(vis.has("7,4"), true);
assert.equal(vis.has("5,4"), true);
assert.equal(vis.has("0,4"), false);

// 5. IA (Oráculo Umbrío)
const best = findBestMove(g2, 2, 0.0, 500);
assert.ok(best);
assert.ok(moveNotation(best).length >= 2);
assert.equal(typeof evaluate(g2), "number");

// 6. Tierra Salvaje, Dilemas y Cruzada Encadenada
const wild = lore.createWildScenario(true);
assert.ok(wild.game.terrain.size >= 6);
const dilemma = lore.wildDilemma(wild.game, wild);
assert.ok(dilemma);
assert.equal(dilemma.options.length, 2);
const choiceEntry = lore.applyWildChoice(wild.game, dilemma.options[0]);
assert.ok(choiceEntry);

const crusade = lore.createCrusade(false);
assert.equal(crusade.roster.length, 16);
const [stageScenario, stageDiff] = lore.createCrusadeStage(crusade, false);
assert.equal(stageDiff, "Escudero");
assert.ok(stageScenario.game.legalMoves(WHITE).length > 0);
const boonMsg = lore.applyCrusadeBoon(crusade, "veteran");
assert.ok(boonMsg.includes("Veterano"));

// 7. Los Cuatro Reinos y Guerra de 4 Frentes
const gRedGreen = lore.createGame(true, RED, GREEN);
assert.equal(gRedGreen.legalMoves(RED).length, 22);
assert.equal(gRedGreen.legalMoves(GREEN).length, 22);
assert.equal(gRedGreen.pieceAt(7, 4).name, "Rey Leónidas");
assert.equal(gRedGreen.pieceAt(7, 3).name, "Reina Gorgo");
assert.equal(gRedGreen.pieceAt(0, 4).name, "Rey Vercingétorix");
assert.equal(gRedGreen.pieceAt(0, 3).name, "Reina Boudica");
for (const c of ALL_COLORS) {
  assert.ok(lore.FACTIONS[c].culture);
  assert.ok(lore.FACTIONS[c].sovereigns);
  assert.ok(lore.FACTIONS[c].lore);
}

const crusadeRed = lore.createCrusade(false, RED);
assert.equal(crusadeRed.player_color, RED);
assert.equal(crusadeRed.stage_rivals.length, 4);

const fourFronts = lore.createFourFrontsGame(true, WHITE);
assert.equal(fourFronts.turn_order.length, 4);
for (const c of ALL_COLORS) {
  assert.ok(fourFronts.findKing(c));
  assert.ok(fourFronts.legalMoves(c).length > 0);
}
const ffMove = findBestMove(fourFronts, 1, 0.0, 400);
assert.ok(ffMove);

// 8. Gran Tablero Imperial 12x12 y Campeón Mítico en Cruzada
const impGame = lore.createImperialGame(WHITE, BLACK);
assert.equal(impGame.size, 12);
const impKinds = new Set();
for (const row of impGame.grid) {
  for (const p of row) {
    if (p) impKinds.add(p.kind);
  }
}
for (const fk of FAIRY_KINDS) {
  assert.equal(impKinds.has(fk), true);
}
assert.ok(impGame.legalMoves(WHITE).length > 40);
const impBest = findBestMove(impGame, 1, 0.0, 400);
assert.ok(impBest);
assert.ok(moveNotation(impBest, false, false, 12).length >= 2);

const mythicMsg = lore.applyCrusadeBoon(crusade, "mythic");
assert.ok(mythicMsg.length > 10);
assert.ok(crusade.roster.some((p) => FAIRY_KINDS.includes(p.kind)));

console.log("ALL MOBILE ENGINE & LORE TESTS PASSED");
