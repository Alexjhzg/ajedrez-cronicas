/**
 * Renderizador de Tablero Táctil de Alta Densidad (HTML5 Canvas 2D + 60 FPS)
 * Port visual fiel de cronicas/ui/board.py, pieces.py, theme.py y animations.py
 */

import {
  AMAZON,
  BISHOP,
  BLACK,
  CAMEL,
  CENTAUR,
  ELEPHANT,
  FALCON,
  FILE_LETTERS,
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
} from "./engine.js";

export const PIECE_GLYPHS = {
  [KING]: "♚",
  [QUEEN]: "♛",
  [ROOK]: "♜",
  [BISHOP]: "♝",
  [KNIGHT]: "♞",
  [PAWN]: "♟",
  [FALCON]: "✦",
  [ELEPHANT]: "⛨",
  [AMAZON]: "♕",
  [GRASSHOPPER]: "☥",
  [NIGHTRIDER]: "♘",
  [CENTAUR]: "⛉",
  [CAMEL]: "◈",
  [LION]: "⚜",
  [ZEBRA]: "❖",
  [PHOENIX]: "❂",
};

export const SCENE_PALETTES = {
  classic: {
    light: "#b79a6f",
    dark: "#4d3346",
    frame: "#1d1527",
    edge: "#4b3560",
    coord: "#8b744a",
    coord_dim: "#5b4967",
  },
  imperial: {
    light: "#cbb07e",
    dark: "#432b3e",
    frame: "#1a1124",
    edge: "#7d6038",
    coord: "#c8a35f",
    coord_dim: "#6c567a",
  },
  bosque: {
    light: "#a8b58a",
    dark: "#405442",
    frame: "#172019",
    edge: "#617a52",
    coord: "#a3b47d",
    coord_dim: "#64745c",
  },
  rio: {
    light: "#aeb8b3",
    dark: "#465760",
    frame: "#172026",
    edge: "#63808c",
    coord: "#9fb7bd",
    coord_dim: "#5c7178",
  },
  acantilado: {
    light: "#c1a486",
    dark: "#5b4140",
    frame: "#24181a",
    edge: "#8a6657",
    coord: "#c0a489",
    coord_dim: "#76605a",
  },
  ruinas: {
    light: "#b6a990",
    dark: "#514355",
    frame: "#221b28",
    edge: "#786782",
    coord: "#b1a3bf",
    coord_dim: "#6d6074",
  },
  paso: {
    light: "#bda88b",
    dark: "#514c4a",
    frame: "#1f1d1c",
    edge: "#7d7367",
    coord: "#b6aa95",
    coord_dim: "#706a62",
  },
};

export const TERRAIN_STYLE = {
  bosque: { base: "#2b462c", edge: "#8ab46a", detail: "#527f46", deep: "#1c3020" },
  rio: { base: "#2a5368", edge: "#79b4cc", detail: "#46819a", deep: "#1c3948" },
  acantilado: { base: "#5a4b45", edge: "#b09378", detail: "#7c6657", deep: "#3a302c" },
  penasco: { base: "#514d48", edge: "#a79c89", detail: "#736b5f", deep: "#36332f" },
  ruinas: { base: "#4f4656", edge: "#9a839f", detail: "#6d5d73", deep: "#332d38" },
  empalizada: { base: "#4b3627", edge: "#b28858", detail: "#755038", deep: "#2f2118" },
  escombros: { base: "#4a4440", edge: "#9b8d7b", detail: "#6b6055", deep: "#302c29" },
};

const CARDS = {
  [WHITE]: { fill: "#f4e7ca", line: "#2b1b14", star: "#ecd398" },
  [BLACK]: { fill: "#38204d", line: "#d7b170", star: "#b28ce0" },
  [RED]: { fill: "#8c2620", line: "#f2c17d", star: "#e06d5b" },
  [GREEN]: { fill: "#1f5938", line: "#c7e8ac", star: "#6ac48a" },
};

