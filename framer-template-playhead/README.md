# Playhead — Framer-Template für Video-Editoren & Short-Form-Creator

Verkaufsfertiges Template-Paket für den Framer-Marketplace. Entscheidung und Marktdaten: `../Framer-Template-Marktrecherche-2026.md`.

| Ordner / Datei | Inhalt |
|---|---|
| `site/` | Fertige Referenz-Website (10 HTML-Seiten, CSS-Design-System, JS, Poster-Grafiken, Schriften). Lokal öffnen: `site/index.html` |
| `docs/FRAMER-BUILD-GUIDE.md` | Bauanleitung für Framer: Tokens, CMS-Schema, Komponenten, Seiten, Effekte, Checkliste — drei Wege (Framer External Agent aus Claude Code, HTML-to-Framer-Extension, manuell) |
| `docs/LISTING.md` | Marketplace-Listing (Pro 69 $ + Lite kostenlos), Polar-Checkout, Launch-Post, Preislogik, Support-Vorlagen |
| `previews/` | Marketplace-Vorschaubilder (`cover-*.jpg`, 1600×1200) und QA-Screenshots aller Seiten (`qa/`, Desktop 1440 + Phone 390) |
| `build/` | Jinja-Templates + `build.py` (alle Texte/Daten), Poster-Generator (`posters/`), Screenshot-Skripte |

## Seiten
Home · Work (filterbar, 16:9 + 9:16) · Project (CMS-Fallstudie) · Services & Packages · About · Contact · 404 · Legal · Start Here (Käufer-Guide, unveröffentlicht) · Lite (kostenlose Ein-Seiten-Version)

## Design-System
Paper `#F4F1EA` / Ink `#101010` / Screen `#0C0C0D` / Accent `#FF4D1A` · Bricolage Grotesque (Display) · Inter (Body) · JetBrains Mono (Labels, Timecodes) · Breakpoints wie Framer: Desktop ≥1200, Tablet 810–1199, Phone <810. Zwei CMS-Collections (Projects, Testimonials) → Basic-Plan-kompatibel.

## Neu bauen / ändern
```bash
python3 build/build.py                      # HTML aus build/templates + Daten in build/build.py
node build/posters/render.js                # Poster-Grafiken (braucht Playwright + Chromium)
node build/shots.js                         # QA-Screenshots → previews/qa
node build/covers.js                        # Marketplace-Cover → previews/
```
Texte, Projekte, Pakete, FAQ: alles in `build/build.py` (ein Ort). Schriften liegen lokal unter `site/assets/fonts/` (SIL Open Font License).

## Lizenz der Demo-Assets
Poster, Reels-Cover, Portrait-Platzhalter und OG-Bild sind programmatisch erzeugte Eigen-Grafiken (keine Fremdrechte). Kundennamen, Personen und Zahlen sind fiktiv.
