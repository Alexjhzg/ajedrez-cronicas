/**
 * Modo Cruzada Encadenada Multi-Frente: progresión, rivales y refuerzos míticos.
 */

import {
  BLACK,
  CENTAUR,
  ELEPHANT,
  FALCON,
  GREEN,
  KING,
  KNIGHT,
  LION,
  NIGHTRIDER,
  PAWN,
  PHOENIX,
  RED,
  WHITE,
  Game,
  createPiece,
} from "../engine.js";
import { createGame, factionName, rivalFactions } from "./catalog.js";
import {
  NAME_POOLS,
  THEMES,
  TITLES,
  armyKinds,
  armySummary,
  createWildScenario,
  generateTerrain,
  isPlayable,
  makePieces,
  shuffle,
  terrainSummary,
} from "./wilds.js";

export const CRUSADE_STAGES = [
  ["bosque", "Etapa I · El Bosque de los Susurros", "Escudero"],
  ["rio", "Etapa II · La Ribera de Ceniza", "Caballero"],
  ["paso", "Etapa III · El Paso del Dragón", "Caballero"],
  ["ruinas", "Etapa IV · Las Ruinas del Trono", "Archimago"],
];

function buildStageRivals(playerColor) {
  if (playerColor === WHITE) return [GREEN, RED, RED, BLACK];
  if (playerColor === BLACK) return [GREEN, RED, WHITE, WHITE];
  if (playerColor === RED) return [GREEN, WHITE, BLACK, BLACK];
  if (playerColor === GREEN) return [RED, WHITE, BLACK, BLACK];
  const rivals = rivalFactions(playerColor);
  return [rivals[0], rivals[1], rivals[1], rivals[2]];
}

export function createCrusade(elephant = false, playerColor = WHITE) {
  const rivals = buildStageRivals(playerColor);
  const baseGame = createGame(elephant, playerColor, rivals[0]);
  const roster = [];
  let maxPid = 1;
  for (const r of [6, 7]) {
    for (let c = 0; c < 8; c++) {
      const p = baseGame.grid[r][c];
      if (p && p.color === playerColor) {
        roster.push(p);
        if (p.pid >= maxPid) maxPid = p.pid + 1;
      }
    }
  }
  return {
    stage: 0,
    total_stages: CRUSADE_STAGES.length,
    roster,
    next_pid: maxPid + 32,
    victories: 0,
    player_color: playerColor,
    stage_rivals: rivals,
  };
}

export function createCrusadeStage(crusade, elephant = false) {
  const idx = Math.min(crusade.stage, CRUSADE_STAGES.length - 1);
  const [theme, stageTitle, stageDiff] = CRUSADE_STAGES[idx];
  const playerC = crusade.player_color || WHITE;
  const rivals = crusade.stage_rivals || buildStageRivals(playerC);
  const enemyC = rivals[Math.min(idx, rivals.length - 1)];

  const enemyComp = armyKinds(elephant);
  let terrain = new Map();
  let game = null;

  for (let attempt = 0; attempt < 120; attempt++) {
    terrain = generateTerrain(theme);
    const candidate = new Game([playerC, enemyC]);
    for (const [key, kind] of terrain.entries()) {
      const [r, c] = key.split(",").map(Number);
      candidate.addTerrain(kind, r, c);
    }
    const playerSlots = [];
    for (const r of [6, 7]) {
      for (let c = 0; c < 8; c++) {
        if (!candidate.isBlocked(r, c)) playerSlots.push([r, c]);
      }
    }
    if (playerSlots.length < crusade.roster.length) continue;
    shuffle(playerSlots);
    for (let i = 0; i < crusade.roster.length; i++) {
      candidate.place(crusade.roster[i], playerSlots[i][0], playerSlots[i][1]);
    }

    const enemyKinds = shuffle([...enemyComp]);
    const [enemyPieces, nextPid] = makePieces(enemyC, enemyKinds, crusade.next_pid);
    crusade.next_pid = nextPid;
    const enemySlots = [];
    for (const r of [0, 1]) {
      for (let c = 0; c < 8; c++) {
        if (!candidate.isBlocked(r, c)) enemySlots.push([r, c]);
      }
    }
    if (enemySlots.length < enemyPieces.length) continue;
    shuffle(enemySlots);
    for (let i = 0; i < enemyPieces.length; i++) {
      candidate.place(enemyPieces[i], enemySlots[i][0], enemySlots[i][1]);
    }

    if (isPlayable(candidate)) {
      game = candidate;
      break;
    }
  }

  if (!game) {
    const fallback = createWildScenario(elephant, playerC, enemyC);
    return [fallback, stageDiff];
  }

  const meta = THEMES[theme];
  const rivalLabel = factionName(enemyC);
  const scenario = {
    game,
    theme,
    title: `${stageTitle} · Frente a ${rivalLabel}`,
    description: meta.description,
    terrain_summary: terrainSummary(terrain),
    army_summary: armySummary(crusade.roster.map((p) => p.kind)),
  };
  return [scenario, stageDiff];
}

