/**
 * Persistencia, Códice de Metaprogresión y Ganchos de Monetización
 * Preparado para conectar con @revenuecat/purchases-capacitor y @capacitor-community/admob
 */

const STORAGE_KEY = "cronicas_aethelgard_codex_v1";

const DEFAULT_DATA = {
  premiumUnlocked: false,
  gamesPlayed: 0,
  dawnVictories: 0,
  eclipseVictories: 0,
  crusadesWon: 0,
  veteransForged: 0,
  fallenHeroes: [],
  oraclePactsUsed: 0,
};

export class CodexStore {
  constructor() {
    this.data = this._load();
  }

  _load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return { ...DEFAULT_DATA };
      const parsed = JSON.parse(raw);
      return { ...DEFAULT_DATA, ...parsed };
    } catch (_e) {
      return { ...DEFAULT_DATA };
    }
  }

  save() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.data));
    } catch (_e) {
      // Ignorar si almacenamiento privado restringido
    }
  }

  isPremium() {
    return Boolean(this.data.premiumUnlocked);
  }

  setPremium(status) {
    this.data.premiumUnlocked = Boolean(status);
    this.save();
  }

  recordVeteranAscension() {
    this.data.veteransForged += 1;
    this.save();
  }

  recordFallenHero(piece, locationName) {
    if (!piece || !piece.name) return;
    const entry = {
      name: piece.name,
      title: piece.title,
      veteran: Boolean(piece.veteran),
      kills: piece.kills || 0,
      location: locationName,
    };
    this.data.fallenHeroes.unshift(entry);
    if (this.data.fallenHeroes.length > 15) {
      this.data.fallenHeroes.length = 15;
    }
    this.save();
  }

  recordGameEnd(winnerColor, isCrusadeComplete = false) {
    this.data.gamesPlayed += 1;
    if (winnerColor === "w") this.data.dawnVictories += 1;
    else if (winnerColor === "b") this.data.eclipseVictories += 1;
    if (isCrusadeComplete) this.data.crusadesWon += 1;
    this.save();
  }

  /**
   * Simulación / Gancho de compra In-App (IAP) para "Códice Completo de Aethelgard"
   * En producción con Capacitor se conecta aquí Purchases.purchasePackage(...)
   */
  async purchasePremiumCodex() {
    if (window.Capacitor && window.Purchases) {
      const offerings = await window.Purchases.getOfferings();
      if (offerings.current && offerings.current.availablePackages.length > 0) {
        await window.Purchases.purchasePackage({
          aPackage: offerings.current.availablePackages[0],
        });
      }
    }
    this.setPremium(true);
    return true;
  }

  /**
   * Simulación / Gancho de Anuncio con Recompensa (Rewarded Ad) para el Pacto del Oráculo
   * En producción con Capacitor se conecta aquí AdMob.showRewardVideoAd()
   */
  async watchRewardedOraclePact(onProgress) {
    if (window.Capacitor && window.AdMob) {
      await window.AdMob.showRewardVideoAd();
      this.data.oraclePactsUsed += 1;
      this.save();
      return true;
    }
    // Simulación de 2 segundos para pruebas en navegador y APK de desarrollo
    for (let step = 2; step >= 1; step--) {
      if (onProgress) onProgress(step);
      await new Promise((r) => setTimeout(r, 750));
    }
    this.data.oraclePactsUsed += 1;
    this.save();
    return true;
  }
}
