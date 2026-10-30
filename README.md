# Crónicas de Aethelgard · Ajedrez Táctico Medieval

Un juego de ajedrez táctico y narrativo ambientado en la disputa por el Trono de Aethelgard, con ediciones sincronizadas para **Escritorio (Python / Tkinter)** y **Móvil / Web PWA (JavaScript / HTML5 Canvas)**.

## Los Cuatro Reinos e Inspiración Histórica

- **☀ Orden del Alba (Blancas)** — *Sacro Imperio y Cruzadas Franco-Normandas*
  - **Soberanos**: `Rey Balduino` y `Reina Leonor`
- **☾ Legión del Eclipse (Negras)** — *Principado de Valaquia y Transilvania Gótica*
  - **Soberanos**: `Rey Vladimir` y `Reina Carmila`
- **⚔ Forja Carmesí (Rojas)** — *Esparta Clásica e Imperio Romano*
  - **Soberanos**: `Rey Leónidas` y `Reina Gorgo`
- **❖ Reino de Avalon (Verdes)** — *Clanes Celtas*
  - **Soberanos**: `Rey Vercingétorix` y `Reina Boudica`

## Modos de Campaña y Características

- **Crónica Clásica (8x8)**: Duelo tradicional entre dos reinos con ascenso a **Veterano (★)** al lograr 2 bajas.
- **Gran Tablero Imperial (12x12)**: 144 casillas y 36 piezas por bando desplegando las **10 órdenes míticas** del Códice (*Halcón, Elefante, Amazonas, Saltamontes, Noctámbulo, Centauro, Camello, León, Cebra y Fénix*).
- **Tierra Salvaje**: Ejércitos dinámicos y terreno táctico (*bosques, ríos, peñascos, acantilados, empalizadas y ruinas fortificadas*) con sucesos de guerra interactivos cada 6 jugadas.
- **Cruzada Encadenada (4 etapas)**: Campaña progresiva donde tus sobrevivientes y veteranos avanzan de etapa y reclutan refuerzos míticos.
- **Guerra de los Cuatro Frentes**: Batalla simultánea de los 4 reinos (Sur, Oeste, Norte y Este) en un mismo tablero.
- **Reglas opcionales**: *Elefante de Guerra* y *Niebla de Guerra*.

## Ejecución

### Edición de Escritorio (Python)
```bash
python3 main.py
```

### Edición Móvil / Web (PWA)
Sirve la carpeta `mobile/` con cualquier servidor estático:
```bash
python3 -m http.server 8000 --directory mobile
```

### Pruebas Unitarias
```bash
python3 -m unittest -v tests.py
node mobile/test_mobile_engine.mjs
```
