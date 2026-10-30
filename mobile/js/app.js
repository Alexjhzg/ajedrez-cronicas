/**
 * Controlador Principal de la Aplicación Móvil (Crónicas de Aethelgard).
 *
 * Responsabilidad única (SRP): coordinar el estado de la partida, el ciclo de
 * turnos (jugador / IA), animaciones y persistencia, delegando la manipulación
 * del DOM a `ui/views.js`.
 */

import {
  BLACK,
  ELEPHANT,
  KING,
  ROOK,
  WHITE,
  createPiece,
  findBestMove,
  moveNotation,
  other,
} from "./engine.js";
import * as lore from "./lore.js";
import { BoardRenderer, durationFor } from "./board_renderer.js";
import { SoundEngine } from "./audio.js";
import { CodexStore } from "./store.js";
import {
  initDialogsLightDismiss,
  openCrusadeInterludeModal,
  openDilemmaModal,
  openEndModal,
  openPromotionModal,
  refreshSetupView,
  renderCodexView,
  renderHudView,
  renderStoryView,
  switchTabView,
} from "./ui/views.js";

const DIFFICULTIES = {
  Escudero: { depth: 1, randomness: 0.45, timeMs: 600 },
  Caballero: { depth: 2, randomness: 0.12, timeMs: 1100 },
  Archimago: { depth: 3, randomness: 0.0, timeMs: 1800 },
};

class MobileChroniclesApp {
  constructor() {
    this.canvas = document.getElementById("boardCanvas");
    this.board = new BoardRenderer(this.canvas);
    this.sound = new SoundEngine();
    this.store = new CodexStore();

    this.mode = "ai";
    this.difficulty = "Caballero";
    this.campaignKey = "crusade"; // "classic" | "wild" | "crusade" | "four_fronts"
    this.playerColor = WHITE;
    this.wild = true;
    this.crusade = true;
    this.elephant = false;
    this.fog = false;

    this.game = lore.createGame();
    this.scenario = null;
    this.crusadeState = null;

    this.selected = null;
    this.selectedMoves = [];
    this.focusPiece = this.findPieceByKind(WHITE, KING);
    this.inspectedTerrain = null;

    this.chapter = 0;
    this.ply = 0;
    this.story = [];
    this.notation = [];
    this.snapshots = [];

    this.started = false;
    this.gameOver = false;
    this.result = null;
    this.busy = false;
    this.aiThinking = false;
    this.anim = null;
    this.pendingDilemma = null;

    initDialogsLightDismiss();
    this._bindEvents();
    this.updateCodexView();
    this.openSetupDialog();
  }

