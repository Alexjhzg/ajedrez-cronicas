/**
 * Oráculo Umbrío: función de evaluación y búsqueda Negamax Alfa-Beta (8x8 y 12x12, 2 y 4 frentes).
 */

import {
  AMAZON,
  BISHOP,
  CAMEL,
  CENTAUR,
  ELEPHANT,
  FALCON,
  GRASSHOPPER,
  KING,
  KNIGHT,
  LION,
  NIGHTRIDER,
  PAWN,
  PHOENIX,
  PIECE_VALUE,
  QUEEN,
  ROOK,
  ZEBRA,
} from "./constants.js";

const PAWN_PST = [
  0, 0, 0, 0, 0, 0, 0, 0,
  50, 50, 50, 50, 50, 50, 50, 50,
  10, 10, 20, 30, 30, 20, 10, 10,
  5, 5, 10, 25, 25, 10, 5, 5,
  0, 0, 0, 20, 20, 0, 0, 0,
  5, -5, -10, 0, 0, -10, -5, 5,
  5, 10, 10, -20, -20, 10, 10, 5,
  0, 0, 0, 0, 0, 0, 0, 0,
];
const KNIGHT_PST = [
  -50, -40, -30, -30, -30, -30, -40, -50,
  -40, -20, 0, 0, 0, 0, -20, -40,
  -30, 0, 10, 15, 15, 10, 0, -30,
  -30, 5, 15, 20, 20, 15, 5, -30,
  -30, 0, 15, 20, 20, 15, 0, -30,
  -30, 5, 10, 15, 15, 10, 5, -30,
  -40, -20, 0, 5, 5, 0, -20, -40,
  -50, -40, -30, -30, -30, -30, -40, -50,
];
const BISHOP_PST = [
  -20, -10, -10, -10, -10, -10, -10, -20,
  -10, 0, 0, 0, 0, 0, 0, -10,
  -10, 0, 5, 10, 10, 5, 0, -10,
  -10, 5, 5, 10, 10, 5, 5, -10,
  -10, 0, 10, 10, 10, 10, 0, -10,
  -10, 10, 10, 10, 10, 10, 10, -10,
  -10, 5, 0, 0, 0, 0, 5, -10,
  -20, -10, -10, -10, -10, -10, -10, -20,
];
const ROOK_PST = [
  0, 0, 0, 0, 0, 0, 0, 0,
  5, 10, 10, 10, 10, 10, 10, 5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  0, 0, 0, 5, 5, 0, 0, 0,
];
const QUEEN_PST = [
  -20, -10, -10, -5, -5, -10, -10, -20,
  -10, 0, 0, 0, 0, 0, 0, -10,
  -10, 0, 5, 5, 5, 5, 0, -10,
  -5, 0, 5, 5, 5, 5, 0, -5,
  0, 0, 5, 5, 5, 5, 0, -5,
  -10, 5, 5, 5, 5, 5, 0, -10,
  -10, 0, 5, 0, 0, 0, 0, -10,
  -20, -10, -10, -5, -5, -10, -10, -20,
];
const KING_PST = [
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -20, -30, -30, -40, -40, -30, -30, -20,
  -10, -20, -20, -20, -20, -20, -20, -10,
  20, 20, 0, 0, 0, 0, 20, 20,
  20, 30, 10, 0, 0, 10, 30, 20,
];
const CENTER_FAIRY_PST = [
  -20, -10, -10, -10, -10, -10, -10, -20,
  -10, 0, 5, 5, 5, 5, 0, -10,
  -10, 5, 10, 15, 15, 10, 5, -10,
  -10, 5, 15, 22, 22, 15, 5, -10,
  -10, 5, 15, 22, 22, 15, 5, -10,
  -10, 5, 10, 15, 15, 10, 5, -10,
  -10, 0, 5, 5, 5, 5, 0, -10,
  -20, -10, -10, -10, -10, -10, -10, -20,
];
const PST = {
  [PAWN]: PAWN_PST,
  [KNIGHT]: KNIGHT_PST,
  [BISHOP]: BISHOP_PST,
  [ROOK]: ROOK_PST,
  [QUEEN]: QUEEN_PST,
  [KING]: KING_PST,
  [FALCON]: CENTER_FAIRY_PST,
  [ELEPHANT]: CENTER_FAIRY_PST,
  [AMAZON]: QUEEN_PST,
  [GRASSHOPPER]: CENTER_FAIRY_PST,
  [NIGHTRIDER]: KNIGHT_PST,
  [CENTAUR]: CENTER_FAIRY_PST,
  [CAMEL]: KNIGHT_PST,
  [LION]: CENTER_FAIRY_PST,
  [ZEBRA]: KNIGHT_PST,
  [PHOENIX]: CENTER_FAIRY_PST,
};

const MATE_SCORE = 100000;

function pstIndex(game, color, r, c) {
  const n = game.size;
  const sr = n === 8 ? r : Math.min(7, Math.floor((r * 7) / Math.max(1, n - 1)));
  const sc = n === 8 ? c : Math.min(7, Math.floor((c * 7) / Math.max(1, n - 1)));
  const [fdr, fdc] = game.pawnVector(color);
  if (fdr === -1) return sr * 8 + sc;
  if (fdr === 1) return (7 - sr) * 8 + sc;
  if (fdc === 1) return (7 - sc) * 8 + sr;
  return sc * 8 + sr;
}

