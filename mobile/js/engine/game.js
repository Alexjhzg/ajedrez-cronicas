/**
 * Estado y reglas completas de una partida (tableros 8x8 y 12x12, 2 o 4 frentes).
 */

import {
  ALFIL_DELTAS,
  ALL_COLORS,
  AMAZON,
  BISHOP,
  BISHOP_DIRS,
  BLACK,
  CAMEL,
  CAMEL_DELTAS,
  CENTAUR,
  ELEPHANT,
  FALCON,
  FORTIFIED_TERRAIN,
  GRASSHOPPER,
  GREEN,
  IMPASSABLE_TERRAIN,
  KING,
  KING_DELTAS,
  KNIGHT,
  KNIGHT_DELTAS,
  LION,
  NIGHTRIDER,
  PAWN,
  PHOENIX,
  QUEEN,
  QUEEN_DIRS,
  RED,
  ROOK,
  ROOK_DIRS,
  SLOW_TERRAIN,
  VISION_BLOCKING_TERRAIN,
  WHITE,
  ZEBRA,
  ZEBRA_DELTAS,
} from "./constants.js";
import { createMove, createPiece } from "./model.js";

const KNIGHT_COMPOUNDS = [KNIGHT, FALCON, ELEPHANT, AMAZON, CENTAUR];
const BISHOP_SLIDERS = [BISHOP, QUEEN, FALCON, AMAZON];
const ROOK_SLIDERS = [ROOK, QUEEN, ELEPHANT, AMAZON];

export class Game {
  constructor(turnOrder = [WHITE, BLACK], frontDirs = null, size = 8) {
    this.size = size;
    this.grid = Array.from({ length: size }, () => Array(size).fill(null));
    this.terrain = new Map();
    this.turn_order = [...turnOrder];
    this.turn = this.turn_order[0];
    this.eliminated = new Set();

    if (frontDirs) {
      this.front_dirs = { ...frontDirs };
    } else {
      this.front_dirs = {
        [WHITE]: [-1, 0],
        [BLACK]: [1, 0],
        [RED]: [0, 1],
        [GREEN]: [0, -1],
      };
      if (this.turn_order.length === 2) {
        this.front_dirs[this.turn_order[0]] = [-1, 0];
        this.front_dirs[this.turn_order[1]] = [1, 0];
      }
    }

    this.castling = {};
    for (const c of ALL_COLORS) {
      this.castling[c] = { K: false, Q: false };
    }
    this.ep = null;
    this.halfmove = 0;
    this.fullmove = 1;
    this.history = [];
    this.last_move = null;
  }

  get multi_front() {
    return this.turn_order.length > 2;
  }

  activeColors() {
    return this.turn_order.filter((c) => !this.eliminated.has(c));
  }

  enemyColors(color) {
    return this.turn_order.filter((c) => c !== color && !this.eliminated.has(c));
  }

  nextActiveColor(current = null) {
    const cur = current || this.turn;
    const active = this.activeColors();
    if (active.length === 0) return cur;
    const idx = this.turn_order.indexOf(cur);
    if (idx === -1) return active[0];
    for (let offset = 1; offset <= this.turn_order.length; offset++) {
      const candidate = this.turn_order[(idx + offset) % this.turn_order.length];
      if (!this.eliminated.has(candidate)) {
        return candidate;
      }
    }
    return active[0];
  }

  pawnVector(color) {
    return this.front_dirs[color] || (color === WHITE ? [-1, 0] : [1, 0]);
  }

  _key(r, c) {
    return `${r},${c}`;
  }

  place(piece, r, c) {
    this.grid[r][c] = piece;
  }

  pieceAt(r, c) {
    const n = this.size;
    if (r >= 0 && r < n && c >= 0 && c < n) {
      return this.grid[r][c];
    }
    return null;
  }

  terrainAt(r, c) {
    return this.terrain.get(this._key(r, c)) || null;
  }

  isBlocked(r, c) {
    const t = this.terrainAt(r, c);
    return t !== null && IMPASSABLE_TERRAIN.has(t);
  }

  isVisionBlocked(r, c) {
    const t = this.terrainAt(r, c);
    return t !== null && VISION_BLOCKING_TERRAIN.has(t);
  }