export function updateCrusadeSurvivors(crusade, game) {
  const playerC = crusade.player_color || WHITE;
  const n = game.size || 8;
  const survivors = [];
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const p = game.grid[r][c];
      if (p && p.color === playerC) survivors.push(p);
    }
  }
  if (!survivors.some((p) => p.kind === KING)) {
    const kingName = (NAME_POOLS[playerC] || NAME_POOLS[WHITE])[KING][0];
    const kingTitle = (TITLES[playerC] || TITLES[WHITE])[KING];
    survivors.unshift(createPiece(playerC, KING, 5, kingName, kingTitle));
  }
  crusade.roster = survivors;
  return survivors;
}

export function applyCrusadeBoon(crusade, boon) {
  const playerC = crusade.player_color || WHITE;
  if (boon === "knight" || boon === "reinforce" || boon === "mythic") {
    const pool =
      boon === "mythic"
        ? [FALCON, LION, NIGHTRIDER, CENTAUR, PHOENIX]
        : [KNIGHT, CENTAUR, PHOENIX, FALCON];
    const vanguardKind = pool[Math.floor(Math.random() * pool.length)];
    const [pieces, nextPid] = makePieces(playerC, [vanguardKind], crusade.next_pid);
    crusade.next_pid = nextPid;
    if (crusade.roster.length < 16) {
      crusade.roster.push(pieces[0]);
      return `${pieces[0].name} (${pieces[0].title}) se une a tu estandarte.`;
    }
    const pawnIdx = crusade.roster.findIndex((p) => p.kind === PAWN && !p.veteran);
    if (pawnIdx >= 0) {
      const old = crusade.roster[pawnIdx];
      crusade.roster[pawnIdx] = pieces[0];
      return `${old.name} cede su puesto de vanguardia a ${pieces[0].name} (${pieces[0].title}).`;
    }
    return "Las filas de tu reino marchan completas.";
  }

  if (boon === "elephant") {
    const [pieces, nextPid] = makePieces(playerC, [ELEPHANT], crusade.next_pid);
    crusade.next_pid = nextPid;
    if (crusade.roster.length < 16) {
      crusade.roster.unshift(pieces[0]);
      return `${pieces[0].name} se une a la vanguardia como coloso de guerra.`;
    }
    const pawnIdx = crusade.roster.findIndex((p) => p.kind === PAWN);
    if (pawnIdx >= 0) {
      crusade.roster[pawnIdx] = pieces[0];
      return `${pieces[0].name} reemplaza a una unidad ligera en la vanguardia.`;
    }
    return "Un coloso de guerra marcha junto al ejército.";
  }

  if (boon === "veteran") {
    const candidates = crusade.roster
      .map((p, i) => [p, i])
      .filter(([p]) => p.kind !== KING && !p.veteran);
    shuffle(candidates);
    const chosen = candidates.slice(0, 2);
    const names = [];
    for (const [p, idx] of chosen) {
      crusade.roster[idx] = createPiece(
        p.color,
        p.kind,
        p.pid,
        p.name,
        p.title,
        Math.max(2, p.kills),
        true
      );
      names.push(p.name);
    }
    return names.length > 0
      ? `Ascendidos al rango de Veterano: ${names.join(" y ")}.`
      : "Tus oficiales ya ostentan el rango de Veterano.";
  }

  const added = [];
  for (let i = 0; i < 3; i++) {
    if (crusade.roster.length >= 16) break;
    const [pieces, nextPid] = makePieces(playerC, [PAWN], crusade.next_pid);
    crusade.next_pid = nextPid;
    crusade.roster.push(pieces[0]);
    added.push(pieces[0].name);
  }
  return added.length > 0
    ? `Nuevas tropas se suman a la marcha: ${added.join(", ")}.`
    : "Las filas de tu reino ya están al máximo de su capacidad (16 unidades).";
}
