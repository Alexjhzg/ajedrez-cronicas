/**
 * Capa de Vistas y Modales DOM (UI Views).
 *
 * Responsabilidad única (SRP): manipular y actualizar el DOM de la interfaz
 * móvil (crónica, inspector de héroes/terrenos, códice y diálogos modales)
 * desacoplado de la lógica de control del juego.
 */

import {
  AMAZON,
  BISHOP,
  BLACK,
  ELEPHANT,
  FALCON,
  GREEN,
  KNIGHT,
  QUEEN,
  RED,
  ROOK,
  WHITE,
} from "../engine.js";
import * as lore from "../lore.js";
import { PIECE_GLYPHS } from "../board_renderer.js";

const TURN_CLASS = {
  [WHITE]: "turn-white",
  [BLACK]: "turn-black",
  [RED]: "turn-red",
  [GREEN]: "turn-green",
};

const GLYPH_CLASS = {
  [WHITE]: "glyph-white",
  [BLACK]: "glyph-black",
  [RED]: "glyph-red",
  [GREEN]: "glyph-green",
};

export function initDialogsLightDismiss() {
  // Fallback obligatorio para navegadores sin soporte nativo de <dialog closedby="any">
  document.querySelectorAll('dialog[closedby="any"]').forEach((dialog) => {
    if (!("closedBy" in HTMLDialogElement.prototype)) {
      dialog.addEventListener("click", (event) => {
        if (event.target !== dialog) return;
        const rect = dialog.getBoundingClientRect();
        const isDialogContent =
          rect.top <= event.clientY &&
          event.clientY <= rect.top + rect.height &&
          rect.left <= event.clientX &&
          event.clientX <= rect.left + rect.width;
        if (isDialogContent) return;
        dialog.close();
      });
    }
  });
}

export function switchTabView(tabName) {
  document.querySelectorAll(".tab-btn").forEach((b) => {
    b.classList.toggle("active", b.dataset.tab === tabName);
  });
  document.querySelectorAll(".tab-panel").forEach((p) => {
    p.classList.toggle("active", p.id === `panel-${tabName}`);
  });
}

export function refreshSetupView({
  mode,
  difficulty,
  campaignKey,
  playerColor = WHITE,
  elephant,
  fog,
  isPremium,
}) {
  document.querySelectorAll("[data-setup-faction]").forEach((btn) => {
    btn.classList.toggle("selected", btn.dataset.setupFaction === playerColor);
  });
  const facDesc = document.getElementById("setupFactionDesc");
  if (facDesc) {
    const f = lore.FACTIONS[playerColor] || lore.FACTIONS[WHITE];
    facDesc.textContent = `${f.name} (${f.culture}) · Soberanos: ${f.sovereigns}. ${f.lore || f.motto || ""}`;
  }

  document.querySelectorAll("[data-setup-mode]").forEach((btn) => {
    btn.classList.toggle("selected", btn.dataset.setupMode === mode);
  });
  document.querySelectorAll("[data-setup-diff]").forEach((btn) => {
    btn.classList.toggle("selected", btn.dataset.setupDiff === difficulty);
  });
  document.querySelectorAll("[data-setup-campaign]").forEach((btn) => {
    btn.classList.toggle("selected", btn.dataset.setupCampaign === campaignKey);
  });

  const campDesc = document.getElementById("setupCampaignDesc");
  if (campaignKey === "crusade") {
    campDesc.textContent = isPremium
      ? "Cuatro batallas encadenadas contra los otros tres reinos rumbo al Trono. Tus sobrevivientes y su veteranía persisten entre etapas."
      : "Cuatro batallas encadenadas contra los reinos rivales. (Etapas I y II gratuitas; Etapas III y IV en Códice Completo).";
  } else if (campaignKey === "imperial") {
    campDesc.textContent =
      "Gran Tablero Imperial 12x12 con las 10 nuevas piezas míticas (Halcón, Elefante, Amazonas, Saltamontes, Noctámbulo, Centauro, Camello, León, Cebra y Fénix).";
  } else if (campaignKey === "four_fronts") {
    campDesc.textContent =
      "Batalla simultánea de los 4 reinos (Sur, Oeste, Norte y Este) en un mismo tablero. Cuando cae un Rey, su frente entero se desmorona.";
  } else if (campaignKey === "wild") {
    campDesc.textContent =
      "Ejércitos aleatorios con campeones míticos y terreno táctico (bosques, ríos, ruinas y peñascos) con dilemas interactivos cada 6 jugadas.";
  } else {
    campDesc.textContent =
      "Formación tradicional con héroes con nombre y ascenso al rango de Veterano al conseguir 2 bajas.";
  }

  const eleBtn = document.getElementById("toggleElephant");
  eleBtn.classList.toggle("selected", elephant);
  eleBtn.textContent = isPremium
    ? `Elefante de guerra (⛨): ${elephant ? "ACTIVO" : "NO"}`
    : "Elefante de guerra (⛨) · [CÓDICE COMPLETO]";

  const fogBtn = document.getElementById("toggleFog");
  fogBtn.classList.toggle("selected", fog);
  fogBtn.textContent = `Niebla de guerra: ${fog ? "ACTIVA" : "NO"}`;
}