const IMPACT_AT = {
  [PAWN]: 0.58,
  [KNIGHT]: 0.78,
  [BISHOP]: 0.64,
  [ELEPHANT]: 0.74,
  [ROOK]: 0.68,
  [QUEEN]: 0.66,
  [KING]: 0.62,
  [FALCON]: 0.72,
  [AMAZON]: 0.68,
  [GRASSHOPPER]: 0.78,
  [NIGHTRIDER]: 0.76,
  [CENTAUR]: 0.70,
  [CAMEL]: 0.80,
  [LION]: 0.76,
  [ZEBRA]: 0.80,
  [PHOENIX]: 0.74,
};

const DURATION_MS = {
  [PAWN]: 260,
  [KNIGHT]: 360,
  [BISHOP]: 320,
  [ELEPHANT]: 370,
  [ROOK]: 300,
  [QUEEN]: 330,
  [KING]: 280,
  [FALCON]: 340,
  [AMAZON]: 350,
  [GRASSHOPPER]: 360,
  [NIGHTRIDER]: 380,
  [CENTAUR]: 320,
  [CAMEL]: 380,
  [LION]: 390,
  [ZEBRA]: 390,
  [PHOENIX]: 350,
};

export function durationFor(kind) {
  return DURATION_MS[kind] || 300;
}

export function impactAt(kind) {
  return IMPACT_AT[kind] || 0.66;
}

function easeOut(t) {
  return 1 - Math.pow(1 - t, 3);
}

export function motionPoint(kind, t, start, end, cell) {
  const [fx, fy] = start;
  const [tx, ty] = end;
  const impact = impactAt(kind);
  const progress = Math.min(1, Math.max(0, t / impact));
  const eased = easeOut(progress);
  let x = fx + (tx - fx) * eased;
  let y = fy + (ty - fy) * eased;
  const dx = tx - fx;
  const dy = ty - fy;

  if ([KNIGHT, NIGHTRIDER, CAMEL, ZEBRA, GRASSHOPPER, LION].includes(kind)) {
    y -= Math.sin(Math.PI * progress) * cell * 0.56;
  } else if ([ELEPHANT, FALCON, PHOENIX, CENTAUR].includes(kind)) {
    y -= Math.sin(Math.PI * progress) * cell * 0.42;
  } else if (kind === BISHOP) {
    const dist = Math.hypot(dx, dy);
    if (dist > 0) {
      const sway = Math.sin(Math.PI * progress) * cell * 0.055;
      x += (-dy / dist) * sway;
      y += (dx / dist) * sway;
    }
  } else if (kind === QUEEN || kind === AMAZON) {
    y -= Math.sin(Math.PI * progress) * cell * 0.13;
  } else if (kind === KING) {
    y -= Math.sin(Math.PI * progress) * cell * 0.055;
  } else if (kind === PAWN) {
    y -= Math.sin(Math.PI * progress) * cell * 0.07;
  }

  if (t > impact) {
    const settle = Math.min(1, (t - impact) / Math.max(0.001, 1 - impact));
    if ([ROOK, ELEPHANT, LION].includes(kind)) {
      x += Math.sin(settle * Math.PI * 7) * (1 - settle) * cell * 0.022;
    } else if (kind === KING) {
      y -= Math.sin(settle * Math.PI) * cell * 0.02;
    }
  }
  return [x, y];
}

