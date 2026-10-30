/**
 * Entidades inmutables de piezas, movimientos y notación algebraica (8x8 y 12x12).
 */

import { FILE_LETTERS, PAWN, PIECE_LETTER_ES } from "./constants.js";

export function createPiece(
  color,
  kind,
  pid,
  name = "",
  title = "",
  kills = 0,
  veteran = false
) {
  return Object.freeze({ color, kind, pid, name, title, kills, veteran });
}

export function createMove(
  fr,
  fc,
  tr,
  tc,
  {
    promotion = null,
    castle = null,
    is_en_passant = false,
    captured = null,
    moved = null,
    placed = null,
    eliminated_factions = [],
  } = {}
) {
  return {
    fr,
    fc,
    tr,
    tc,
    promotion,
    castle,
    is_en_passant,
    captured,
    moved,
    placed,
    eliminated_factions,
  };
}

export function algebraic(r, c, size = 8) {
  return `${FILE_LETTERS[c]}${size - r}`;
}

export function moveNotation(move, check = false, mate = false, size = 8) {
  let text = "";
  if (move.castle === "K") {
    text = "0-0";
  } else if (move.castle === "Q") {
    text = "0-0-0";
  } else {
    const piece = move.moved;
    const dest = algebraic(move.tr, move.tc, size);
    if (piece && piece.kind === PAWN) {
      text = (move.captured ? `${FILE_LETTERS[move.fc]}x` : "") + dest;
    } else {
      const letter = piece ? PIECE_LETTER_ES[piece.kind] || "" : "";
      text = letter + (move.captured ? "x" : "") + dest;
    }
    if (move.promotion) {
      text += `=${PIECE_LETTER_ES[move.promotion] || ""}`;
    }
  }
  return text + (mate ? "#" : check ? "+" : "");
}