export function openPromotionModal(matchingMoves, onSelectMove) {
  const dlg = document.getElementById("promotionDialog");
  const container = document.getElementById("promotionOptions");
  container.innerHTML = "";
  for (const kind of [AMAZON, QUEEN, ELEPHANT, FALCON, ROOK, BISHOP, KNIGHT]) {
    const move = matchingMoves.find((m) => m.promotion === kind);
    if (!move) continue;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "choice-card";
    btn.innerHTML = `
      <span class="choice-glyph">${PIECE_GLYPHS[kind]}</span>
      <div>
        <div class="choice-title">${lore.PROMOTED_TITLE[kind]}</div>
        <div class="choice-desc">Renace como ${lore.PROMOTION_ROLE[kind]}</div>
      </div>
    `;
    btn.addEventListener("click", () => {
      dlg.close();
      onSelectMove(move);
    });
    container.appendChild(btn);
  }
  dlg.showModal();
}

export function openDilemmaModal(dilemma, onChooseOption) {
  const dlg = document.getElementById("dilemmaDialog");
  document.getElementById("dilemmaTitle").textContent = dilemma.title;
  document.getElementById("dilemmaPrompt").textContent = dilemma.prompt;
  const container = document.getElementById("dilemmaOptions");
  container.innerHTML = "";

  dilemma.options.forEach((choice, idx) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "choice-card";
    btn.innerHTML = `
      <div>
        <div class="choice-kicker">OPCIÓN ${idx + 1}</div>
        <div class="choice-title">${choice.label}</div>
        <div class="choice-desc">${choice.description}</div>
      </div>
    `;
    btn.addEventListener("click", () => {
      dlg.close();
      onChooseOption(choice);
    });
    container.appendChild(btn);
  });
  dlg.showModal();
}

