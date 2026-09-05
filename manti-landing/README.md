# Manti & Pelmeni – Landingpage

Statische Landingpage im traditionellen usbekischen Stil (Lapisblau, Türkis-Glasur, Gold, Krapprot, Teig-Creme;
Girih-Sternmuster, Ikat-Bänder, Spitzbögen) mit 3D-animierten Manti und Pelmeni.

## Öffnen

- `index.html` im Browser öffnen (Doppelklick). Internetverbindung nötig: Three.js und die Schriften (Yeseva One, Lora) kommen per CDN.
- Alternativ lokal ausliefern: `npx serve manti-landing`

## Dateien

| Datei | Zweck |
| --- | --- |
| `index.html` | Die komplette Seite: Layout, Texte, Styles, Animationen |
| `assets/models.js` | Die beiden 3D-Modelle als eingebettete, komprimierte Daten (werden von `index.html` geladen) |
| `assets/manti.glb`, `assets/pelmeni.glb` | Die Original-3D-Modelle (GLB), z. B. für Blender oder andere Projekte |
| `assets/manti.jpg`, `assets/pelmeni.jpg` | Produktfotos für die Speisekarte |

## Wie die 3D-Modelle entstanden sind

1. Referenzfotos je Teigtasche mit Higgsfield (Nano Banana Pro) generiert: klassischer usbekischer Manti (viereckig gefaltet, vier Ecken oben zusammengekniffen) und ein Pelmeni-Öhrchen mit gekräuseltem Rand.
2. Daraus per Bild-zu-3D (Tripo H3.1 über Higgsfield) texturierte GLB-Modelle erzeugt.
3. Mit `gltf-transform` auf 24k Dreiecke vereinfacht, Textur auf 1024 px verkleinert und als quantisierte Daten in `assets/models.js` eingebettet, damit die Seite ohne weitere Dateien funktioniert.

Verbrauchte Higgsfield-Credits: 48 (4 Bilder à 2, zwei Tripo-Modelle à 9, zwei Hunyuan-Vergleichsmodelle à 11).

## Was die Seite macht

- Hero mit Manti (mit Dampf) und Pelmeni-Cluster im Goldbogen, Maus-Parallaxe, Scroll-Rotation
- Beim Scrollen fliegen die Objekte von der Hero in ihre Kapitel („Manti“, „Pelmeni“) und in den Bestell-Abschnitt.
  Die Zielpositionen sind DOM-Elemente mit `data-actor="manti"` bzw. `data-actor="pelmeni"`.
- Speisekarte als Preisliste mit Punktlinien, Family Box als Lackrot-Panel, Ticker, Scroll-Reveals, Zähler, Lese-Fortschritt
- Ohne WebGL: Fallback mit Schriftzug statt 3D. `prefers-reduced-motion` wird respektiert.

## Anpassen

- Texte und Preise: direkt im HTML (Abschnitte `#manti`, `#pelmeni`, `#speisekarte`, `#bestellen`)
- Farben und Muster: CSS-Variablen in `:root` am Anfang der Datei
- Größe und Neigung der 3D-Objekte: Felder `fit` und `tilt` in `assets/models.js`
- Platzhalter ersetzen: Telefonnummer, Adresse, Öffnungszeiten, Bewertungszahlen, Ziel des Buttons „Online bestellen“, Impressum/Datenschutz
