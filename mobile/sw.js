const CACHE_NAME = "cronicas-aethelgard-v2";
const ASSETS = [
  "./",
  "./index.html",
  "./styles.css",
  "./manifest.json",
  "./js/app.js",
  "./js/engine.js",
  "./js/engine/constants.js",
  "./js/engine/model.js",
  "./js/engine/game.js",
  "./js/engine/ai.js",
  "./js/lore.js",
  "./js/lore/catalog.js",
  "./js/lore/narrative.js",
  "./js/lore/wilds.js",
  "./js/lore/crusade.js",
  "./js/ui/views.js",
  "./js/board_renderer.js",
  "./js/audio.js",
  "./js/store.js",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});