export function openCrusadeInterludeModal(crusadeState, onSelectBoon) {
  const dlg = document.getElementById("interludeDialog");
  const survivors = crusadeState.roster.length;
  const vets = crusadeState.roster.filter((p) => p.veteran).length;
  const nextStage = lore.CRUSADE_STAGES[crusadeState.stage + 1][1];
  const pName = lore.factionName(crusadeState.player_color || WHITE);

  document.getElementById("interludeSummary").textContent =
    `Sobrevivientes de ${pName}: ${survivors} unidades (${vets} veteranos). Próximo destino: ${nextStage}.`;

  const container = document.getElementById("interludeBoons");
  container.innerHTML = "";
  const boons = [
    {
      id: "mythic",
      title: "Invocar Campeón Mítico",
      desc: "Recluta una unidad legendaria (Halcón, Elefante, Centauro, Fénix, León, Noctámbulo, Camello, Cebra o Saltamontes).",
    },
    {
      id: "veteran",
      title: "Consagrar Veteranos (★)",
      desc: "Asciende inmediatamente a 2 unidades de tu ejército al rango de Veterano.",
    },
    {
      id: "squires",
      title: "Leva de Vanguardia",
      desc: "Recluta hasta 3 nuevas unidades ligeras para reponer las bajas de la línea frontal.",
    },
  ];

  boons.forEach((b) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "choice-card";
    btn.innerHTML = `
      <div>
        <div class="choice-title">${b.title}</div>
        <div class="choice-desc">${b.desc}</div>
      </div>
    `;
    btn.addEventListener("click", () => {
      dlg.close();
      onSelectBoon(b.id);
    });
    container.appendChild(btn);
  });
  dlg.showModal();
}

export function openEndModal({
  result,
  game,
  isCrusadeComplete,
  canOracleRetry,
  isPremium,
}) {
  const [title, subtitle] = lore.resultTitle(result);
  document.getElementById("endIcon").textContent = lore.resultIcon(result);
  document.getElementById("endTitle").textContent = isCrusadeComplete
    ? "CRUZADA COMPLETADA"
    : title;
  document.getElementById("endSubtitle").textContent = isCrusadeComplete
    ? "Has conquistado las cuatro etapas y recuperado el Trono de Aethelgard"
    : subtitle;
  document.getElementById("endEpilogue").textContent = lore.epilogue(result).text;
  document.getElementById("endStatMoves").textContent = String(
    Math.ceil(game.history.length / 2)
  );
  document.getElementById("endStatCaptures").textContent = String(
    game.capturedPieces().length
  );

  const oracleBtn = document.getElementById("btnOracleRetry");
  if (canOracleRetry) {
    oracleBtn.hidden = false;
    oracleBtn.textContent = isPremium
      ? "Reintentar Etapa (Códice Completo)"
      : "Pacto del Oráculo · Reintentar Etapa (Ver Anuncio)";
  } else {
    oracleBtn.hidden = true;
  }

  const dlg = document.getElementById("endDialog");
  if (!dlg.open) dlg.showModal();
}

export function renderStoryView(story, notation) {
  const latest = story[story.length - 1];
  if (latest) {
    document.getElementById("tickerHeading").textContent = latest.heading;
    document.getElementById("tickerText").textContent = latest.text.replace(/\n+/g, " ");
  }

  const log = document.getElementById("storyLog");
  log.innerHTML = "";
  story
    .slice()
    .reverse()
    .forEach((entry) => {
      const item = document.createElement("article");
      item.className = `story-entry tag-${entry.tag}`;
      item.innerHTML = `
        <div class="story-heading">${entry.heading}</div>
        <div class="story-body">${entry.text.replace(/\n/g, "<br>")}</div>
      `;
      log.appendChild(item);
    });

  const movesBox = document.getElementById("notationList");
  movesBox.innerHTML = "";
  for (let i = 0; i < notation.length; i += 2) {
    const chip = document.createElement("span");
    chip.className = "move-chip";
    const w = notation[i] || "";
    const b = notation[i + 1] || "";
    chip.textContent = `${i / 2 + 1}. ${w}${b ? " " + b : ""}`;
    movesBox.appendChild(chip);
  }
}

