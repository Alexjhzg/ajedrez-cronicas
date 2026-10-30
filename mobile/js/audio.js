/**
 * Sintetizador de audio medieval y vibración háptica (Web Audio API + Vibration API)
 * Cero archivos externos para garantizar carga instantánea y peso mínimo en APK.
 */

export class SoundEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
    this.haptics = true;
  }

  _ensureCtx() {
    if (!this.enabled) return null;
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === "suspended") {
      this.ctx.resume().catch(() => {});
    }
    return this.ctx;
  }

  vibrate(pattern) {
    if (!this.haptics) return;
    if (typeof navigator !== "undefined" && typeof navigator.vibrate === "function") {
      try {
        navigator.vibrate(pattern);
      } catch (_e) {
        // Ignorar en navegadores sin soporte
      }
    }
  }

  playSelect() {
    this.vibrate(8);
    const ctx = this._ensureCtx();
    if (!ctx) return;
    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "triangle";
    osc.frequency.setValueAtTime(320, now);
    osc.frequency.exponentialRampToValueAtTime(440, now + 0.055);
    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.065);
  }

  playMove(heavy = false) {
    this.vibrate(heavy ? [18, 25, 22] : 14);
    const ctx = this._ensureCtx();
    if (!ctx) return;
    const now = ctx.currentTime;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(heavy ? 115 : 165, now);
    osc.frequency.exponentialRampToValueAtTime(heavy ? 48 : 68, now + (heavy ? 0.16 : 0.11));
    gain.gain.setValueAtTime(heavy ? 0.24 : 0.16, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + (heavy ? 0.17 : 0.12));
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + (heavy ? 0.18 : 0.13));
  }

  playCapture(veteranAscend = false) {
    this.vibrate(veteranAscend ? [30, 40, 60] : [28, 30, 18]);
    const ctx = this._ensureCtx();
    if (!ctx) return;
    const now = ctx.currentTime;

    // Golpe metálico grave + resonancia de espada
    for (const [freqStart, freqEnd, dur, type, vol] of [
      [140, 42, 0.22, "sawtooth", 0.18],
      [620, 290, 0.16, "triangle", 0.12],
    ]) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freqStart, now);
      osc.frequency.exponentialRampToValueAtTime(freqEnd, now + dur);
      gain.gain.setValueAtTime(vol, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + dur);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + dur + 0.01);
    }

    if (veteranAscend) {
      this.playVeteranFanfare(0.14);
    }
  }

  playVeteranFanfare(delay = 0) {
    const ctx = this._ensureCtx();
    if (!ctx) return;
    const base = ctx.currentTime + delay;
    const notes = [440, 554.37, 659.25];
    notes.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const start = base + i * 0.07;
      osc.type = "triangle";
      osc.frequency.setValueAtTime(freq, start);
      gain.gain.setValueAtTime(0.11, start);
      gain.gain.exponentialRampToValueAtTime(0.001, start + 0.26);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(start);
      osc.stop(start + 0.27);
    });
  }

  playCheck() {
    this.vibrate([40, 50, 40]);
    const ctx = this._ensureCtx();
    if (!ctx) return;
    const now = ctx.currentTime;
    for (const [freq, offset] of [
      [220, 0],
      [207.65, 0.12],
    ]) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(freq, now + offset);
      gain.gain.setValueAtTime(0.11, now + offset);
      gain.gain.exponentialRampToValueAtTime(0.001, now + offset + 0.25);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now + offset);
      osc.stop(now + offset + 0.26);
    }
  }

  playVictory(isWhite) {
    this.vibrate([45, 40, 45, 40, 90]);
    const ctx = this._ensureCtx();
    if (!ctx) return;
    const now = ctx.currentTime;
    const chord = isWhite ? [261.63, 329.63, 392.0, 523.25] : [220.0, 261.63, 329.63, 415.3];
    chord.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const t = now + idx * 0.09;
      osc.type = "triangle";
      osc.frequency.setValueAtTime(freq, t);
      gain.gain.setValueAtTime(0.12, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.55);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(t);
      osc.stop(t + 0.56);
    });
  }
}