  _bindEvents() {
    window.addEventListener("resize", () => this.render());

    this.canvas.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      this.onBoardPointer(e.clientX, e.clientY);
    });

    document.getElementById("btnNewGame").addEventListener("click", () => {
      this.sound.playSelect();
      this.openSetupDialog();
    });
    document.getElementById("btnUndo").addEventListener("click", () => {
      this.sound.playSelect();
      this.undoMove();
    });
    document.getElementById("btnFlip").addEventListener("click", () => {
      this.sound.playSelect();
      this.board.toggleFlip();
      this.render();
    });
    document.getElementById("btnSurrender").addEventListener("click", () => {
      this.sound.playSelect();
      this.surrender();
    });
    document.getElementById("btnSound").addEventListener("click", () => {
      this.sound.enabled = !this.sound.enabled;
      const btn = document.getElementById("btnSound");
      btn.textContent = this.sound.enabled ? "SONIDO: SÍ" : "SONIDO: NO";
      btn.classList.toggle("active-pill", this.sound.enabled);
    });
    document.getElementById("btnPremiumBadge").addEventListener("click", () => {
      this.sound.playSelect();
      this.openPremiumDialog();
    });

    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.sound.playSelect();
        switchTabView(btn.dataset.tab);
      });
    });

    document.querySelectorAll("[data-setup-mode]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.sound.playSelect();
        this.mode = btn.dataset.setupMode;
        if (this.crusade && this.mode !== "ai") {
          this.campaignKey = "wild";
          this.crusade = false;
        }
        this._refreshSetupUI();
      });
    });

    document.querySelectorAll("[data-setup-diff]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.sound.playSelect();
        this.difficulty = btn.dataset.setupDiff;
        this._refreshSetupUI();
      });
    });

    document.querySelectorAll("[data-setup-faction]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.sound.playSelect();
        this.playerColor = btn.dataset.setupFaction;
        this._refreshSetupUI();
      });
    });

    document.querySelectorAll("[data-setup-campaign]").forEach((btn) => {
      btn.addEventListener("click", () => {
        this.sound.playSelect();
        this.campaignKey = btn.dataset.setupCampaign;
        this.crusade = this.campaignKey === "crusade";
        this.wild = this.campaignKey === "wild" || this.campaignKey === "crusade";
        if (this.crusade) this.mode = "ai";
        this._refreshSetupUI();
      });
    });

    document.getElementById("toggleElephant").addEventListener("click", () => {
      this.sound.playSelect();
      if (!this.store.isPremium() && !this.elephant) {
        this.openPremiumDialog();
        return;
      }
      this.elephant = !this.elephant;
      this._refreshSetupUI();
    });

    document.getElementById("toggleFog").addEventListener("click", () => {
      this.sound.playSelect();
      this.fog = !this.fog;
      this._refreshSetupUI();
    });

    document.getElementById("btnStartChronicle").addEventListener("click", () => {
      this.sound.playMove(true);
      document.getElementById("setupDialog").close();
      this.startNewGame();
    });

    document.getElementById("btnEndReview").addEventListener("click", () => {
      document.getElementById("endDialog").close();
    });
    document.getElementById("btnEndNew").addEventListener("click", () => {
      document.getElementById("endDialog").close();
      this.openSetupDialog();
    });
    document.getElementById("btnOracleRetry").addEventListener("click", async () => {
      const btn = document.getElementById("btnOracleRetry");
      if (this.store.isPremium()) {
        document.getElementById("endDialog").close();
        this.launchCrusadeStage("El Códice Completo restaura tu columna en esta etapa.");
        return;
      }
      btn.disabled = true;
      await this.store.watchRewardedOraclePact((sec) => {
        btn.textContent = `Consultando al Oráculo (${sec}s)...`;
      });
      btn.disabled = false;
      document.getElementById("endDialog").close();
      this.updateCodexView();
      this.launchCrusadeStage("El Pacto del Oráculo concede una segunda oportunidad a tu ejército.");
    });

    document.getElementById("btnBuyPremium").addEventListener("click", async () => {
      const btn = document.getElementById("btnBuyPremium");
      btn.disabled = true;
      btn.textContent = "Procesando desbloqueo...";
      await this.store.purchasePremiumCodex();
      btn.disabled = false;
      this.sound.playVeteranFanfare();
      this.updateCodexView();
      this._refreshSetupUI();
      document.getElementById("premiumDialog").close();
    });

    document.getElementById("btnToggleFreeTest").addEventListener("click", () => {
      this.store.setPremium(!this.store.isPremium());
      if (!this.store.isPremium()) {
        this.elephant = false;
      }
      this.updateCodexView();
      this._refreshSetupUI();
    });
  }

  openSetupDialog() {
    this._refreshSetupUI();
    const dlg = document.getElementById("setupDialog");
    if (!dlg.open) dlg.showModal();
  }

  openPremiumDialog() {
    const dlg = document.getElementById("premiumDialog");
    if (!dlg.open) dlg.showModal();
  }

  _refreshSetupUI() {
    refreshSetupView({
      mode: this.mode,
      difficulty: this.difficulty,
      campaignKey: this.campaignKey,
      playerColor: this.playerColor,
      elephant: this.elephant,
      fog: this.fog,
      isPremium: this.store.isPremium(),
    });
  }

  findPieceByKind(color, kind) {
    const n = this.game.size || 8;
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const p = this.game.grid[r][c];
        if (p && p.color === color && p.kind === kind) return p;
      }
    }
    return null;
  }

  startNewGame() {
    this.wild = this.campaignKey === "wild" || this.campaignKey === "crusade";
    this.crusade = this.campaignKey === "crusade";
    if (this.crusade) this.mode = "ai";

    this.board.resetFlip();
    this.started = true;
    this.gameOver = false;
    this.result = null;
    this.selected = null;
    this.selectedMoves = [];
    this.inspectedTerrain = null;
    this.snapshots = [];
    this.story = [];
    this.notation = [];
    this.chapter = 0;
    this.ply = 0;
    this.busy = false;
    this.aiThinking = false;
    this.anim = null;

    if (this.crusade) {
      this.crusadeState = lore.createCrusade(this.elephant, this.playerColor);
      this.launchCrusadeStage();
      return;
    }

    this.crusadeState = null;
    const rivals = lore.rivalFactions(this.playerColor);
    const enemyColor = rivals[0] || BLACK;
    let intro;
    if (this.campaignKey === "imperial") {
      this.scenario = null;
      this.game = lore.createImperialGame(this.playerColor, enemyColor);
      this.board.setScene("imperial");
      document.getElementById("campaignSubtitle").textContent =
        `Imperio 12x12 · ${lore.factionName(this.playerColor)} vs ${lore.factionName(enemyColor)}`;
      intro = lore.imperialPrologue(
        this.mode === "ai",
        this.difficulty,
        this.fog,
        this.playerColor,
        enemyColor
      );
    } else if (this.campaignKey === "four_fronts") {
      this.scenario = null;
      this.game = lore.createFourFrontsGame(this.elephant, this.playerColor);
      this.board.setScene("ruinas");
      document.getElementById("campaignSubtitle").textContent =
        `Guerra de 4 Frentes · ${lore.factionName(this.playerColor)}`;
      intro = lore.fourFrontsPrologue(
        this.mode === "ai",
        this.difficulty,
        this.elephant,
        this.fog,
        this.playerColor
      );
    } else if (this.wild) {
      const scenario = lore.createWildScenario(
        this.elephant,
        this.playerColor,
        enemyColor
      );
      this.scenario = scenario;
      this.game = scenario.game;
      this.board.setScene(scenario.theme);
      document.getElementById("campaignSubtitle").textContent = `Tierra Salvaje · ${scenario.title}`;
      intro = lore.wildPrologue(scenario, this.mode === "ai", this.difficulty, this.fog);
    } else {
      this.scenario = null;
      this.game = lore.createGame(this.elephant, this.playerColor, enemyColor);
      this.board.setScene("classic");
      document.getElementById("campaignSubtitle").textContent =
        `Crónica Clásica · ${lore.factionName(this.playerColor)} vs ${lore.factionName(enemyColor)}`;
      intro = lore.prologue(
        this.mode === "ai",
        this.difficulty,
        this.elephant,
        this.fog,
        this.playerColor,
        enemyColor
      );
    }

    this.focusPiece = this.findPieceByKind(this.playerColor, KING);
    this.story = [intro];
    this.renderStory();
    this.render();
    this.updateHUD();
  }

  launchCrusadeStage(boonNote = "") {
    if (!this.crusadeState) return;
    const [scenario, stageDiff] = lore.createCrusadeStage(this.crusadeState, this.elephant);
    this.scenario = scenario;
    this.difficulty = stageDiff;
    this.game = scenario.game;
    this.board.setScene(scenario.theme);
    this.gameOver = false;
    this.result = null;
    this.selected = null;
    this.selectedMoves = [];
    this.inspectedTerrain = null;
    this.snapshots = [];
    this.notation = [];
    this.chapter = 0;
    this.ply = 0;

    document.getElementById("campaignSubtitle").textContent =
      `Cruzada (${this.crusadeState.stage + 1}/${this.crusadeState.total_stages}) · ${scenario.title}`;

    const intro = lore.wildPrologue(scenario, true, stageDiff, this.fog);
    if (boonNote) {
      intro.text = `${boonNote}\n\n${intro.text}`;
    }
    this.story = [intro];
    this.focusPiece = this.findPieceByKind(this.playerColor, KING);
    this.renderStory();
    this.render();
    this.updateHUD();
  }

  visibleSquares() {
    if (!this.fog) return null;
    const viewer = this.mode === "ai" ? this.playerColor : this.game.turn;
    return this.game.visibleSquares(viewer);
  }

  onBoardPointer(clientX, clientY) {
    if (!this.started || this.gameOver || this.busy || this.aiThinking) return;
    if (this.mode === "ai" && this.game.turn !== this.playerColor) return;

    const sq = this.board.squareAt(clientX, clientY);
    if (!sq) return;
    const [r, c] = sq;
    const visible = this.visibleSquares();
    const isVisible = !visible || visible.has(`${r},${c}`);

    if (this.selected) {
      const matching = this.selectedMoves.filter((m) => m.tr === r && m.tc === c);
      if (matching.length > 0) {
        this.executeCandidateMoves(matching);
        return;
      }
    }

    const piece = isVisible ? this.game.pieceAt(r, c) : null;
    const terrain = isVisible ? this.game.terrainAt(r, c) : null;

    if (piece) {
      this.focusPiece = piece;
      this.inspectedTerrain = terrain ? { kind: terrain, r, c } : null;
      if (piece.color === this.game.turn) {
        this.sound.playSelect();
        this.selected = [r, c];
        this.selectedMoves = this.game.legalMovesFrom(r, c);
      } else {
        this.selected = null;
        this.selectedMoves = [];
      }
    } else {
      this.selected = null;
      this.selectedMoves = [];
      if (terrain) {
        this.sound.playSelect();
        this.inspectedTerrain = { kind: terrain, r, c };
      }
    }

    this.render();
    this.updateHUD();
  }

  executeCandidateMoves(matching) {
    if (matching.length === 1 && !matching[0].promotion) {
      this.performMove(matching[0]);
      return;
    }
    openPromotionModal(matching, (move) => this.performMove(move));
  }

  saveSnapshot() {
    this.snapshots.push({
      game: this.game.clone(),
      focusPiece: this.focusPiece,
      chapter: this.chapter,
      ply: this.ply,
      story: this.story.map((e) => ({ ...e })),
      notation: [...this.notation],
    });
  }

  undoMove() {
    if (!this.started || this.busy || this.aiThinking || this.snapshots.length === 0) return;
    let steps = 1;
    if (this.mode === "ai" && this.game.turn === this.playerColor) {
      steps = Math.min(this.game.turn_order.length, this.snapshots.length);
    }
    let snap = null;
    for (let i = 0; i < steps; i++) {
      snap = this.snapshots.pop();
    }
    if (!snap) return;
    this.game = snap.game;
    this.focusPiece = snap.focusPiece;
    this.chapter = snap.chapter;
    this.ply = snap.ply;
    this.story = snap.story;
    this.notation = snap.notation;
    this.gameOver = false;
    this.result = null;
    this.selected = null;
    this.selectedMoves = [];
    this.renderStory();
    this.render();
    this.updateHUD();
  }

  surrender() {
    if (!this.started || this.gameOver || this.busy) return;
    const loser = this.mode === "ai" ? this.playerColor : this.game.turn;
    const winner = other(loser, this.game.turn_order);
    this.result = { type: "surrender", winner, loser };
    this.gameOver = true;
    this.story.push(lore.epilogue(this.result));
    this.renderStory();
    this.updateHUD();
    this.showEndDialog();
  }

  performMove(move, wasAi = false) {
    if (!this.started || this.gameOver) return;
    this.saveSnapshot();
    this.selected = null;
    this.selectedMoves = [];

    const preVis = this.visibleSquares();
    this.game.applyMove(move);
    if (move.promotion && move.placed) {
      const placed = this.game.grid[move.tr][move.tc];
      if (placed) {
        const promoPool = (lore.NAME_POOLS[placed.color] || lore.NAME_POOLS[WHITE])[move.promotion];
        const promoName = promoPool ? promoPool[0] : placed.name;
        const promoted = createPiece(
          placed.color,
          placed.kind,
          placed.pid,
          promoName,
          lore.PROMOTED_TITLE[move.promotion],
          placed.kills,
          placed.veteran
        );
        this.game.grid[move.tr][move.tc] = promoted;
        move.placed = promoted;
      }
    }

    const postVis = this.visibleSquares();
    const moveHidden =
      wasAi &&
      this.fog &&
      move.captured === null &&
      preVis &&
      postVis &&
      !preVis.has(`${move.fr},${move.fc}`) &&
      !postVis.has(`${move.tr},${move.tc}`);

    const activePiece = move.placed || move.moved;
    if (!moveHidden && activePiece) {
      this.focusPiece = activePiece;
    }

    const becameVeteran =
      move.placed && move.placed.veteran && move.moved && !move.moved.veteran;
    if (becameVeteran && activePiece && activePiece.color === this.playerColor) {
      this.store.recordVeteranAscension();
    }
    if (move.captured && move.captured.color === this.playerColor) {
      this.store.recordFallenHero(move.captured, lore.squareName(move.tr, move.tc, this.game.size));
    }

    this.ply += 1;
    this.chapter += 1;

    const preResult = this.game.result();
    let wildEntry = null;
    this.pendingDilemma = null;
    if (
      this.wild &&
      this.scenario &&
      !preResult &&
      this.chapter % lore.WILD_EVENT_EVERY === 0
    ) {
      if (!wasAi) {
        this.pendingDilemma = lore.wildDilemma(this.game, this.scenario);
      }
      if (!this.pendingDilemma) {
        wildEntry = lore.wildEvent(this.game, this.scenario);
      }
    }

    const result = this.game.result();
    const check = this.game.inCheck(this.game.turn);
    const mate = Boolean(result && result.type === "checkmate");

    this.notation.push(moveHidden ? "?" : moveNotation(move, check, mate, this.game.size));

    const entry = moveHidden
      ? lore.fogEntry(this.chapter)
      : lore.narrateMove(move, this.game, check, mate, this.chapter);
    this.story.push(entry);
    if (wildEntry) this.story.push(wildEntry);

    if (result) {
      this.gameOver = true;
      this.result = result;
      this.story.push(lore.epilogue(result));
    }

    if (check || mate) {
      this.sound.playCheck();
    } else if (move.captured) {
      this.sound.playCapture(becameVeteran);
    } else {
      this.sound.playMove([ROOK, ELEPHANT].includes(activePiece.kind));
    }

    this.renderStory();
    this.updateCodexView();

    if (moveHidden) {
      this.render();
      this.updateHUD();
      this.afterMoveCompleted(result);
      return;
    }

    this.beginAnimation(move, result);
  }

  beginAnimation(move, result) {
    this.busy = true;
    const piece = move.placed || move.moved;
    const duration = durationFor(piece.kind);
    const startTime = performance.now();
    const [fdr, fdc] = this.game.front_dirs[piece.color] || [-1, 0];
    const captureSq = move.captured
      ? move.is_en_passant
        ? [move.tr - fdr, move.tc - fdc]
        : [move.tr, move.tc]
      : null;

    let push = [0, -1];
    if (captureSq) {
      const dx = move.tr - move.fr;
      const dy = move.tc - move.fc;
      const len = Math.hypot(dy, dx) || 1;
      push = [dy / len, dx / len];
    }

    const step = (now) => {
      const t = Math.min(1, (now - startTime) / duration);
      this.anim = {
        piece,
        t,
        fromSq: [move.fr, move.fc],
        toSq: [move.tr, move.tc],
        captureSq,
        victim: move.captured,
        push,
      };
      this.render();
      if (t < 1) {
        requestAnimationFrame(step);
      } else {
        this.anim = null;
        this.busy = false;
        this.render();
        this.updateHUD();
        this.afterMoveCompleted(result);
      }
    };
    requestAnimationFrame(step);
  }

  afterMoveCompleted(result) {
    if (this.pendingDilemma && !result) {
      const dilemma = this.pendingDilemma;
      this.pendingDilemma = null;
      this.openDilemmaDialog(dilemma);
      return;
    }

    if (result) {
      setTimeout(() => this.showEndDialog(), 280);
      return;
    }

    if (this.mode === "ai" && this.game.turn !== this.playerColor) {
      this.aiThinking = true;
      this.updateHUD();
      setTimeout(() => this.runAiTurn(), 220);
    }
  }

  runAiTurn() {
    if (!this.started || this.gameOver || this.game.turn === this.playerColor) {
      this.aiThinking = false;
      return;
    }
    const cfg = DIFFICULTIES[this.difficulty] || DIFFICULTIES.Caballero;
    const move = findBestMove(this.game, cfg.depth, cfg.randomness, cfg.timeMs);
    this.aiThinking = false;
    if (!move) {
      const res = this.game.result();
      if (res) {
        this.gameOver = true;
        this.result = res;
        this.showEndDialog();
      }
      return;
    }
    this.performMove(move, true);
  }

  openDilemmaDialog(dilemma) {
    openDilemmaModal(dilemma, (choice) => {
      this.sound.playMove(true);
      const entry = lore.applyWildChoice(this.game, choice);
      if (entry) {
        this.story.push(entry);
        this.renderStory();
      }
      const res = this.game.result();
      if (res) {
        this.gameOver = true;
        this.result = res;
        this.story.push(lore.epilogue(res));
        this.renderStory();
      }
      this.render();
      this.updateHUD();
      this.afterMoveCompleted(res);
    });
  }

  showEndDialog() {
    if (!this.result) return;
    const winner = this.result.winner;

    if (
      this.crusade &&
      this.crusadeState &&
      winner === this.playerColor &&
      this.crusadeState.stage + 1 < this.crusadeState.total_stages
    ) {
      this.sound.playVictory(true);
      lore.updateCrusadeSurvivors(this.crusadeState, this.game);
      this.crusadeState.victories += 1;

      if (this.crusadeState.stage + 1 >= 2 && !this.store.isPremium()) {
        this.openPremiumDialog();
        return;
      }

      openCrusadeInterludeModal(this.crusadeState, (boonId) => {
        this.sound.playVeteranFanfare();
        const note = lore.applyCrusadeBoon(this.crusadeState, boonId);
        this.crusadeState.stage += 1;
        this.launchCrusadeStage(note);
      });
      return;
    }

    const isCrusadeComplete = Boolean(
      this.crusade && this.crusadeState && winner === this.playerColor
    );
    this.store.recordGameEnd(winner, isCrusadeComplete);
    this.updateCodexView();
    this.sound.playVictory(winner === this.playerColor);

    openEndModal({
      result: this.result,
      game: this.game,
      isCrusadeComplete,
      canOracleRetry: Boolean(this.crusade && this.crusadeState && winner !== this.playerColor),
      isPremium: this.store.isPremium(),
    });
  }

  render() {
    this.board.render(
      this.game,
      this.selected,
      this.selectedMoves,
      this.anim,
      this.visibleSquares()
    );
  }

  renderStory() {
    renderStoryView(this.story, this.notation);
  }

  updateHUD() {
    renderHudView({
      game: this.game,
      gameOver: this.gameOver,
      aiThinking: this.aiThinking,
      focusPiece: this.focusPiece,
      inspectedTerrain: this.inspectedTerrain,
    });
  }

  updateCodexView() {
    renderCodexView(this.store.data, this.store.isPremium());
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.cronicasApp = new MobileChroniclesApp();
});