export function renderHudView({
  game,
  gameOver,
  aiThinking,
  focusPiece,
  inspectedTerrain,
}) {
  const turnBadge = document.getElementById("turnBadge");
  const activeFaction = lore.FACTIONS[game.turn] || lore.FACTIONS[WHITE];
  const turnClass = TURN_CLASS[game.turn] || "turn-white";
  if (gameOver) {
    turnBadge.textContent = "Crónica concluida";
    turnBadge.className = "turn-badge";
  } else if (aiThinking) {
    turnBadge.textContent = `${activeFaction.crest} ${activeFaction.name} medita...`;
    turnBadge.className = `turn-badge ${turnClass}`;
  } else {
    turnBadge.textContent = `${activeFaction.crest} Turno de ${activeFaction.short}`;
    turnBadge.className = `turn-badge ${turnClass}`;
  }

  if (focusPiece) {
    document.getElementById("heroGlyph").textContent =
      PIECE_GLYPHS[focusPiece.kind] || "♟";
    const glyphClass = GLYPH_CLASS[focusPiece.color] || "glyph-white";
    document.getElementById("heroGlyph").className =
      `hero-glyph ${glyphClass}`;
    document.getElementById("heroName").textContent =
      `${focusPiece.veteran ? "★ " : ""}${focusPiece.name}`;
    document.getElementById("heroTitle").textContent =
      `${focusPiece.title}${focusPiece.veteran ? " · Veterano" : ""}`;

    const pos = lore.pieceOnBoard(game, focusPiece);
    document.getElementById("heroStatus").textContent = pos
      ? `En ${lore.locationLabel(pos[0], pos[1], game.size)} · Bajas: ${focusPiece.kills}`
      : `Caído en combate · Bajas logradas: ${focusPiece.kills}`;
    document.getElementById("heroBio").textContent = lore.characterBio(focusPiece);
  }

  const terrainBox = document.getElementById("terrainInspector");
  if (inspectedTerrain) {
    const { kind, r, c } = inspectedTerrain;
    terrainBox.hidden = false;
    document.getElementById("terrainTitle").textContent =
      `Terreno: ${lore.TERRAIN_LABEL[kind]} (${lore.locationLabel(r, c, game.size)})`;
    document.getElementById("terrainDesc").textContent =
      lore.TERRAIN_CONSEQUENCE[kind];
  } else {
    terrainBox.hidden = true;
  }
}

export function renderCodexView(storeData, isPremium) {
  const badge = document.getElementById("btnPremiumBadge");
  badge.textContent = isPremium ? "CÓDICE COMPLETO" : "EDICIÓN GRATUITA";
  badge.classList.toggle("premium-active", isPremium);

  document.getElementById("codexGames").textContent = String(storeData.gamesPlayed);
  document.getElementById("codexDawnWins").textContent = String(storeData.dawnVictories);
  document.getElementById("codexCrusades").textContent = String(storeData.crusadesWon);
  document.getElementById("codexVeterans").textContent = String(storeData.veteransForged);

  const statusBanner = document.getElementById("codexLicenseStatus");
  statusBanner.textContent = isPremium
    ? "Licencia activa: Códice Completo de Aethelgard desbloqueado (Cruzada completa, Elefante de Guerra y sin anuncios)."
    : "Edición Gratuita (Free-to-Try): Etapas I y II de la Cruzada activas. Desbloquea el Códice Completo por $2.99 USD.";

  const toggleBtn = document.getElementById("btnToggleFreeTest");
  toggleBtn.textContent = isPremium
    ? "Modo Desarrollador: Cambiar a Edición Gratuita para probar bloqueos"
    : "Modo Desarrollador: Simular Códice Completo activo";

  const fallenList = document.getElementById("fallenMemorial");
  fallenList.innerHTML = "";
  if (storeData.fallenHeroes.length === 0) {
    fallenList.innerHTML = `<div class="muted-note">Ningún héroe del Alba ha caído aún en tus crónicas.</div>`;
  } else {
    storeData.fallenHeroes.slice(0, 6).forEach((h) => {
      const row = document.createElement("div");
      row.className = "fallen-row";
      row.textContent = `${h.veteran ? "★ " : ""}${h.name} (${h.title}) — Caído en ${h.location}`;
      fallenList.appendChild(row);
    });
  }
}