export class BoardRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.flipped = false;
    this.scene = "classic";
    this.boardSize = 8;
    this.cell = 44;
    this.ox = 16;
    this.oy = 16;
    this.logicalSize = 360;
  }

  setScene(scene) {
    this.scene = SCENE_PALETTES[scene] ? scene : "classic";
  }

  resetFlip() {
    this.flipped = false;
  }

  toggleFlip() {
    this.flipped = !this.flipped;
  }

  displayPos(r, c) {
    const n = this.boardSize;
    return this.flipped ? [n - 1 - r, n - 1 - c] : [r, c];
  }

  boardPos(dr, dc) {
    const n = this.boardSize;
    return this.flipped ? [n - 1 - dr, n - 1 - dc] : [dr, dc];
  }

  squareCenter(r, c) {
    const [dr, dc] = this.displayPos(r, c);
    return [
      this.ox + (dc + 0.5) * this.cell,
      this.oy + (dr + 0.5) * this.cell,
    ];
  }

  squareAt(clientX, clientY) {
    const rect = this.canvas.getBoundingClientRect();
    const x = clientX - rect.left;
    const y = clientY - rect.top;
    if (this.cell <= 0) return null;
    const n = this.boardSize;
    const dc = Math.floor((x - this.ox) / this.cell);
    const dr = Math.floor((y - this.oy) / this.cell);
    if (dr >= 0 && dr < n && dc >= 0 && dc < n) {
      return this.boardPos(dr, dc);
    }
    return null;
  }

  resize() {
    const parent = this.canvas.parentElement;
    if (!parent) return;
    const rect = parent.getBoundingClientRect();
    const size = Math.max(260, Math.floor(Math.min(rect.width, rect.height || rect.width)));
    const dpr = Math.min(window.devicePixelRatio || 1, 2.5);
    if (this.canvas.width !== Math.floor(size * dpr) || this.logicalSize !== size) {
      this.logicalSize = size;
      this.canvas.width = Math.floor(size * dpr);
      this.canvas.height = Math.floor(size * dpr);
      this.canvas.style.width = `${size}px`;
      this.canvas.style.height = `${size}px`;
    }
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const n = this.boardSize;
    const margin = Math.max(18, size * 0.048);
    this.cell = (size - margin * 2) / n;
    const board = this.cell * n;
    this.ox = (size - board) / 2;
    this.oy = (size - board) / 2;
  }

  render(game, selected, selectedMoves, anim = null, visible = null) {
    const n = game.size || 8;
    this.boardSize = n;
    this.resize();
    const ctx = this.ctx;
    const size = this.logicalSize;
    const { ox, oy, cell } = this;
    const board = cell * n;
    const palette = SCENE_PALETTES[this.scene] || SCENE_PALETTES.classic;

    ctx.clearRect(0, 0, size, size);

    // Marco medieval del tablero
    const framePad = Math.max(10, cell * 0.22);
    ctx.save();
    ctx.fillStyle = "#08050c";
    this._roundRect(
      ox - framePad + 3,
      oy - framePad + 4,
      board + framePad * 2,
      board + framePad * 2,
      10
    );
    ctx.fill();

    ctx.fillStyle = palette.frame;
    ctx.strokeStyle = palette.edge;
    ctx.lineWidth = 2;
    this._roundRect(
      ox - framePad,
      oy - framePad,
      board + framePad * 2,
      board + framePad * 2,
      10
    );
    ctx.fill();
    ctx.stroke();

    ctx.strokeStyle = "#8b744a";
    ctx.lineWidth = 1;
    ctx.strokeRect(ox - 3, oy - 3, board + 6, board + 6);
    ctx.restore();

    // Casillas y coordenadas
    const coordSize = Math.max(8, Math.floor(cell * 0.17));
    ctx.font = `bold ${coordSize}px sans-serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    for (let dr = 0; dr < n; dr++) {
      for (let dc = 0; dc < n; dc++) {
        const [r, c] = this.boardPos(dr, dc);
        const x = ox + dc * cell;
        const y = oy + dr * cell;
        ctx.fillStyle = (r + c) % 2 === 0 ? palette.light : palette.dark;
        ctx.fillRect(x, y, cell + 0.6, cell + 0.6);

        if (dc === 0) {
          ctx.fillStyle = palette.coord;
          ctx.fillText(String(n - r), ox - framePad * 0.52, y + cell / 2);
        }
        if (dr === n - 1) {
          ctx.fillStyle = palette.coord;
          ctx.fillText(FILE_LETTERS[c].toUpperCase(), x + cell / 2, oy + board + framePad * 0.54);
        }
      }
    }

    // Terrenos tácticos
    this._drawTerrain(game, visible);

    // Última jugada
    if (game.last_move) {
      for (const [r, c] of [
        [game.last_move.fr, game.last_move.fc],
        [game.last_move.tr, game.last_move.tc],
      ]) {
        if (!visible || visible.has(`${r},${c}`)) {
          this._highlightSquare(r, c, "rgba(200, 163, 95, 0.28)");
        }
      }
    }

    // Jaque al Rey
    if (game.inCheck(game.turn)) {
      const kingPos = game.findKing(game.turn);
      if (kingPos && (!visible || visible.has(`${kingPos[0]},${kingPos[1]}`))) {
        this._highlightSquare(kingPos[0], kingPos[1], "rgba(217, 106, 95, 0.42)", "#d96a5f");
      }
    }

    // Casilla seleccionada y movimientos legales
    if (selected) {
      this._highlightSquare(selected[0], selected[1], "rgba(236, 211, 152, 0.34)", "#ecd398");
      for (const move of selectedMoves) {
        const [dr, dc] = this.displayPos(move.tr, move.tc);
        const cx = ox + (dc + 0.5) * cell;
        const cy = oy + (dr + 0.5) * cell;
        const isCapture =
          move.captured !== null ||
          move.is_en_passant ||
          game.grid[move.tr][move.tc] !== null;

        ctx.save();
        if (isCapture) {
          ctx.strokeStyle = "#d96a5f";
          ctx.lineWidth = Math.max(2.5, cell * 0.06);
          ctx.beginPath();
          ctx.arc(cx, cy, cell * 0.37, 0, Math.PI * 2);
          ctx.stroke();
        } else {
          ctx.fillStyle = "#ecd398";
          ctx.strokeStyle = "#c8a35f";
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.arc(cx, cy, cell * 0.13, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
        }
        ctx.restore();
      }
    }

    // Piezas estáticas
    const hidePid = anim && anim.piece ? anim.piece.pid : null;
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        if (visible && !visible.has(`${r},${c}`)) continue;
        const piece = game.grid[r][c];
        if (!piece) continue;
        if (hidePid !== null && piece.pid === hidePid) continue;
        const [cx, cy] = this.squareCenter(r, c);
        this._drawPiece(cx, cy, piece, cell * 0.72);
      }
    }

    // Niebla de guerra
    if (visible) {
      this._drawFog(visible);
    }

    // Animación en curso (estela, víctima empujada, onda de impacto y pieza en vuelo)
    if (anim) {
      this._drawAnimation(anim);
    }
  }

  _highlightSquare(r, c, fillRgba, borderHex = null) {
    const [dr, dc] = this.displayPos(r, c);
    const x = this.ox + dc * this.cell;
    const y = this.oy + dr * this.cell;
    this.ctx.save();
    this.ctx.fillStyle = fillRgba;
    this.ctx.fillRect(x, y, this.cell, this.cell);
    if (borderHex) {
      this.ctx.strokeStyle = borderHex;
      this.ctx.lineWidth = 2;
      this.ctx.strokeRect(x + 1, y + 1, this.cell - 2, this.cell - 2);
    }
    this.ctx.restore();
  }

  _drawFog(visible) {
    const ctx = this.ctx;
    const { ox, oy, cell, boardSize: n } = this;
    ctx.save();
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        if (visible.has(`${r},${c}`)) continue;
        const [dr, dc] = this.displayPos(r, c);
        const x = ox + dc * cell;
        const y = oy + dr * cell;
        ctx.fillStyle = "rgba(13, 9, 20, 0.82)";
        ctx.fillRect(x, y, cell + 0.5, cell + 0.5);
        ctx.strokeStyle = "rgba(90, 68, 118, 0.22)";
        ctx.lineWidth = 1;
        ctx.strokeRect(x + 0.5, y + 0.5, cell - 1, cell - 1);
      }
    }
    ctx.restore();
  }

  _drawPiece(x, y, piece, size, alpha = 1) {
    const ctx = this.ctx;
    const glyph = PIECE_GLYPHS[piece.kind] || "♟";
    const card = CARDS[piece.color] || CARDS[WHITE];
    const fontSize = Math.max(12, Math.round(size));
    const outlineOff = Math.max(1.2, size * 0.045);

    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.font = `${fontSize}px "DejaVu Sans", "Segoe UI Symbol", "Apple Symbols", serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Sombra proyectada
    ctx.fillStyle = "#08050c";
    ctx.fillText(glyph, x + outlineOff * 0.7, y + outlineOff * 1.6);

    // Contorno nítido
    ctx.lineWidth = outlineOff * 2.1;
    ctx.strokeStyle = card.line;
    ctx.lineJoin = "round";
    ctx.strokeText(glyph, x, y);

    // Cuerpo de la pieza
    ctx.fillStyle = card.fill;
    ctx.fillText(glyph, x, y);

    // Insignia de Veterano (★)
    if (piece.veteran) {
      const starX = x + size * 0.34;
      const starY = y - size * 0.32;
      const starFont = Math.max(9, Math.round(size * 0.31));
      ctx.font = `bold ${starFont}px sans-serif`;
      ctx.fillStyle = "#08050c";
      ctx.fillText("★", starX + 1, starY + 1);
      ctx.fillStyle = card.star;
      ctx.fillText("★", starX, starY);
    }
    ctx.restore();
  }

  _drawTerrain(game, visible) {
    const ctx = this.ctx;
    const { ox, oy, cell } = this;
    for (const [r, c, kind] of game.terrainEntries()) {
      if (visible && !visible.has(`${r},${c}`)) continue;
      const [dr, dc] = this.displayPos(r, c);
      const x = ox + dc * cell;
      const y = oy + dr * cell;
      const style = TERRAIN_STYLE[kind] || TERRAIN_STYLE.escombros;

      ctx.save();
      ctx.fillStyle = style.base;
      ctx.fillRect(x, y, cell + 0.5, cell + 0.5);
      ctx.strokeStyle = style.deep;
      ctx.lineWidth = 1;
      ctx.strokeRect(x + 0.5, y + 0.5, cell - 1, cell - 1);

      if (kind === "bosque") {
        this._drawBosque(ctx, x, y, cell, style);
      } else if (kind === "rio") {
        this._drawRio(ctx, x, y, cell, style);
      } else if (kind === "acantilado") {
        this._drawAcantilado(ctx, x, y, cell, style);
      } else if (kind === "penasco") {
        this._drawPenasco(ctx, x, y, cell, style);
      } else if (kind === "ruinas") {
        this._drawRuinas(ctx, x, y, cell, style);
      } else if (kind === "empalizada") {
        this._drawEmpalizada(ctx, x, y, cell, style);
      } else {
        this._drawEscombros(ctx, x, y, cell, style);
      }
      ctx.restore();
    }
  }

  _drawBosque(ctx, x, y, s, style) {
    ctx.lineWidth = Math.max(1, s * 0.03);
    for (const [fx, fy, scale] of [
      [0.3, 0.74, 0.2],
      [0.63, 0.65, 0.16],
      [0.47, 0.45, 0.11],
    ]) {
      const cx = x + fx * s;
      const base = y + fy * s;
      const h = scale * s;
      ctx.strokeStyle = style.deep;
      ctx.beginPath();
      ctx.moveTo(cx, base);
      ctx.lineTo(cx, base - h * 0.5);
      ctx.stroke();

      ctx.fillStyle = style.detail;
      ctx.strokeStyle = style.edge;
      ctx.beginPath();
      ctx.moveTo(cx, base - h * 1.55);
      ctx.lineTo(cx + h * 0.72, base - h * 0.42);
      ctx.lineTo(cx - h * 0.72, base - h * 0.42);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }
  }

  _drawRio(ctx, x, y, s, style) {
    ctx.lineWidth = Math.max(1.5, s * 0.05);
    ctx.lineCap = "round";
    [0.28, 0.52, 0.76].forEach((fy, idx) => {
      ctx.strokeStyle = idx === 1 ? style.edge : style.detail;
      ctx.beginPath();
      ctx.moveTo(x + 0.08 * s, y + fy * s);
      ctx.bezierCurveTo(
        x + 0.32 * s,
        y + (fy - 0.09) * s,
        x + 0.58 * s,
        y + (fy + 0.09) * s,
        x + 0.92 * s,
        y + fy * s
      );
      ctx.stroke();
    });
  }

  _drawAcantilado(ctx, x, y, s, style) {
    ctx.lineWidth = Math.max(1, s * 0.03);
    const pts = [
      [0.02, 0.9], [0.1, 0.55], [0.24, 0.62], [0.35, 0.28],
      [0.5, 0.5], [0.68, 0.22], [0.8, 0.48], [0.98, 0.38], [0.98, 0.9],
    ];
    ctx.fillStyle = style.detail;
    ctx.strokeStyle = style.edge;
    ctx.beginPath();
    pts.forEach(([px, py], i) => {
      if (i === 0) ctx.moveTo(x + px * s, y + py * s);
      else ctx.lineTo(x + px * s, y + py * s);
    });
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  }

  _drawPenasco(ctx, x, y, s, style) {
    ctx.lineWidth = Math.max(1, s * 0.03);
    for (const [cx, cy, radius] of [
      [0.34, 0.64, 0.22],
      [0.62, 0.73, 0.18],
      [0.55, 0.42, 0.13],
    ]) {
      const px = x + cx * s;
      const py = y + cy * s;
      const r = radius * s;
      ctx.fillStyle = style.detail;
      ctx.strokeStyle = style.edge;
      ctx.beginPath();
      ctx.moveTo(px, py - r);
      ctx.lineTo(px + r, py - r * 0.2);
      ctx.lineTo(px + r * 0.55, py + r);
      ctx.lineTo(px - r * 0.55, py + r);
      ctx.lineTo(px - r, py - r * 0.2);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }
  }

  _drawRuinas(ctx, x, y, s, style) {
    ctx.lineWidth = Math.max(1, s * 0.025);
    ctx.fillStyle = style.detail;
    ctx.strokeStyle = style.edge;
    for (const [fx, fy, w, h] of [
      [0.14, 0.48, 0.16, 0.36],
      [0.36, 0.34, 0.15, 0.5],
      [0.58, 0.52, 0.13, 0.32],
      [0.76, 0.41, 0.12, 0.43],
    ]) {
      ctx.fillRect(x + fx * s, y + fy * s, w * s, h * s);
      ctx.strokeRect(x + fx * s, y + fy * s, w * s, h * s);
    }
  }

  _drawEmpalizada(ctx, x, y, s, style) {
    ctx.lineWidth = Math.max(1.5, s * 0.04);
    for (const fx of [0.2, 0.4, 0.6, 0.8]) {
      const cx = x + fx * s;
      ctx.strokeStyle = style.detail;
      ctx.beginPath();
      ctx.moveTo(cx, y + 0.24 * s);
      ctx.lineTo(cx, y + 0.82 * s);
      ctx.stroke();
    }
    ctx.strokeStyle = style.edge;
    for (const fy of [0.46, 0.68]) {
      ctx.beginPath();
      ctx.moveTo(x + 0.08 * s, y + fy * s);
      ctx.lineTo(x + 0.92 * s, y + fy * s);
      ctx.stroke();
    }
  }

  _drawEscombros(ctx, x, y, s, style) {
    ctx.lineWidth = Math.max(1, s * 0.025);
    for (const [cx, cy, radius] of [
      [0.28, 0.66, 0.15],
      [0.55, 0.58, 0.18],
      [0.76, 0.72, 0.12],
    ]) {
      const px = x + cx * s;
      const py = y + cy * s;
      const r = radius * s;
      ctx.fillStyle = style.detail;
      ctx.strokeStyle = style.edge;
      ctx.beginPath();
      ctx.moveTo(px - r, py + r * 0.5);
      ctx.lineTo(px - r * 0.5, py - r);
      ctx.lineTo(px + r * 0.7, py - r * 0.4);
      ctx.lineTo(px + r, py + r * 0.7);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }
  }

  _drawAnimation(anim) {
    const ctx = this.ctx;
    const { cell } = this;
    const { piece, t, fromSq, toSq, captureSq, victim, push } = anim;
    const start = this.squareCenter(fromSq[0], fromSq[1]);
    const end = this.squareCenter(toSq[0], toSq[1]);
    const impact = impactAt(piece.kind);

    // 1. Estela (Trail)
    if (t > 0 && t < impact) {
      const magical = [BISHOP, QUEEN, KING].includes(piece.kind);
      const magicalTrails = {
        [WHITE]: "rgba(236, 211, 152, 0.45)",
        [BLACK]: "rgba(178, 140, 224, 0.45)",
        [RED]: "rgba(224, 109, 91, 0.45)",
        [GREEN]: "rgba(106, 196, 138, 0.45)",
      };
      const trailColor = magical
        ? magicalTrails[piece.color] || magicalTrails[WHITE]
        : "rgba(169, 132, 91, 0.42)";
      const count = piece.kind === PAWN ? 2 : 3;
      const sizes = [0.055, 0.04, 0.028];
      ctx.save();
      ctx.fillStyle = trailColor;
      for (let i = 0; i < count; i++) {
        const lag = t - 0.075 * (i + 1);
        if (lag <= 0 || lag >= impact) continue;
        const [lx, ly] = motionPoint(piece.kind, lag, start, end, cell);
        const radius = cell * sizes[i] * (1 - (lag / impact) * 0.3);
        ctx.beginPath();
        ctx.arc(lx, ly, radius, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }

    // 2. Impacto y víctima desplazada
    if (captureSq && t >= impact) {
      const progress = Math.min(1, (t - impact) / Math.max(0.001, 1 - impact));
      const [ix, iy] = this.squareCenter(captureSq[0], captureSq[1]);

      if (victim && progress < 0.92) {
        const scale = Math.max(0.56, 1 - progress * 0.44);
        const travel = cell * 0.28 * progress;
        const gravity = cell * 0.2 * progress * progress;
        const vx = ix + push[0] * travel;
        const vy = iy + push[1] * travel + gravity;
        this._drawPiece(vx, vy, victim, cell * 0.72 * scale, 1 - progress * 0.85);
      }

      // Onda expansiva y destello de captura
      ctx.save();
      const card = CARDS[piece.color] || CARDS[WHITE];
      const accent = card.star;
      ctx.strokeStyle = "#d96a5f";
      ctx.lineWidth = Math.max(1.5, cell * 0.06 * (1 - progress));
      ctx.globalAlpha = 1 - progress;
      ctx.beginPath();
      ctx.arc(ix, iy, cell * (0.08 + progress * 0.38), 0, Math.PI * 2);
      ctx.stroke();

      ctx.strokeStyle = accent;
      ctx.lineWidth = Math.max(1, cell * 0.035 * (1 - progress));
      ctx.beginPath();
      ctx.arc(ix, iy, cell * (0.05 + progress * 0.28), 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }

    // 3. Pieza en movimiento
    const [mx, my] = motionPoint(piece.kind, t, start, end, cell);
    this._drawPiece(mx, my, piece, cell * 0.74);
  }

  _roundRect(x, y, w, h, r) {
    const ctx = this.ctx;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
}