  isFortified(r, c) {
    const t = this.terrainAt(r, c);
    return t !== null && FORTIFIED_TERRAIN.has(t);
  }

  isSlow(r, c) {
    const t = this.terrainAt(r, c);
    return t !== null && SLOW_TERRAIN.has(t);
  }

  addTerrain(kind, r, c) {
    const n = this.size;
    if (r < 0 || r >= n || c < 0 || c >= n) return false;
    const key = this._key(r, c);
    if (this.terrain.has(key)) return false;
    if (IMPASSABLE_TERRAIN.has(kind) && this.grid[r][c] !== null) return false;
    this.terrain.set(key, kind);
    if (
      IMPASSABLE_TERRAIN.has(kind) &&
      this.ep &&
      this.ep[0] === r &&
      this.ep[1] === c
    ) {
      this.ep = null;
    }
    return true;
  }

  clone(search = false) {
    const g = new Game(this.turn_order, this.front_dirs, this.size);
    for (let r = 0; r < this.size; r++) {
      g.grid[r] = this.grid[r].slice();
    }
    g.terrain = new Map(this.terrain);
    g.turn = this.turn;
    g.eliminated = new Set(this.eliminated);
    for (const c of Object.keys(this.castling)) {
      g.castling[c] = { ...this.castling[c] };
    }
    g.ep = this.ep ? [...this.ep] : null;
    g.halfmove = this.halfmove;
    g.fullmove = this.fullmove;
    if (!search) {
      g.history = this.history.slice();
      g.last_move = this.last_move;
    }
    return g;
  }

