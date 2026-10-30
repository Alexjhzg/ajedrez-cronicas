"""Controlador principal de la interfaz de Crónicas de Aethelgard."""

from __future__ import annotations

import math
import queue
import random
import threading
import time
import tkinter as tk
from typing import Optional

from .. import lore
from ..engine import (
    BLACK, WHITE, Move, Piece, find_best_move, move_notation,
)
from .animations import (
    ImpactEffect, TrailEffect, VictimEffect, frames_for, impact_at,
    motion_point,
)
from .board import BoardView
from .dialogs import (
    ConfirmDialog, CrusadeInterludeDialog, DilemmaDialog, EndDialog,
    PromotionDialog, SetupDialog,
)
from .pieces import create_piece_items
from .sidebar import SidebarView
from .state import Snapshot, ViewState
from .status import StatusBar
from .theme import (
    BG, DANGER_SOFT, DIFFICULTIES, FACTION_ACCENT, GLYPH_FONT, GOLD_LIGHT,
    IVORY, MUTED, SERIF, VIOLET, configure_styles,
)
from .widgets import make_button


class ChroniclesApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Crónicas de Aethelgard · Ajedrez Medieval")
        self.configure(bg=BG)
        self.minsize(1140, 660)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        width = min(1320, screen_w - 70)
        height = min(860, screen_h - 90)
        self.geometry(
            f"{width}x{height}+{(screen_w - width) // 2}+{(screen_h - height) // 2}"
        )

        self.mode = "ai"
        self.difficulty = "Caballero"
        self.player_color = WHITE
        self.wild = False
        self.crusade = False
        self.four_fronts = False
        self.imperial = False
        self.crusade_state: Optional[lore.CrusadeState] = None
        self.elephant = False
        self.fog = False
        self.scenario: Optional[lore.WildScenario] = None
        self.started = False
        self.game = lore.create_game()

        self.selected: Optional[tuple[int, int]] = None
        self.selected_moves: list[Move] = []
        self.focus_piece: Optional[Piece] = self._find_king(WHITE)
        self.chapter = 0
        self.ply = 0
        self.story = []
        self.notation: list[str] = []
        self.snapshots: list[Snapshot] = []

        self.game_over = False
        self.result: Optional[dict] = None
        self.start_time: Optional[float] = None

        self.busy = False
        self.anim = None
        self.anim_after = None
        self.ai_thinking = False
        self.ai_queue: queue.Queue = queue.Queue()
        self.ai_serial = 0
        self.ai_poll_after = None
        self.ai_start_after = None
        self.end_after = None

        self.setup_dialog: Optional[tk.Toplevel] = None
        self.end_dialog: Optional[tk.Toplevel] = None
        self.promotion_dialog: Optional[tk.Toplevel] = None
        self.confirm_dialog: Optional[tk.Toplevel] = None
        self.dilemma_dialog: Optional[tk.Toplevel] = None
        self.interlude_dialog: Optional[tk.Toplevel] = None

        self._resize_after = None
        self._last_cursor = ""

        configure_styles(self)
        self._build_layout()
        self._bind_events()
        self.after(60, self._startup)

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def _build_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        content = tk.Frame(self, bg=BG)
        content.grid(row=0, column=0, sticky="nsew", padx=18, pady=14)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, minsize=396)

        left = tk.Frame(content, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        self._build_header(left)
        self._build_board(left)
        self.status_bar = StatusBar(left)
        self.status_bar.grid(row=2, column=0, sticky="ew", pady=(9, 0))
        self.sidebar = SidebarView(content)
        self.sidebar.grid(row=0, column=1, sticky="nsew")

    def _build_header(self, parent: tk.Frame) -> None:
        header = tk.Frame(parent, bg=BG)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)

        title_box = tk.Frame(header, bg=BG)
        title_box.grid(row=0, column=0, sticky="w")
        tk.Label(
            title_box, text="CRÓNICAS DE AETHELGARD", bg=BG, fg=GOLD_LIGHT,
            font=(SERIF, 18, "bold"),
        ).pack(anchor="w")
        self.header_sub = tk.Label(
            title_box,
            text="Ajedrez de la Era Umbría  ·  cada jugada escribe una página",
            bg=BG, fg=MUTED, font=(SERIF, 9, "italic"),
        )
        self.header_sub.pack(anchor="w", pady=(2, 0))

        buttons = tk.Frame(header, bg=BG)
        buttons.grid(row=0, column=1, sticky="e", padx=(14, 0))
        self.new_btn = make_button(
            buttons, "Nueva", self._open_setup, accent=True, compact=True,
        )
        self.new_btn.pack(side="left", padx=(0, 6))
        self.undo_btn = make_button(buttons, "Deshacer", self.undo, compact=True)
        self.undo_btn.pack(side="left", padx=(0, 6))
        self.flip_btn = make_button(buttons, "Girar", self._flip_board, compact=True)
        self.flip_btn.pack(side="left", padx=(0, 6))
        self.surrender_btn = make_button(
            buttons, "Abandonar", self._ask_surrender, compact=True,
        )
        self.surrender_btn.pack(side="left")

    def _build_board(self, parent: tk.Frame) -> None:
        holder = tk.Frame(parent, bg=BG)
        holder.grid(row=1, column=0, sticky="nsew")
        holder.grid_rowconfigure(0, weight=1)
        holder.grid_columnconfigure(0, weight=1)
        self.board = BoardView(holder)
        self.board.grid(row=0, column=0, sticky="nsew")

    def _bind_events(self) -> None:
        self.board.bind("<Button-1>", self._on_click)
        self.board.bind("<Motion>", self._on_motion)
        self.board.bind("<Leave>", self._on_leave)
        self.board.bind("<Configure>", self._on_resize)
        self.bind("<Key-u>", self._key_undo)
        self.bind("<Key-f>", self._key_flip)
        self.bind("<Escape>", self._key_escape)
        self.board.bind("<Key-u>", self._key_undo)
        self.board.bind("<Key-f>", self._key_flip)
        self.board.bind("<Escape>", self._key_escape)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------------
    # Arranque y partida
    # ------------------------------------------------------------------
    def _startup(self) -> None:
        self.render()
        self._update_sidebar()
        self._update_buttons()
        self._redraw_story()
        self._open_setup()

    def _find_king(self, color: str) -> Optional[Piece]:
        pos = self.game.find_king(color)
        return self.game.grid[pos[0]][pos[1]] if pos else None

    def _open_setup(self) -> None:
        if self.busy or self.ai_thinking:
            return
        if self.end_dialog is not None and self.end_dialog.winfo_exists():
            self.end_dialog.destroy()
            self.end_dialog = None
        if self.setup_dialog is not None and self.setup_dialog.winfo_exists():
            self.setup_dialog.lift()
            return
        self._cancel_ai_start()
        self.setup_dialog = SetupDialog(
            self,
            self.start_new_game,
            cancel_allowed=self.started,
            on_cancel=self._resume_ai,
            on_closed=self._clear_setup_dialog,
            initial_mode=self.mode,
            initial_difficulty=self.difficulty,
            initial_wild=self.wild,
            initial_elephant=self.elephant,
            initial_fog=self.fog,
            initial_crusade=self.crusade,
            initial_four_fronts=self.four_fronts,
            initial_player_color=self.player_color,
            initial_imperial=self.imperial,
        )

    def _clear_setup_dialog(self) -> None:
        self.setup_dialog = None

    def _resume_ai(self) -> None:
        if (
            self.started and not self.game_over and self.mode == "ai"
            and self.game.turn != self.player_color and not self.ai_thinking
            and not self.busy
        ):
            self.after(40, self._schedule_ai)

    def start_new_game(
        self,
        mode: str,
        difficulty: str,
        wild: bool = False,
        elephant: bool = False,
        fog: bool = False,
        crusade: bool = False,
        four_fronts: bool = False,
        player_color: str = WHITE,
        imperial: bool = False,
    ) -> None:
        self._cancel_animation()
        self._close_end_dialog()
        self._clear_ai()
        self._cancel_end_timer()

        self.mode = "ai" if crusade else mode
        self.difficulty = difficulty
        self.player_color = player_color
        self.imperial = imperial
        self.four_fronts = four_fronts and not imperial
        self.wild = (wild or crusade) and not four_fronts and not imperial
        self.crusade = crusade and not four_fronts and not imperial
        self.elephant = elephant
        self.fog = fog
        self.board.reset_flip()
        self.started = True
        self.game_over = False
        self.result = None
        self.selected = None
        self.selected_moves = []
        self.snapshots = []
        self.story = []
        self.notation = []
        self.chapter = 0
        self.ply = 0
        self.start_time = time.time()

        enemy_color = BLACK if player_color != BLACK else WHITE

        if self.crusade:
            self.crusade_state = lore.create_crusade(
                elephant=elephant, player_color=player_color,
            )
            self._launch_crusade_stage()
            return

        self.crusade_state = None
        if self.imperial:
            self.scenario = None
            self.game = lore.create_imperial_game(
                player_color=player_color, enemy_color=enemy_color,
            )
            self.board.set_scene("imperial")
            self.title("Crónicas de Aethelgard · Gran Tablero Imperial (12x12)")
            self.header_sub.configure(
                text="Imperio 12x12  ·  Las 10 Órdenes Míticas del Códice en batalla",
            )
            intro = lore.imperial_prologue(
                self.mode == "ai", difficulty, fog=fog,
                player_color=player_color, enemy_color=enemy_color,
            )
            hint = f"Imperio 12x12: {lore.faction_name(player_color)} despliega su legión."
        elif self.four_fronts:
            self.scenario = None
            self.game = lore.create_four_fronts_game(
                elephant=elephant, player_color=player_color,
            )
            self.board.set_scene("ruinas")
            self.title("Crónicas de Aethelgard · Guerra de los Cuatro Frentes")
            self.header_sub.configure(
                text="Guerra de 4 Frentes  ·  Alba, Forja, Eclipse y Pacto en batalla",
            )
            intro = lore.four_fronts_prologue(
                self.mode == "ai", difficulty, elephant=elephant,
                fog=fog, player_color=player_color,
            )
            hint = f"Guerra de 4 Frentes: {lore.faction_name(player_color)} abre la marcha."
        elif self.wild:
            scenario = lore.create_wild_scenario(
                elephant=elephant, player_color=player_color, enemy_color=enemy_color,
            )
            self.scenario = scenario
            self.game = scenario.game
            self.board.set_scene(scenario.theme)
            self.title(f"Crónicas de Aethelgard · {scenario.title}")
            self.header_sub.configure(
                text=f"Tierra Salvaje  ·  {scenario.title}",
            )
            intro = lore.wild_prologue(
                scenario, self.mode == "ai", difficulty, fog=fog,
            )
            hint = f"Tierra Salvaje: {lore.faction_name(player_color)} mueve primero."
        else:
            self.scenario = None
            self.game = lore.create_game(
                elephant=elephant, player_color=player_color, enemy_color=enemy_color,
            )
            self.board.set_scene("classic")
            self.title("Crónicas de Aethelgard · Ajedrez Medieval")
            self.header_sub.configure(
                text="Ajedrez de la Era Umbría  ·  cada jugada escribe una página",
            )
            intro = lore.prologue(
                self.mode == "ai", difficulty, elephant=elephant, fog=fog,
                player_color=player_color, enemy_color=enemy_color,
            )
            hint = f"{lore.faction_name(player_color)} mueve primero. Selecciona una pieza."

        self.focus_piece = self._find_king(player_color)
        self.story.append(intro)
        self._redraw_story()
        self.render()
        self._update_sidebar()
        self._update_buttons()
        self.board.focus_set()
        self.status_bar.set_hint(hint, MUTED)

    def _launch_crusade_stage(self, boon_note: str = "") -> None:
        assert self.crusade_state is not None
        scenario, stage_diff = lore.create_crusade_stage(
            self.crusade_state, elephant=self.elephant,
        )
        self.scenario = scenario
        self.game = scenario.game
        self.difficulty = stage_diff
        self.game_over = False
        self.result = None
        self.selected = None
        self.selected_moves = []
        self.snapshots = []
        self.notation = []
        self.chapter = 0
        self.ply = 0
        self.board.set_scene(scenario.theme)
        stage_num = self.crusade_state.stage + 1
        total = self.crusade_state.total_stages
        self.title(f"Crónicas de Aethelgard · Cruzada ({stage_num}/{total})")
        self.header_sub.configure(
            text=f"Cruzada Encadenada ({stage_num}/{total})  ·  {scenario.title}",
        )
        intro = lore.wild_prologue(
            scenario, True, self.difficulty, fog=self.fog,
        )
        if boon_note:
            intro = lore.LoreEntry(
                intro.heading, f"{boon_note}\n\n{intro.text}", intro.tag,
            )
        self.focus_piece = self._find_king(self.player_color)
        self.story.append(intro)
        self._redraw_story()
        self.render()
        self._update_sidebar()
        self._update_buttons()
        self.board.focus_set()
        self.status_bar.set_hint(
            f"Cruzada Etapa {stage_num}/{total}: tus supervivientes toman posición.",
            GOLD_LIGHT,
        )

    def _clear_ai(self) -> None:
        self.ai_serial += 1
        self.ai_thinking = False
        self._cancel_ai_start()
        if self.ai_poll_after is not None:
            try:
                self.after_cancel(self.ai_poll_after)
            except tk.TclError:
                pass
            self.ai_poll_after = None
        while True:
            try:
                self.ai_queue.get_nowait()
            except queue.Empty:
                break

    # ------------------------------------------------------------------
    # Turno, interacción y movimiento
    # ------------------------------------------------------------------
    def _human_can_move(self) -> bool:
        if not self.started or self.game_over or self.busy or self.ai_thinking:
            return False
        if self.mode == "ai" and self.game.turn != self.player_color:
            return False
        return True

    def _visible_squares(self) -> Optional[set[tuple[int, int]]]:
        if not self.fog or not self.started or self.game_over:
            return None
        perspective = self.player_color if self.mode == "ai" else self.game.turn
        return self.game.visible_squares(perspective)

    def _on_click(self, event) -> None:
        self.board.focus_set()
        if not self._human_can_move():
            return
        square = self.board.square_at(event.x, event.y)
        if square is None:
            self._deselect()
            return
        r, c = square
        visible = self._visible_squares()
        if (visible is None or (r, c) in visible) and self.game.is_blocked(r, c):
            kind = self.game.terrain[(r, c)]
            self.status_bar.set_hint(
                f"{lore.terrain_label(kind)}: el paso está cerrado.", MUTED,
            )
            return
        piece = self.game.grid[r][c]

        if self.selected is not None:
            targets = [m for m in self.selected_moves if (m.tr, m.tc) == (r, c)]
            if targets:
                if len(targets) > 1:
                    self._open_promotion(targets)
                else:
                    self._perform_move(targets[0])
                return
            if visible is not None and (r, c) not in visible:
                self._deselect()
                self.status_bar.set_hint(
                    "La niebla de guerra oculta esa casilla.", MUTED,
                )
                return
            if piece is not None and piece.color == self.game.turn:
                if (r, c) == self.selected:
                    self._deselect()
                else:
                    self._select(r, c)
                return
            self._deselect()
            return

        if visible is not None and (r, c) not in visible:
            self.status_bar.set_hint(
                "La niebla de guerra oculta esa casilla.", MUTED,
            )
            return

        if piece is not None and piece.color == self.game.turn:
            self._select(r, c)
        elif piece is not None:
            self.focus_piece = piece
            self._update_character()

    def _select(self, r: int, c: int) -> None:
        piece = self.game.grid[r][c]
        if piece is None:
            return
        self.selected = (r, c)
        self.selected_moves = self.game.legal_moves_from(r, c)
        self.focus_piece = piece
        self._update_character()
        self.render()
        self.status_bar.set_hint(
            f"{piece.name}: elige una casilla iluminada." if self.selected_moves
            else f"{piece.name} no puede moverse sin condenar a su rey.",
            IVORY if self.selected_moves else DANGER_SOFT,
        )

    def _deselect(self) -> None:
        if self.selected is None:
            return
        self.selected = None
        self.selected_moves = []
        self.render()
        self._update_status()

    def _open_promotion(self, moves: list[Move]) -> None:
        if self.promotion_dialog is not None and self.promotion_dialog.winfo_exists():
            self.promotion_dialog.lift()
            return
        mover = moves[0].moved or self.game.grid[moves[0].fr][moves[0].fc]
        color = mover.color if mover else self.game.turn
        allowed = {m.promotion for m in moves if m.promotion is not None}
        self.promotion_dialog = PromotionDialog(
            self,
            color,
            mover.name if mover else "El escudero",
            lambda choice: self._promotion_chosen(choice, moves),
            on_closed=self._clear_promotion_dialog,
            allowed_kinds=allowed or None,
        )

    def _clear_promotion_dialog(self) -> None:
        self.promotion_dialog = None

    def _promotion_chosen(self, choice: Optional[str], moves: list[Move]) -> None:
        if choice is None:
            self.status_bar.set_hint(
                "Coronación cancelada. Elige de nuevo.", MUTED,
            )
            return
        for move in moves:
            if move.promotion == choice:
                self._perform_move(move)
                return

    def _save_snapshot(self) -> None:
        self.snapshots.append(
            Snapshot(
                game=self.game.clone(),
                story=list(self.story),
                notation=list(self.notation),
                chapter=self.chapter,
                ply=self.ply,
                focus=self.focus_piece,
            )
        )

    def _perform_move(self, move: Move) -> None:
        if self.game_over:
            return
        piece_before = self.game.grid[move.fr][move.fc]
        if piece_before is None:
            return
        self._save_snapshot()

        was_ai = self.ai_thinking
        self.selected = None
        self.selected_moves = []
        self.game.apply_move(move)
        if move.promotion is not None and move.placed is not None:
            placed = self.game.grid[move.tr][move.tc]
            if placed is not None:
                promo_name = lore.NAME_POOLS.get(
                    placed.color, lore.NAME_POOLS[WHITE],
                )[move.promotion][0]
                promoted = Piece(
                    placed.color, placed.kind, placed.pid, promo_name,
                    lore.PROMOTED_TITLE[move.promotion],
                    kills=placed.kills, veteran=placed.veteran,
                )
                self.game.grid[move.tr][move.tc] = promoted
                move.placed = promoted
        self.chapter += 1
        self.ply += 1

        pre_result = self.game.result()
        wild_entry = None
        pending_dilemma: Optional[lore.WildDilemma] = None
        if (
            self.wild and self.scenario is not None and pre_result is None
            and self.chapter % lore.WILD_EVENT_EVERY == 0
        ):
            if not was_ai:
                pending_dilemma = lore.wild_dilemma(self.game, self.scenario)
            if pending_dilemma is None:
                wild_entry = lore.wild_event(self.game, self.scenario)
        self._pending_dilemma = pending_dilemma

        check = self.game.in_check(self.game.turn)
        result = self.game.result()
        mate = bool(result and result.get("type") == "checkmate")
        visible_after = (
            self.game.visible_squares(
                self.player_color if self.mode == "ai" else self.game.turn
            )
            if self.fog and result is None
            else None
        )
        move_hidden = (
            visible_after is not None
            and (move.fr, move.fc) not in visible_after
            and (move.tr, move.tc) not in visible_after
            and not check
            and not mate
        )
        self.notation.append(
            "?"
            if move_hidden
            else move_notation(move, check=check, mate=mate, size=self.game.size)
        )
        if not move_hidden:
            self.focus_piece = move.placed or move.moved
        self.game_over = result is not None
        self.result = result

        entry = (
            lore.fog_entry(self.chapter)
            if move_hidden
            else lore.narrate_move(move, self.game, check, mate, self.chapter)
        )
        self.story.append(entry)
        self._append_story(entry)
        if wild_entry is not None:
            self.story.append(wild_entry)
            self._append_story(wild_entry)
        if result is None and not self.wild and self.chapter % 8 == 0:
            ambient = lore.ambient_entry(size=self.game.size)
            self.story.append(ambient)
            self._append_story(ambient)
        if result is not None:
            epilogue = lore.epilogue(result)
            self.story.append(epilogue)
            self._append_story(epilogue)

        if was_ai:
            self.ai_thinking = False
        if move_hidden:
            self.render()
            self._update_sidebar()
            self._update_buttons()
            self._post_move(result)
            return
        self.busy = True
        self._update_sidebar()
        self._update_buttons()
        self._begin_animation(move, result)

    # ------------------------------------------------------------------
    # Animación
    # ------------------------------------------------------------------
    def _capture_square(self, move: Move) -> Optional[tuple[int, int]]:
        if move.captured is None:
            return None
        if move.is_en_passant and move.moved is not None:
            fdr, _fdc = self.game.pawn_vector(move.moved.color)
            return move.tr - fdr, move.tc
        return move.tr, move.tc

    def _push_direction(
        self, move: Move, capture_pos: tuple[int, int],
    ) -> tuple[float, float]:
        to_x, to_y = self.board.square_center(move.tr, move.tc)
        if capture_pos != (move.tr, move.tc):
            victim_x, victim_y = self.board.square_center(*capture_pos)
            dx = victim_x - to_x
            dy = victim_y - to_y
        else:
            from_x, from_y = self.board.square_center(move.fr, move.fc)
            dx = to_x - from_x
            dy = to_y - from_y
        length = math.hypot(dx, dy)
        if length == 0:
            return 0.0, -1.0
        return dx / length, dy / length

    def _begin_animation(self, move: Move, result: Optional[dict]) -> None:
        piece = move.placed or move.moved or self.game.grid[move.tr][move.tc]
        if piece is None:
            self.busy = False
            self._post_move(result)
            return
        from_x, from_y = self.board.square_center(move.fr, move.fc)
        to_x, to_y = self.board.square_center(move.tr, move.tc)
        kind = piece.kind
        capture_pos = self._capture_square(move)
        self.anim = {
            "piece": piece,
            "move": move,
            "from": (from_x, from_y),
            "to": (to_x, to_y),
            "frame": 0,
            "frames": frames_for(kind),
            "impact": impact_at(kind),
            "ids": [],
            "result": result,
            "capture_pos": capture_pos,
            "victim": None,
            "trail": None,
            "impact_fx": None,
        }
        self.render()
        if capture_pos is not None and move.captured is not None:
            victim_x, victim_y = self.board.square_center(*capture_pos)
            self.anim["victim"] = VictimEffect(
                self.board, move.captured, victim_x, victim_y,
                self.board.cell,
            )
        self.anim["trail"] = TrailEffect(
            self.board, kind, piece.color, self.board.cell,
        )
        self.anim["ids"] = create_piece_items(
            self.board, from_x, from_y, piece,
            int(self.board.cell * 0.72), tags=("anim", "anim_mover"),
            font=GLYPH_FONT,
        )
        self.anim_after = self.after(16, self._animate_step)

    def _animate_step(self) -> None:
        anim = self.anim
        self.anim_after = None
        if anim is None:
            return
        frames = max(1, anim["frames"])
        t = min(1.0, anim["frame"] / max(1, frames - 1))
        piece = anim["piece"]
        start = anim["from"]
        end = anim["to"]
        x, y = motion_point(piece.kind, t, start, end, self.board.cell)
        for item_id, dx, dy in anim["ids"]:
            self.board.coords(item_id, x + dx, y + dy)
        trail = anim["trail"]
        if trail is not None:
            trail.update(t, start, end)
        capture_pos = anim["capture_pos"]
        if capture_pos is not None and t >= anim["impact"]:
            progress = min(
                1.0,
                (t - anim["impact"]) / max(0.001, 1.0 - anim["impact"]),
            )
            if anim["impact_fx"] is None:
                impact_x, impact_y = self.board.square_center(*capture_pos)
                anim["impact_fx"] = ImpactEffect(
                    self.board, piece.kind, piece.color,
                    impact_x, impact_y, self.board.cell,
                )
                self.board.tag_raise("anim_mover")
            anim["impact_fx"].update(progress)
            victim = anim["victim"]
            if victim is not None:
                push = self._push_direction(anim["move"], capture_pos)
                victim.update(progress, push, self.board.cell)
        anim["frame"] += 1
        if t >= 1.0:
            self._complete_animation()
        else:
            self.anim_after = self.after(16, self._animate_step)

    def _complete_animation(self) -> None:
        if self.anim is None:
            return
        if self.anim_after is not None:
            try:
                self.after_cancel(self.anim_after)
            except tk.TclError:
                pass
            self.anim_after = None
        result = self.anim.get("result")
        self.board.delete("anim")
        self.anim = None
        self.busy = False
        self.render()
        self._update_sidebar()
        self._update_buttons()
        self._post_move(result)

    def _cancel_animation(self) -> None:
        if self.anim_after is not None:
            try:
                self.after_cancel(self.anim_after)
            except tk.TclError:
                pass
            self.anim_after = None
        self.board.delete("anim")
        self.anim = None
        self.busy = False

    def _post_move(self, result: Optional[dict]) -> None:
        if not self.started:
            return
        dilemma = getattr(self, "_pending_dilemma", None)
        self._pending_dilemma = None
        if dilemma is not None and result is None:
            self._open_dilemma(dilemma)
            return
        self._update_status()
        if result is not None:
            self._cancel_end_timer()
            self.end_after = self.after(350, self._show_end_dialog)
        elif self.mode == "ai" and self.game.turn != self.player_color:
            self._cancel_ai_start()
            self.ai_start_after = self.after(280, self._schedule_ai)

    def _open_dilemma(self, dilemma: lore.WildDilemma) -> None:
        if self.dilemma_dialog is not None and self.dilemma_dialog.winfo_exists():
            self.dilemma_dialog.lift()
            return
        self.dilemma_dialog = DilemmaDialog(
            self,
            dilemma,
            self._on_dilemma_chosen,
            on_closed=self._clear_dilemma_dialog,
        )

    def _clear_dilemma_dialog(self) -> None:
        self.dilemma_dialog = None

    def _on_dilemma_chosen(self, choice: lore.WildChoice) -> None:
        entry = lore.apply_wild_choice(self.game, choice)
        if entry is not None:
            self.story.append(entry)
            self._append_story(entry)
        result = self.game.result()
        self.game_over = result is not None
        self.result = result
        if result is not None:
            epilogue = lore.epilogue(result)
            self.story.append(epilogue)
            self._append_story(epilogue)
        self.render()
        self._update_sidebar()
        self._update_buttons()
        self._post_move(result)

    # ------------------------------------------------------------------
    # Oráculo Umbrío (IA)
    # ------------------------------------------------------------------
    def _schedule_ai(self) -> None:
        self.ai_start_after = None
        if (
            not self.started or self.game_over or self.mode != "ai"
            or self.game.turn == self.player_color or self.ai_thinking or self.busy
        ):
            return
        self.ai_thinking = True
        self.ai_serial += 1
        serial = self.ai_serial
        config = DIFFICULTIES.get(self.difficulty, DIFFICULTIES["Caballero"])
        snapshot = self.game.clone()
        seed = random.randrange(1_000_000)

        def worker() -> None:
            try:
                move = find_best_move(
                    snapshot,
                    depth=config["depth"],
                    randomness=config["randomness"],
                    time_limit=config["time"],
                    rng=random.Random(seed),
                )
            except Exception:
                move = None
            self.ai_queue.put((serial, move))

        threading.Thread(target=worker, daemon=True).start()
        f_name = lore.faction_name(self.game.turn)
        self.status_bar.set_hint(
            f"El Oráculo ({f_name}) medita…",
            FACTION_ACCENT.get(self.game.turn, VIOLET),
        )
        self._update_sidebar()
        self._update_buttons()
        if self.ai_poll_after is not None:
            try:
                self.after_cancel(self.ai_poll_after)
            except tk.TclError:
                pass
        self.ai_poll_after = self.after(80, self._poll_ai)

    def _poll_ai(self) -> None:
        self.ai_poll_after = None
        if not self.started or not self.ai_thinking:
            return
        try:
            serial, move = self.ai_queue.get_nowait()
        except queue.Empty:
            self.ai_poll_after = self.after(90, self._poll_ai)
            return
        if serial != self.ai_serial:
            self.ai_poll_after = self.after(20, self._poll_ai)
            return
        self.ai_thinking = False
        if self.game_over or self.game.turn == self.player_color:
            self._update_sidebar()
            self._update_buttons()
            return

        legal = self.game.legal_moves(self.game.turn)
        chosen = None
        if move is not None:
            for candidate in legal:
                if (
                    candidate.fr == move.fr and candidate.fc == move.fc
                    and candidate.tr == move.tr and candidate.tc == move.tc
                    and candidate.promotion == move.promotion
                ):
                    chosen = candidate
                    break
        if chosen is None and legal:
            chosen = random.choice(legal)
        if chosen is None:
            self._update_sidebar()
            return
        self._perform_move(chosen)

    # ------------------------------------------------------------------
    # Eventos de botones y teclado
    # ------------------------------------------------------------------
    def undo(self) -> None:
        if not self.started or self.busy or self.ai_thinking or not self.snapshots:
            return
        self._cancel_animation()
        self._cancel_end_timer()
        self._close_end_dialog()
        self.game_over = False
        self.result = None
        steps = 0
        while self.snapshots:
            snapshot = self.snapshots.pop()
            self.game = snapshot.game.clone()
            self.story = list(snapshot.story)
            self.notation = list(snapshot.notation)
            self.chapter = snapshot.chapter
            self.ply = snapshot.ply
            self.focus_piece = snapshot.focus
            steps += 1
            if self.mode != "ai" or self.game.turn == self.player_color:
                break
            if steps >= 4:
                break
        if self.focus_piece is None:
            self.focus_piece = self._find_king(self.player_color)
        self.selected = None
        self.selected_moves = []
        self._redraw_story()
        self.render()
        self._update_sidebar()
        self._update_buttons()
        self._update_status()
        self.status_bar.set_hint("La crónica retrocede una página.", MUTED)

    def _flip_board(self) -> None:
        if self.busy:
            return
        self.board.toggle_flip()
        self.render()

    def _ask_surrender(self) -> None:
        if not self.started or self.game_over or self.busy or self.ai_thinking:
            return
        if self.mode == "ai" and self.game.turn != self.player_color:
            return
        if self.confirm_dialog is not None and self.confirm_dialog.winfo_exists():
            self.confirm_dialog.lift()
            return
        side = lore.faction_name(self.game.turn)
        self.confirm_dialog = ConfirmDialog(
            self,
            "Doblar el estandarte",
            f"¿Abandonan las fuerzas de {side}? La crónica registrará la "
            "rendición y el rival reclamará el trono.",
            "Sí, abandonar",
            self._surrender,
            on_closed=self._clear_confirm_dialog,
        )

    def _clear_confirm_dialog(self) -> None:
        self.confirm_dialog = None

    def _surrender(self) -> None:
        if not self.started or self.game_over:
            return
        self._save_snapshot()
        loser = self.game.turn
        winner = self.game.next_active_color(loser)
        result = {
            "type": "surrender",
            "winner": winner,
            "loser": loser,
        }
        self.game_over = True
        self.result = result
        self.selected = None
        self.selected_moves = []
        entry = lore.epilogue(result)
        self.story.append(entry)
        self._append_story(entry)
        self.render()
        self._update_sidebar()
        self._update_buttons()
        self._update_status()
        self._cancel_end_timer()
        self.end_after = self.after(200, self._show_end_dialog)

    def _show_end_dialog(self) -> None:
        self.end_after = None
        if not self.started or not self.game_over or self.result is None:
            return
        if (
            self.crusade
            and self.crusade_state is not None
            and self.result.get("winner") == self.player_color
            and self.crusade_state.stage + 1 < self.crusade_state.total_stages
        ):
            lore.update_crusade_survivors(self.crusade_state, self.game)
            self.crusade_state.victories += 1
            if self.interlude_dialog is not None and self.interlude_dialog.winfo_exists():
                self.interlude_dialog.lift()
                return
            self.interlude_dialog = CrusadeInterludeDialog(
                self,
                self.crusade_state,
                self._on_crusade_boon,
                on_closed=self._clear_interlude_dialog,
            )
            return
        if self.end_dialog is not None and self.end_dialog.winfo_exists():
            self.end_dialog.lift()
            return
        self.end_dialog = EndDialog(
            self, self.result, self.game, self.start_time,
            on_new=self._end_new_game,
            on_closed=self._close_end_dialog,
        )

    def _clear_interlude_dialog(self) -> None:
        self.interlude_dialog = None

    def _on_crusade_boon(self, boon: str) -> None:
        if self.crusade_state is None:
            return
        boon_note = lore.apply_crusade_boon(self.crusade_state, boon)
        self.crusade_state.stage += 1
        self._launch_crusade_stage(boon_note=boon_note)

    def _end_new_game(self) -> None:
        self._close_end_dialog()
        if self.busy or self.ai_thinking:
            return
        self._open_setup()

    def _close_end_dialog(self) -> None:
        if self.end_dialog is not None:
            try:
                if self.end_dialog.winfo_exists():
                    self.end_dialog.destroy()
            except tk.TclError:
                pass
            self.end_dialog = None

    def _cancel_end_timer(self) -> None:
        if self.end_after is not None:
            try:
                self.after_cancel(self.end_after)
            except tk.TclError:
                pass
            self.end_after = None

    def _cancel_ai_start(self) -> None:
        if self.ai_start_after is not None:
            try:
                self.after_cancel(self.ai_start_after)
            except tk.TclError:
                pass
            self.ai_start_after = None

    def _key_undo(self, _event=None) -> None:
        if self._modal_open():
            return
        self.undo()

    def _key_flip(self, _event=None) -> None:
        if self._modal_open():
            return
        self._flip_board()

    def _key_escape(self, _event=None) -> None:
        if self._modal_open():
            return
        self._deselect()

    def _modal_open(self) -> bool:
        for dialog in (
            self.setup_dialog, self.end_dialog,
            self.promotion_dialog, self.confirm_dialog,
            self.dilemma_dialog, self.interlude_dialog,
        ):
            try:
                if dialog is not None and dialog.winfo_exists():
                    return True
            except tk.TclError:
                continue
        return False

    def _on_close(self) -> None:
        self._cancel_animation()
        self.destroy()

    # ------------------------------------------------------------------
    # Cursor y geometría
    # ------------------------------------------------------------------
    def _on_motion(self, event) -> None:
        if not self._human_can_move():
            self._set_cursor("")
            return
        square = self.board.square_at(event.x, event.y)
        cursor = ""
        if square is not None:
            r, c = square
            visible = self._visible_squares()
            if self.selected is not None and any(
                (m.tr, m.tc) == (r, c) for m in self.selected_moves
            ):
                cursor = "hand2"
            elif visible is not None and (r, c) not in visible:
                cursor = ""
            elif self.game.is_blocked(r, c):
                cursor = "X_cursor"
            else:
                piece = self.game.grid[r][c]
                if piece is not None and piece.color == self.game.turn:
                    cursor = "hand2"
        self._set_cursor(cursor)

    def _on_leave(self, _event) -> None:
        self._set_cursor("")

    def _set_cursor(self, cursor: str) -> None:
        if cursor != self._last_cursor:
            self.board.configure(cursor=cursor)
            self._last_cursor = cursor

    def _on_resize(self, _event) -> None:
        if self.anim is not None:
            self._complete_animation()
        if self._resize_after is not None:
            try:
                self.after_cancel(self._resize_after)
            except tk.TclError:
                pass
        self._resize_after = self.after(40, self._resize_render)

    def _resize_render(self) -> None:
        self._resize_after = None
        self.render()

    def render(self) -> None:
        self.board.render(
            self.game, self.selected, self.selected_moves, self.anim,
            visible=self._visible_squares(),
        )

    # ------------------------------------------------------------------
    # Actualización de vistas
    # ------------------------------------------------------------------
    def _view_state(self) -> ViewState:
        return ViewState(
            game=self.game,
            focus_piece=self.focus_piece,
            started=self.started,
            game_over=self.game_over,
            result=self.result,
            busy=self.busy,
            ai_thinking=self.ai_thinking,
            mode=self.mode,
            selected=self.selected,
            notation=self.notation,
            chapter=self.chapter,
        )

    def _update_sidebar(self) -> None:
        state = self._view_state()
        self.sidebar.update(state)
        self.status_bar.update(state)

    def _update_status(self) -> None:
        self.status_bar.update(self._view_state())

    def _update_buttons(self) -> None:
        undo_ready = (
            bool(self.snapshots) and not self.busy
            and not self.ai_thinking and self.started
        )
        self.undo_btn.configure(state="normal" if undo_ready else "disabled")
        new_ready = not self.busy and not self.ai_thinking
        self.new_btn.configure(state="normal" if new_ready else "disabled")
        self.flip_btn.configure(state="normal" if not self.busy else "disabled")
        surrender_ready = (
            self.started and not self.game_over and not self.busy
            and not self.ai_thinking
            and not (self.mode == "ai" and self.game.turn != self.player_color)
        )
        self.surrender_btn.configure(
            state="normal" if surrender_ready else "disabled",
        )

    def _update_character(self) -> None:
        self.sidebar.update_character(self.game, self.focus_piece)

    def _redraw_story(self) -> None:
        self.sidebar.story.redraw(self.story)

    def _append_story(self, entry) -> None:
        self.sidebar.story.append(entry)