export function evaluate(game, perspective = null) {
  const pov = perspective || game.turn;
  const n = game.size;
  let ownScore = 0;
  const enemyScores = {};
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const piece = game.grid[r][c];
      if (!piece) continue;
      const table = PST[piece.kind] || CENTER_FAIRY_PST;
      let bonus = piece.veteran ? 35 : 0;
      if (game.isFortified(r, c)) bonus += 25;
      const val =
        (PIECE_VALUE[piece.kind] || 300) +
        bonus +
        table[pstIndex(game, piece.color, r, c)];
      if (piece.color === pov) {
        ownScore += val;
      } else {
        enemyScores[piece.color] = (enemyScores[piece.color] || 0) + val;
      }
    }
  }
  const vals = Object.values(enemyScores);
  if (vals.length === 0) return ownScore;
  if (!game.multi_front) {
    return ownScore - vals.reduce((a, b) => a + b, 0);
  }
  const maxEnemy = Math.max(...vals);
  const avgEnemy = Math.floor(vals.reduce((a, b) => a + b, 0) / vals.length);
  return ownScore - Math.floor((maxEnemy + avgEnemy) / 2);
}

function orderMoves(game, moves) {
  return moves.slice().sort((a, b) => {
    const score = (m) => {
      let val = 0;
      const target = game.grid[m.tr][m.tc];
      if (target) {
        val +=
          10 * (PIECE_VALUE[target.kind] || 300) -
          (PIECE_VALUE[game.grid[m.fr][m.fc].kind] || 300);
      }
      if (m.is_en_passant) val += 1000;
      if (m.promotion) val += PIECE_VALUE[m.promotion] || 900;
      if (m.castle) val += 60;
      return val;
    };
    return score(b) - score(a);
  });
}

export function findBestMove(
  game,
  { depth = 2, randomness = 0.0, timeLimitMs = 1200 } = {}
) {
  const moves = game.legalMoves(game.turn);
  if (moves.length === 0) return null;

  const deadline = performance.now() + timeLimitMs;
  let nodes = 0;
  let timedOut = false;

  function negamax(state, d, alpha, beta, ply) {
    nodes += 1;
    if ((nodes & 255) === 0 && performance.now() > deadline) {
      timedOut = true;
      return 0;
    }
    if (d <= 0 && !state.inCheck(state.turn)) {
      return evaluate(state);
    }
    const legal = state.legalMoves(state.turn);
    if (legal.length === 0) {
      if (state.inCheck(state.turn)) return -(MATE_SCORE - ply);
      return 0;
    }
    if (d <= 0) return evaluate(state);

    let best = -MATE_SCORE * 2;
    for (const move of orderMoves(state, legal)) {
      const child = state.clone(true);
      const mover = child.turn;
      child.applyMove(move);
      const val = child.multi_front
        ? evaluate(child, mover)
        : -negamax(child, d - 1, -beta, -alpha, ply + 1);
      if (timedOut) return 0;
      if (val > best) best = val;
      if (val > alpha) alpha = val;
      if (alpha >= beta) break;
    }
    return best;
  }

  let scored = [];
  let bestScore = -MATE_SCORE * 2;
  const maxD =
    game.multi_front || game.size > 8
      ? Math.min(2, Math.max(1, depth))
      : Math.max(1, depth);

  for (let d = 1; d <= maxD; d++) {
    timedOut = false;
    const currentScored = [];
    let currentBest = -MATE_SCORE * 2;
    const ordered =
      scored.length > 0 ? scored.map((item) => item[1]) : orderMoves(game, moves);

    for (const move of ordered) {
      const child = game.clone(true);
      const mover = child.turn;
      child.applyMove(move);
      let val = 0;
      if (child.multi_front) {
        const nextMoves = child.legalMoves(child.turn).slice(0, 8);
        if (nextMoves.length > 0) {
          let worstReply = Infinity;
          for (const nm of nextMoves) {
            const g2 = child.clone(true);
            g2.applyMove(nm);
            const s = evaluate(g2, mover);
            if (s < worstReply) worstReply = s;
          }
          val = worstReply + (move.captured ? 120 : 0);
        } else {
          val = evaluate(child, mover);
        }
      } else {
        val = -negamax(child, d - 1, -MATE_SCORE * 2, MATE_SCORE * 2, 1);
      }
      if (timedOut) break;
      currentScored.push([val, move]);
      if (val > currentBest) currentBest = val;
    }

    if (currentScored.length > 0 && (!timedOut || scored.length === 0)) {
      currentScored.sort((a, b) => b[0] - a[0]);
      scored = currentScored;
      bestScore = currentBest;
    }
    if (timedOut) break;
  }

  if (scored.length === 0) return moves[0];
  scored.sort((a, b) => b[0] - a[0]);
  if (bestScore < -MATE_SCORE) bestScore = scored[0][0];

  if (randomness > 0 && Math.random() < randomness) {
    const margin = depth <= 1 ? 90 : 45;
    const nearBest = scored
      .filter(([s]) => s >= bestScore - margin)
      .map(([, m]) => m);
    const pool = nearBest.length > 0 ? nearBest : [scored[0][1]];
    return pool[Math.floor(Math.random() * pool.length)];
  }
  const top = scored.filter(([s]) => s === bestScore).map(([, m]) => m);
  const pool = top.length > 0 ? top : [scored[0][1]];
  return pool[Math.floor(Math.random() * pool.length)];
}