  findKing(color) {
    const n = this.size;
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const p = this.grid[r][c];
        if (p && p.color === color && p.kind === KING) {
          return [r, c];
        }
      }
    }
    return null;
  }

  capturedPieces() {
    return this.history.filter((m) => m.captured).map((m) => m.captured);
  }

  isAttacked(r, c, byColor) {
    const n = this.size;
    const fortified = this.isFortified(r, c);
    const [fdr, fdc] = this.pawnVector(byColor);

    if (fdr !== 0) {
      const pawnRow = r - fdr;
      for (const dc of [-1, 1]) {
        const pc = c + dc;
        if (pawnRow >= 0 && pawnRow < n && pc >= 0 && pc < n) {
          const p = this.grid[pawnRow][pc];
          if (p && p.color === byColor && p.kind === PAWN) return true;
        }
      }
      if (pawnRow >= 0 && pawnRow < n) {
        const p = this.grid[pawnRow][c];
        if (p && p.color === byColor && p.kind === PAWN && p.veteran) {
          return true;
        }
      }
    } else {
      const pawnCol = c - fdc;
      for (const dr of [-1, 1]) {
        const pr = r + dr;
        if (pr >= 0 && pr < n && pawnCol >= 0 && pawnCol < n) {
          const p = this.grid[pr][pawnCol];
          if (p && p.color === byColor && p.kind === PAWN) return true;
        }
      }
      if (pawnCol >= 0 && pawnCol < n) {
        const p = this.grid[r][pawnCol];
        if (p && p.color === byColor && p.kind === PAWN && p.veteran) {
          return true;
        }
      }
    }

    if (!fortified) {
      for (const [dr, dc] of KNIGHT_DELTAS) {
        const rr = r + dr;
        const cc = c + dc;
        if (rr >= 0 && rr < n && cc >= 0 && cc < n) {
          const p = this.grid[rr][cc];
          if (
            p &&
            p.color === byColor &&
            (KNIGHT_COMPOUNDS.includes(p.kind) ||
              (p.kind === QUEEN && p.veteran))
          ) {
            return true;
          }
        }
      }

      for (const [dr, dc] of KNIGHT_DELTAS) {
        let rr = r + dr;
        let cc = c + dc;
        while (rr >= 0 && rr < n && cc >= 0 && cc < n) {
          if (this.isBlocked(rr, cc)) break;
          const p = this.grid[rr][cc];
          if (p !== null) {
            if (p.color === byColor && p.kind === NIGHTRIDER) return true;
            break;
          }
          if (this.isVisionBlocked(rr, cc) || this.isSlow(rr, cc)) break;
          rr += dr;
          cc += dc;
        }
      }

      for (const [dr, dc] of ALFIL_DELTAS) {
        const rr = r + dr;
        const cc = c + dc;
        if (rr >= 0 && rr < n && cc >= 0 && cc < n) {
          const p = this.grid[rr][cc];
          if (p && p.color === byColor && p.kind === PHOENIX) return true;
        }
      }

      for (const [dr, dc] of CAMEL_DELTAS) {
        const rr = r + dr;
        const cc = c + dc;
        if (rr >= 0 && rr < n && cc >= 0 && cc < n) {
          const p = this.grid[rr][cc];
          if (p && p.color === byColor && p.kind === CAMEL) return true;
        }
      }

      for (const [dr, dc] of ZEBRA_DELTAS) {
        const rr = r + dr;
        const cc = c + dc;
        if (rr >= 0 && rr < n && cc >= 0 && cc < n) {
          const p = this.grid[rr][cc];
          if (p && p.color === byColor && p.kind === ZEBRA) return true;
        }
      }
    }

    for (const [dr, dc] of KING_DELTAS) {
      const rr = r + dr;
      const cc = c + dc;
      if (rr >= 0 && rr < n && cc >= 0 && cc < n) {
        const p = this.grid[rr][cc];
        if (!p || p.color !== byColor) continue;
        if (p.kind === KING || p.kind === CENTAUR) return true;
        const ortho = Math.abs(dr) + Math.abs(dc) === 1;
        const diag = Math.abs(dr) === 1 && Math.abs(dc) === 1;
        if (p.kind === PHOENIX && (ortho || p.veteran)) return true;
        if (p.veteran) {
          if (p.kind === PAWN && dr === -fdr && dc === -fdc) return true;
          if (
            [KNIGHT, BISHOP, CAMEL, ZEBRA, NIGHTRIDER, GRASSHOPPER].includes(
              p.kind
            ) &&
            ortho
          ) {
            return true;
          }
          if (p.kind === ROOK && diag) return true;
        }
      }
    }

    const slideSpecs = [
      [BISHOP_DIRS, BISHOP_SLIDERS],
      [ROOK_DIRS, ROOK_SLIDERS],
    ];
    for (const [dirs, kinds] of slideSpecs) {
      for (const [dr, dc] of dirs) {
        let rr = r + dr;
        let cc = c + dc;
        let steps = 1;
        while (rr >= 0 && rr < n && cc >= 0 && cc < n) {
          if (this.isBlocked(rr, cc)) break;
          const p = this.grid[rr][cc];
          if (p !== null) {
            if (p.color === byColor && kinds.includes(p.kind)) {
              if (!(fortified && steps > 1)) {
                if (!(this.isSlow(rr, cc) && steps > 2)) {
                  return true;
                }
              }
            }
            break;
          }
          if (this.isVisionBlocked(rr, cc) || this.isSlow(rr, cc)) break;
          rr += dr;
          cc += dc;
          steps += 1;
        }
      }
    }

    if (!fortified) {
      for (const [dr, dc] of QUEEN_DIRS) {
        let rr = r + dr;
        let cc = c + dc;
        let hurdleFound = false;
        let distFromTarget = 1;
        while (rr >= 0 && rr < n && cc >= 0 && cc < n) {
          if (this.isBlocked(rr, cc)) break;
          const p = this.grid[rr][cc];
          if (!hurdleFound) {
            if (p !== null) {
              hurdleFound = true;
            }
          } else {
            if (p !== null) {
              if (p.color === byColor) {
                if (p.kind === LION) return true;
                if (p.kind === GRASSHOPPER && distFromTarget === 2) {
                  return true;
                }
              }
              break;
            }
          }
          rr += dr;
          cc += dc;
          distFromTarget += 1;
        }
      }
    }

    return false;
  }

  isThreatened(r, c, defenderColor) {
    return this.enemyColors(defenderColor).some((enemy) =>
      this.isAttacked(r, c, enemy)
    );
  }

  inCheck(color) {
    const king = this.findKing(color);
    if (!king) return false;
    return this.isThreatened(king[0], king[1], color);
  }

  pseudoMoves(color = null) {
    const side = color || this.turn;
    const n = this.size;
    const moves = [];
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const piece = this.grid[r][c];
        if (!piece || piece.color !== side) continue;
        const kind = piece.kind;
        if (kind === PAWN) {
          this._pawnMoves(r, c, piece, moves);
        } else if (kind === KNIGHT) {
          const deltas = piece.veteran
            ? [...KNIGHT_DELTAS, ...ROOK_DIRS]
            : KNIGHT_DELTAS;
          this._stepMoves(r, c, piece, moves, deltas);
        } else if (kind === BISHOP) {
          this._slideMoves(r, c, piece, moves, BISHOP_DIRS);
          if (piece.veteran) this._stepMoves(r, c, piece, moves, ROOK_DIRS);
        } else if (kind === ROOK) {
          this._slideMoves(r, c, piece, moves, ROOK_DIRS);
          if (piece.veteran) this._stepMoves(r, c, piece, moves, BISHOP_DIRS);
        } else if (kind === QUEEN) {
          this._slideMoves(r, c, piece, moves, QUEEN_DIRS);
          if (piece.veteran) this._stepMoves(r, c, piece, moves, KNIGHT_DELTAS);
        } else if (kind === KING) {
          this._stepMoves(r, c, piece, moves, KING_DELTAS);
          if (!this.multi_front) {
            this._castleMoves(r, c, piece, moves);
          }
        } else if (kind === FALCON) {
          this._slideMoves(r, c, piece, moves, BISHOP_DIRS);
          const deltas = piece.veteran
            ? [...KNIGHT_DELTAS, ...ROOK_DIRS]
            : KNIGHT_DELTAS;
          this._stepMoves(r, c, piece, moves, deltas);
        } else if (kind === ELEPHANT) {
          this._slideMoves(r, c, piece, moves, ROOK_DIRS);
          const deltas = piece.veteran
            ? [...KNIGHT_DELTAS, ...BISHOP_DIRS]
            : KNIGHT_DELTAS;
          this._stepMoves(r, c, piece, moves, deltas);
        } else if (kind === AMAZON) {
          this._slideMoves(r, c, piece, moves, QUEEN_DIRS);
          const deltas = piece.veteran
            ? [...KNIGHT_DELTAS, ...ALFIL_DELTAS]
            : KNIGHT_DELTAS;
          this._stepMoves(r, c, piece, moves, deltas);
        } else if (kind === GRASSHOPPER) {
          this._grasshopperMoves(r, c, piece, moves);
          if (piece.veteran) this._stepMoves(r, c, piece, moves, ROOK_DIRS);
        } else if (kind === NIGHTRIDER) {
          this._nightriderMoves(r, c, piece, moves);
          if (piece.veteran) this._stepMoves(r, c, piece, moves, ROOK_DIRS);
        } else if (kind === CENTAUR) {
          const deltas = piece.veteran
            ? [...KING_DELTAS, ...KNIGHT_DELTAS, ...ALFIL_DELTAS]
            : [...KING_DELTAS, ...KNIGHT_DELTAS];
          this._stepMoves(r, c, piece, moves, deltas);
        } else if (kind === CAMEL) {
          const deltas = piece.veteran
            ? [...CAMEL_DELTAS, ...ROOK_DIRS]
            : CAMEL_DELTAS;
          this._stepMoves(r, c, piece, moves, deltas);
        } else if (kind === LION) {
          this._lionMoves(r, c, piece, moves);
          if (piece.veteran) this._stepMoves(r, c, piece, moves, KING_DELTAS);
        } else if (kind === ZEBRA) {
          const deltas = piece.veteran
            ? [...ZEBRA_DELTAS, ...ROOK_DIRS]
            : ZEBRA_DELTAS;
          this._stepMoves(r, c, piece, moves, deltas);
        } else if (kind === PHOENIX) {
          const deltas = piece.veteran
            ? [...ROOK_DIRS, ...ALFIL_DELTAS, ...BISHOP_DIRS]
            : [...ROOK_DIRS, ...ALFIL_DELTAS];
          this._stepMoves(r, c, piece, moves, deltas);
        }
      }
    }
    return moves;
  }

  _pawnMoves(r, c, piece, out) {
    const n = this.size;
    const [fdr, fdc] = this.pawnVector(piece.color);
    const nr = r + fdr;
    const ncFwd = c + fdc;
    if (nr < 0 || nr >= n || ncFwd < 0 || ncFwd >= n) return;

    let startLine = false;
    let isPromo = false;
    let sideDeltas = [];
    if (fdr !== 0) {
      startLine =
        fdr === -1 ? r === n - 2 || r === n - 3 : r === 1 || r === 2;
      isPromo = nr === (fdr === -1 ? 0 : n - 1);
      sideDeltas = [
        [0, -1],
        [0, 1],
      ];
    } else {
      startLine =
        fdc === 1 ? c === 1 || c === 2 : c === n - 2 || c === n - 3;
      isPromo = ncFwd === (fdc === 1 ? n - 1 : 0);
      sideDeltas = [
        [-1, 0],
        [1, 0],
      ];
    }

    const promoOptions =
      n >= 12
        ? [AMAZON, QUEEN, ELEPHANT, FALCON, ROOK, KNIGHT]
        : [QUEEN, ELEPHANT, FALCON, ROOK, BISHOP, KNIGHT];

    const addPawnMove = (tr, tc, ep = false) => {
      if (isPromo) {
        for (const promo of promoOptions) {
          out.push(createMove(r, c, tr, tc, { promotion: promo }));
        }
      } else {
        out.push(createMove(r, c, tr, tc, { is_en_passant: ep }));
      }
    };

    if (!this.isBlocked(nr, ncFwd) && this.grid[nr][ncFwd] === null) {
      addPawnMove(nr, ncFwd);
      if (!isPromo && startLine) {
        const r2 = r + 2 * fdr;
        const c2 = c + 2 * fdc;
        if (
          r2 >= 0 &&
          r2 < n &&
          c2 >= 0 &&
          c2 < n &&
          !this.isSlow(r, c) &&
          !this.isSlow(nr, ncFwd) &&
          !this.isBlocked(r2, c2) &&
          this.grid[r2][c2] === null
        ) {
          out.push(createMove(r, c, r2, c2));
        }
      }
    } else if (
      piece.veteran &&
      !this.isBlocked(nr, ncFwd) &&
      this.grid[nr][ncFwd] !== null &&
      this.grid[nr][ncFwd].color !== piece.color
    ) {
      addPawnMove(nr, ncFwd);
    }

    if (piece.veteran) {
      for (const [sdr, sdc] of sideDeltas) {
        const sr = r + sdr;
        const sc = c + sdc;
        if (
          sr >= 0 &&
          sr < n &&
          sc >= 0 &&
          sc < n &&
          !this.isBlocked(sr, sc) &&
          this.grid[sr][sc] === null
        ) {
          out.push(createMove(r, c, sr, sc));
        }
      }
    }

    for (const [sdr, sdc] of sideDeltas) {
      const cr = nr + sdr;
      const cc = ncFwd + sdc;
      if (cr < 0 || cr >= n || cc < 0 || cc >= n || this.isBlocked(cr, cc)) {
        continue;
      }
      const target = this.grid[cr][cc];
      if (target !== null && target.color !== piece.color) {
        addPawnMove(cr, cc);
      } else if (
        target === null &&
        !this.multi_front &&
        this.ep &&
        this.ep[0] === cr &&
        this.ep[1] === cc
      ) {
        addPawnMove(cr, cc, true);
      }
    }
  }

  _stepMoves(r, c, piece, out, deltas) {
    const n = this.size;
    for (const [dr, dc] of deltas) {
      const rr = r + dr;
      const cc = c + dc;
      if (rr < 0 || rr >= n || cc < 0 || cc >= n) continue;
      if (this.isBlocked(rr, cc)) continue;
      const target = this.grid[rr][cc];
      if (target === null) {
        out.push(createMove(r, c, rr, cc));
      } else if (target.color !== piece.color) {
        const dist = Math.max(Math.abs(dr), Math.abs(dc));
        if (this.isFortified(rr, cc) && dist > 1) continue;
        out.push(createMove(r, c, rr, cc));
      }
    }
  }

  _slideMoves(r, c, piece, out, directions) {
    const n = this.size;
    const maxSteps = this.isSlow(r, c) ? 2 : n;
    for (const [dr, dc] of directions) {
      let rr = r + dr;
      let cc = c + dc;
      let steps = 1;
      while (rr >= 0 && rr < n && cc >= 0 && cc < n && steps <= maxSteps) {
        if (this.isBlocked(rr, cc)) break;
        const target = this.grid[rr][cc];
        if (target === null) {
          out.push(createMove(r, c, rr, cc));
          if (this.isVisionBlocked(rr, cc) || this.isSlow(rr, cc)) break;
        } else {
          if (target.color !== piece.color) {
            if (!(this.isFortified(rr, cc) && steps > 1)) {
              out.push(createMove(r, c, rr, cc));
            }
          }
          break;
        }
        rr += dr;
        cc += dc;
        steps += 1;
      }
    }
  }

  _nightriderMoves(r, c, piece, out) {
    const n = this.size;
    const maxLeaps = this.isSlow(r, c) ? 1 : n;
    for (const [dr, dc] of KNIGHT_DELTAS) {
      let rr = r + dr;
      let cc = c + dc;
      let leaps = 1;
      while (rr >= 0 && rr < n && cc >= 0 && cc < n && leaps <= maxLeaps) {
        if (this.isBlocked(rr, cc)) break;
        const target = this.grid[rr][cc];
        if (target === null) {
          out.push(createMove(r, c, rr, cc));
          if (this.isVisionBlocked(rr, cc) || this.isSlow(rr, cc)) break;
        } else {
          if (target.color !== piece.color && !this.isFortified(rr, cc)) {
            out.push(createMove(r, c, rr, cc));
          }
          break;
        }
        rr += dr;
        cc += dc;
        leaps += 1;
      }
    }
  }

  _grasshopperMoves(r, c, piece, out) {
    const n = this.size;
    for (const [dr, dc] of QUEEN_DIRS) {
      let rr = r + dr;
      let cc = c + dc;
      while (rr >= 0 && rr < n && cc >= 0 && cc < n) {
        if (this.isBlocked(rr, cc)) break;
        if (this.grid[rr][cc] !== null) {
          const lr = rr + dr;
          const lc = cc + dc;
          if (lr >= 0 && lr < n && lc >= 0 && lc < n && !this.isBlocked(lr, lc)) {
            const target = this.grid[lr][lc];
            if (target === null) {
              out.push(createMove(r, c, lr, lc));
            } else if (
              target.color !== piece.color &&
              !this.isFortified(lr, lc)
            ) {
              out.push(createMove(r, c, lr, lc));
            }
          }
          break;
        }
        if (this.isVisionBlocked(rr, cc)) break;
        rr += dr;
        cc += dc;
      }
    }
  }

  _lionMoves(r, c, piece, out) {
    const n = this.size;
    for (const [dr, dc] of QUEEN_DIRS) {
      let rr = r + dr;
      let cc = c + dc;
      let hurdleFound = false;
      while (rr >= 0 && rr < n && cc >= 0 && cc < n) {
        if (this.isBlocked(rr, cc)) break;
        const p = this.grid[rr][cc];
        if (!hurdleFound) {
          if (p !== null) {
            hurdleFound = true;
          } else if (this.isVisionBlocked(rr, cc)) {
            break;
          }
        } else {
          if (p === null) {
            out.push(createMove(r, c, rr, cc));
            if (this.isVisionBlocked(rr, cc) || this.isSlow(rr, cc)) break;
          } else {
            if (p.color !== piece.color && !this.isFortified(rr, cc)) {
              out.push(createMove(r, c, rr, cc));
            }
            break;
          }
        }
        rr += dr;
        cc += dc;
      }
    }
  }

  _castleMoves(r, c, piece, out) {
    if (piece.kind !== KING || this.size !== 8) return;
    const [fdr] = this.pawnVector(piece.color);
    const homeRow = fdr === -1 ? 7 : 0;
    if (r !== homeRow || c !== 4) return;
    const rights = this.castling[piece.color] || { K: false, Q: false };

    if (rights.K) {
      const corner = this.grid[homeRow][7];
      if (
        corner &&
        corner.kind === ROOK &&
        corner.color === piece.color &&
        this.grid[homeRow][5] === null &&
        this.grid[homeRow][6] === null &&
        !this.isBlocked(homeRow, 5) &&
        !this.isBlocked(homeRow, 6) &&
        ![4, 5, 6].some((col) => this.isThreatened(homeRow, col, piece.color))
      ) {
        out.push(createMove(r, c, homeRow, 6, { castle: "K" }));
      }
    }

    if (rights.Q) {
      const corner = this.grid[homeRow][0];
      if (
        corner &&
        corner.kind === ROOK &&
        corner.color === piece.color &&
        this.grid[homeRow][1] === null &&
        this.grid[homeRow][2] === null &&
        this.grid[homeRow][3] === null &&
        ![1, 2, 3].some((col) => this.isBlocked(homeRow, col)) &&
        ![4, 3, 2].some((col) => this.isThreatened(homeRow, col, piece.color))
      ) {
        out.push(createMove(r, c, homeRow, 2, { castle: "Q" }));
      }
    }
  }

  legalMoves(color = null) {
    const side = color || this.turn;
    if (this.eliminated.has(side)) return [];
    const legal = [];
    for (const move of this.pseudoMoves(side)) {
      if (this._leavesKingSafe(move, side)) {
        legal.push(move);
      }
    }
    return legal;
  }

  _leavesKingSafe(move, color) {
    const gridBackup = this.grid.map((row) => row.slice());
    const castlingBackup = {};
    for (const c of Object.keys(this.castling)) {
      castlingBackup[c] = { ...this.castling[c] };
    }
    const epBackup = this.ep ? [...this.ep] : null;
    const halfBackup = this.halfmove;
    this._movePieces(move);
    const safe = !this.inCheck(color);
    this.grid = gridBackup;
    this.castling = castlingBackup;
    this.ep = epBackup;
    this.halfmove = halfBackup;
    return safe;
  }

  legalMovesFrom(r, c) {
    return this.legalMoves(this.turn).filter((m) => m.fr === r && m.fc === c);
  }

  visibleSquares(color) {
    const n = this.size;
    const visible = new Set();
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const piece = this.grid[r][c];
        if (piece && piece.color === color) {
          visible.add(this._key(r, c));
          for (const [dr, dc] of KING_DELTAS) {
            const rr = r + dr;
            const cc = c + dc;
            if (rr >= 0 && rr < n && cc >= 0 && cc < n) {
              visible.add(this._key(rr, cc));
            }
          }
        }
      }
    }

    for (const move of this.pseudoMoves(color)) {
      visible.add(this._key(move.tr, move.tc));
    }

    const king = this.findKing(color);
    if (king && this.inCheck(color)) {
      for (const enemy of this.enemyColors(color)) {
        for (const move of this.pseudoMoves(enemy)) {
          if (move.tr === king[0] && move.tc === king[1]) {
            visible.add(this._key(move.fr, move.fc));
          }
        }
      }
    }
    return visible;
  }

  _movePieces(move) {
    const n = this.size;
    const piece = this.grid[move.fr][move.fc];
    let captured = this.grid[move.tr][move.tc];
    let placed = null;

    if (move.is_en_passant) {
      const [fdr] = this.pawnVector(piece.color);
      const capRow = move.tr - fdr;
      captured = this.grid[capRow][move.tc];
      this.grid[capRow][move.tc] = null;
    }

    this.grid[move.fr][move.fc] = null;
    const kills = piece.kills + (captured !== null ? 1 : 0);
    const veteran = piece.veteran || (kills >= 2 && piece.kind !== KING);

    if (move.promotion) {
      placed = createPiece(
        piece.color,
        move.promotion,
        piece.pid,
        piece.name,
        piece.title,
        kills,
        veteran
      );
      this.grid[move.tr][move.tc] = placed;
    } else if (kills !== piece.kills || veteran !== piece.veteran) {
      placed = createPiece(
        piece.color,
        piece.kind,
        piece.pid,
        piece.name,
        piece.title,
        kills,
        veteran
      );
      this.grid[move.tr][move.tc] = placed;
    } else {
      this.grid[move.tr][move.tc] = piece;
    }

    if (move.castle && n === 8) {
      const row = move.tr;
      const [rookFrom, rookTo] = move.castle === "K" ? [7, 5] : [0, 3];
      const rook = this.grid[row][rookFrom];
      this.grid[row][rookFrom] = null;
      this.grid[row][rookTo] = rook;
    }

    if (this.castling[piece.color]) {
      if (piece.kind === KING) {
        this.castling[piece.color].K = false;
        this.castling[piece.color].Q = false;
      } else if (piece.kind === ROOK) {
        if (move.fc === 0) this.castling[piece.color].Q = false;
        if (move.fc === n - 1) this.castling[piece.color].K = false;
      }
    }

    if (captured && captured.kind === ROOK && this.castling[captured.color]) {
      const opp = captured.color;
      if (move.tr === 0 || move.tr === n - 1) {
        if (move.tc === 0) this.castling[opp].Q = false;
        if (move.tc === n - 1) this.castling[opp].K = false;
      }
    }

    this.ep = null;
    if (
      piece.kind === PAWN &&
      Math.abs(move.tr - move.fr) === 2 &&
      !this.multi_front
    ) {
      this.ep = [(move.fr + move.tr) >> 1, move.fc];
    }

    if (piece.kind === PAWN || captured !== null) {
      this.halfmove = 0;
    } else {
      this.halfmove += 1;
    }

    move.moved = piece;
    move.captured = captured;
    move.placed = placed;
    return [piece, captured, placed];
  }

  _eliminateFaction(color) {
    const n = this.size;
    this.eliminated.add(color);
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const p = this.grid[r][c];
        if (p && p.color === color) {
          this.grid[r][c] = null;
        }
      }
    }
  }

  applyMove(move) {
    const moverColor = this.turn;
    this._movePieces(move);
    const eliminatedNow = [];

    if (this.multi_front) {
      for (const c of [...this.activeColors()]) {
        if (c !== moverColor && !this.findKing(c)) {
          this._eliminateFaction(c);
          eliminatedNow.push(c);
        }
      }
      let nextC = this.nextActiveColor(moverColor);
      while (
        this.activeColors().length > 1 &&
        this.legalMoves(nextC).length === 0
      ) {
        this._eliminateFaction(nextC);
        eliminatedNow.push(nextC);
        nextC = this.nextActiveColor(moverColor);
      }
      this.turn = nextC;
    } else {
      this.turn = this.nextActiveColor(moverColor);
    }

    move.eliminated_factions = eliminatedNow;
    if (this.turn === this.turn_order[0]) {
      this.fullmove += 1;
    }
    this.last_move = move;
    this.history.push(move);
    return move;
  }

  insufficientMaterial() {
    if (this.multi_front) return false;
    const n = this.size;
    const minors = [];
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const p = this.grid[r][c];
        if (!p) continue;
        if (
          [
            PAWN,
            ROOK,
            QUEEN,
            FALCON,
            ELEPHANT,
            AMAZON,
            CENTAUR,
            LION,
            NIGHTRIDER,
          ].includes(p.kind)
        ) {
          return false;
        }
        if ([BISHOP, KNIGHT, CAMEL, ZEBRA, PHOENIX, GRASSHOPPER].includes(p.kind)) {
          minors.push(p);
        }
      }
    }
    if (minors.length <= 1) return true;
    return false;
  }

  result() {
    if (this.multi_front) {
      const active = this.activeColors();
      if (active.length === 1) {
        return { type: "checkmate", winner: active[0] };
      }
      if (this.eliminated.has(this.turn_order[0])) {
        const lastMover =
          this.last_move && this.last_move.moved
            ? this.last_move.moved.color
            : active[0];
        return { type: "checkmate", winner: lastMover };
      }
      if (this.halfmove >= 120) {
        return { type: "fifty", winner: null };
      }
      return null;
    }

    const moves = this.legalMoves(this.turn);
    if (moves.length === 0) {
      if (this.inCheck(this.turn)) {
        return { type: "checkmate", winner: this.nextActiveColor(this.turn) };
      }
      return { type: "stalemate", winner: null };
    }
    if (this.halfmove >= 100) {
      return { type: "fifty", winner: null };
    }
    if (this.insufficientMaterial()) {
      return { type: "material", winner: null };
    }
    return null;
  }
}
