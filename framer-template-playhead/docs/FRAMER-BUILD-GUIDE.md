# Playhead — Bauanleitung für Framer

Dieses Dokument ist die Spezifikation, mit der du das Template **in Framer** nachbaust. Die Referenz-Website in `site/` ist pixelgenau das Ziel: gleiche Seiten, gleiche Sektionen, gleiche Farben, Schriften und Breakpoints. Wähle einen der drei Wege in Abschnitt 2; alle enden beim gleichen Framer-Projekt.

Zeitbudget (Erfahrungswerte für Framer-Einsteiger): Weg A 3–5 h, Weg B 6–8 h, Weg C 8–12 h.

---

## 1. Was gebaut wird

| Seite | Slug in Framer | Quelle | Besonderheit |
|---|---|---|---|
| Home | `/` | `site/index.html` | 9 Sektionen, Reels-Wall, Pakete, FAQ |
| Work | `/work` | `site/work.html` | Collection List „Projects" mit Filter (Format) |
| Project | `/work/:slug` (CMS-Detailseite) | `site/project.html` | alle Felder aus der Collection |
| Services | `/services` | `site/services.html` | Pakete, Vergleichstabelle, Add-ons, FAQ |
| About | `/about` | `site/about.html` | Portrait, Tools, Timeline, Kunden |
| Contact | `/contact` | `site/contact.html` | Framer-Formular + Booking-Embed |
| 404 | `/404` | `site/404.html` | Pflicht laut Framer-Requirements |
| Legal | `/legal` | `site/legal.html` | Impressum/Datenschutz-Gerüst (EU) |
| Start here | `/start-here` (**nicht veröffentlichen**) | `site/start-here.html` | Käufer-Anleitung + Agent-Prompts |
| Lite (separates Projekt) | `/` | `site/lite.html` | kostenlose Ein-Seiten-Version |

**Design-Tokens** (in Framer als *Color Styles* und *Text Styles* anlegen — exakt diese Namen):

Farben: `Paper #F4F1EA` · `Paper 2 #ECE7DC` · `Paper 3 #E0DACB` · `Ink #101010` · `Ink 2 #47443D` · `Ink 3 #8A857A` · `Screen #0C0C0D` · `Screen 2 #17171A` · `Screen 3 #2A2A30` · `On Screen #F4F1EA` · `On Screen 2 #A9A59B` · `Accent #FF4D1A` · `Accent 2 #FFC9B5`.

Text-Styles (Desktop / Tablet / Phone):
- `Display` Bricolage Grotesque 700 · 96 / 72 / 52 px · line-height 0.96 · letter-spacing −3.5 %
- `H1` Bricolage Grotesque 700 · 72 / 56 / 44 · lh 1.0 · ls −3 %
- `H2` Bricolage Grotesque 700 · 52 / 42 / 34 · lh 1.04 · ls −2.5 %
- `H3` Bricolage Grotesque 600 · 32 / 32 / 26 · lh 1.15 · ls −2 %
- `H4` Bricolage Grotesque 600 · 24 · lh 1.25 · ls −1.5 %
- `Lead` Inter 400 · 21 / 21 / 18 · lh 1.5 · Farbe Ink 2
- `Body` Inter 400 · 17 / 17 / 16 · lh 1.6
- `Small` Inter 400 · 15 · lh 1.55 · Ink 2
- `Mono` JetBrains Mono 500 · 12.5 · ls 8 % · Großbuchstaben (Labels, Timecodes)

Alle drei Schriften sind in Framers Font-Bibliothek (Google Fonts) — kein Upload nötig.

Breakpoints: Desktop ≥ 1200 (Container 1240, Gutter 40) · Tablet 810–1199 (Gutter 32) · Phone < 810 (Gutter 20). Sektionsabstand 128 / 96 / 72 px. Radien: Buttons Pill, Karten 22 px, Medien 14 px.

---

## 2. Drei Wege ins Framer-Projekt

### Weg A — Framer External Agent aus Claude Code (empfohlen, Framer 3.0)
Seit Framer 3.0 (Juni 2026) kann ein externer Agent (Claude Code, Cursor, Codex) direkt im Framer-Projekt arbeiten: Seiten, Layer, Komponenten, Styles und **CMS-Collections anlegen und befüllen**, in einem Branch, den du danach prüfst und mergst.

1. Neues Framer-Projekt anlegen (leer), Projekt öffnen.
2. Lokal im Terminal, im Ordner `framer-template-playhead/`:
   ```bash
   npx @framer/agent setup
   ```
   Danach in Claude Code `/framer` aufrufen, im Browser authentifizieren und das Projekt auswählen.
3. Claude Code diesen Auftrag geben (Prompt kopieren):
   ```text
   Baue das Framer-Projekt exakt nach docs/FRAMER-BUILD-GUIDE.md. Referenz: site/*.html und site/assets/css/playhead.css.
   Reihenfolge: (1) Color Styles + Text Styles aus Abschnitt 1, (2) CMS-Collections aus Abschnitt 3 inkl. Demo-Einträgen aus build/build.py,
   (3) Komponenten aus Abschnitt 4 mit Varianten, (4) Seiten aus Abschnitt 5 Sektion für Sektion, (5) Breakpoints Tablet/Phone,
   (6) Effekte aus Abschnitt 6, (7) SEO-Titel/Beschreibungen aus build/build.py. Verwende nur native Framer-Features (Stacks, Grids,
   Collection Lists, Accordion, Video, Form). Keine Code-Komponenten außer für die Reels-Hover-Play-Logik, falls nötig.
   ```
4. Branch im Framer-Editor prüfen (jede Seite in drei Breakpoints), mergen, veröffentlichen.

### Weg B — „HTML to Framer"-Extension (sektionsweise)
Framers offizielle Chrome-Extension kopiert markierte Bereiche einer *live geöffneten* Seite als Framer-Layer (Text, Bilder, Farben, Flex-Stacks). Nicht übernommen werden: CMS, Formulare, Hover/Scroll-Effekte, Breakpoints, Grids mit min/max.

1. `site/index.html` in Chrome öffnen (Doppelklick genügt; für Bilder muss der Ordner `site/` komplett vorliegen).
2. Extension aktivieren, Sektion anklicken (z. B. `section.hero`), kopieren, in Framer einfügen. Sektion für Sektion, Seite für Seite.
3. Danach in Framer: Text-Styles zuweisen, Color Styles ersetzen, Grids in Framer-Grids umbauen, Breakpoints setzen, CMS verbinden (Abschnitt 3), Effekte (Abschnitt 6).

### Weg C — Manuell nach Spezifikation
Abschnitte 3–6 sind so geschrieben, dass sie ohne die HTML-Datei funktionieren. Halte die Referenz-Seite daneben.

---

## 3. CMS-Collections (genau zwei → Basic-Plan-kompatibel)

### Collection „Projects" (13 Demo-Einträge in `build/build.py`: 7 × 16:9, 6 × 9:16)
| Feld | Typ | Hinweis |
|---|---|---|
| Title | Title | |
| Slug | Slug | |
| Client | Plain text | |
| Format | Option: Short-form · Long-form · Ads · Motion · Podcast | Filter auf /work |
| Platform | Option: YouTube · TikTok · Reels · Shorts · Web | Badge auf Reel-Karten |
| Orientation | Option: 16:9 · 9:16 | steuert Karten-Variante |
| Poster | Image | 16:9 = 1600×900, 9:16 = 1080×1920 |
| Video URL | Link | YouTube/Vimeo/MP4 → Embed auf Detailseite |
| Result | Plain text | z. B. „2.4M views" |
| Summary | Plain text | Untertitel im Hero der Detailseite |
| Brief / Approach / Outcome | Formatted text | drei Textblöcke |
| Metric 1–3 (Wert + Label) | Plain text ×6 | Kacheln unter dem Video |
| Stills | Gallery (3 Bilder) | Sektion „Frames from the edit" |
| Featured | Toggle | Home zeigt `Featured = true`, max. 3 (16:9) + 6 (9:16) |
| Date | Date | Sortierung |

### Collection „Testimonials" (3 Demo-Einträge)
Quote (Plain text) · Name · Role · Initials · Color (Color) · Featured (Toggle).

Alle anderen wiederholten Inhalte (Services, Pakete, FAQ, Prozess, Add-ons, Timeline, Kunden) bleiben statische Komponenten mit Varianten — das hält das Template auf zwei Collections.

---

## 4. Komponenten (mit Varianten)

| Komponente | Varianten / Props | Referenz-Klasse |
|---|---|---|
| Nav | Desktop · Tablet/Phone (Burger + Overlay); Prop `status` (Text) | `.nav` |
| Button | Primary · Accent · Ghost × Size (S/M/L) × Theme (Paper/Screen); Icon Arrow | `.btn` |
| Pill / Badge | Default · Solid · Accent; mit/ohne Dot | `.pill`, `.badge` |
| Section Head | Prop `index` (01–08), `title`, `lead`, optional Link; Theme | `.section-head` |
| Media Frame | 16:9 · 9:16 · Rounded L; Slots: Poster, Frame-Corners, Play-Badge, Timecode-Bar | `.frame` |
| Reel Card | CMS-gebunden (Poster, Platform, Views, Title, Client, Meta); Hover: Zoom + Progress-Bar + Video-Play | `.reel` |
| Project Card | 16:9 · 9:16 (Orientation); CMS-gebunden | `.project` |
| Service Card | Icon (4 SVGs) · Title · Text · Deliverables (optional) · From-Preis | `.service` |
| Process Step | Nummer · Zeitpunkt · Titel · Text; Linie mit Playhead als eigene Grafik | `.step`, `.process-line` |
| Proof Tile | Big number (mit Accent-Span) · Text · Who | `.proof-tile` |
| Testimonial | CMS-gebunden; Sterne (5 SVG) · Quote · Avatar (Initials + Color) | `.testimonial` |
| Price Card | Default · Featured (dunkel + Ribbon „Most booked") | `.price-card` |
| FAQ Item | Framer-Accordion; Plus-Icon rotiert 45° | `.faq-item` |
| CTA Band | Accent-Fläche, Timecode oben rechts, 2 Buttons | `.cta-band` |
| Footer | 4 Spalten + Riesenwort + Bottom-Row | `.footer` |
| Marquee | Framer-Ticker mit 10 Wortmarken (Text, keine Logos) | `.marquee` |

Icons: 4 Service-Icons, Arrow, Tick, Plus, Star liegen als Inline-SVG in `build/build.py` (Klasse `ICONS`) — als Framer-Vektoren einfügen.

---

## 5. Seitenaufbau Sektion für Sektion

**Home** (Stack, vertical): Hero (Grid 1.05fr/0.95fr; rechts Media-Frame 16:9 + schwebende Reel-Karte 34 % Breite, 3° rotiert, + Tag „+38 % retention") → Marquee → Showreel (Theme Screen, Frame 16:9, Meta-Zeile) → Reels-Wall (Theme Screen, Grid 6 → 3 → 2 Spalten, Collection List `Orientation = 9:16`, Featured) → Selected Work (Grid 3 → 2 → 1, Collection List `Orientation = 16:9`, Featured, Limit 3) → Services (Theme Paper 2, Grid 4 → 2 → 1) → Process (Theme Screen, Grid 4 → 2 → 1, Linie nur Desktop) → Results (3 Proof-Tiles + 3 Testimonials aus CMS) → Packages (Theme Paper 2, Grid 3 → 2 → 1) → FAQ (Grid 0.8fr/1.2fr → 1 Spalte) → CTA Band → Footer.

**Work:** Page-Hero → Filter-Chips (Framer-CMS-Filter nach `Format`) → Grid 3 → 2 → 1 mit gemischten 16:9/9:16-Karten (Variante per `Orientation`).

**Project (CMS-Detail):** Detail-Head (Grid 1.3fr/0.7fr; rechts 4 Fakten) → Frame 16:9 mit Video-Embed (Video URL) → 3 Metrik-Kacheln → Text (Brief/Approach/Outcome mit Pullquote) + Sticky-Sidebar (Fakten, Button) → Stills-Galerie (Theme Screen, 3 → 2 → 1) → Next-Project-Karte.

**Services:** Page-Hero → 4 Service-Karten mit Deliverables → Pakete (Paper 2) → Vergleichstabelle (auf Phone horizontal scrollbar) → Add-ons (Theme Screen, Grid 3 → 2 → 1) → FAQ.

**About:** Page-Hero → Grid 0.9fr/1.1fr (Portrait 4:5 + Pills | Text, Tools-Pills, 3 Proof-Tiles) → Timeline (5 Zeilen, Grid 140px/1fr/auto) → Kunden-Grid 4 → 2 → 1 → Testimonials (Theme Screen).

**Contact:** Page-Hero → Grid 1fr/0.8fr (Framer-Form: Name, Email, Project type (Select), Budget (Select), Link, Message | Contact-Card mit Booking-Embed-Platzhalter, Email `mailto:`, Telefon `tel:`) → 3 Schritte.

**404:** Riesige „404" (mittlere Ziffer Accent) + 2 Buttons. **Legal:** Doc-Layout mit Sprungnavigation. **Start here:** Doc-Layout, unveröffentlicht lassen (Seite → „Exclude from publishing" bzw. nicht verlinken).

---

## 6. Effekte & Interaktionen (nur native Framer-Effekte)

- **Appear** auf allen `.appear`-Elementen: Opacity 0→1, Y 18→0, 0.7 s, Ease `[0.2, 0.7, 0.2, 1]`, Stagger 80 ms innerhalb einer Sektion.
- **Buttons:** Hover Y −1 px; Primary wird Accent; Arrow-Icon +3 px X.
- **Reel Card:** Hover → Bild Scale 1.05 (0.6 s), Play-Badge Opacity 0, Progress-Bar animiert 0→100 % (4 s, loop); Video-Layer „Play on hover" (muted, loop).
- **Project Card:** Hover → Bild Scale 1.04.
- **Service Card:** Hover → Border Ink, Y −3 px.
- **FAQ:** Accordion; Plus rotiert 45°, Kreis wird Ink.
- **Marquee:** Ticker 32 s, Pause on hover.
- **Nav:** Sticky, Background Paper 82 % + Blur 12.
- Keine Scroll-Parallax-Spielereien — Performance-Check muss grün bleiben.

---

## 7. SEO, Assets, Abgabe-Checkliste

- Titel/Beschreibungen pro Seite: siehe `pages`-Liste in `build/build.py`. Social-Image: `site/assets/img/og-cover.jpg`. Favicon: `favicon.svg`.
- Alt-Texte für alle Bilder sind in den HTML-Dateien vorgegeben.
- Demo-Bilder (`site/assets/img/`) sind selbst erzeugte Grafiken (keine Lizenzfrage). Käufer ersetzen sie durch eigene Poster/Videos.
- Vor dem Einreichen (Framer-Requirements): 404 vorhanden ✔ · kein Lorem ipsum ✔ · alle Links funktionieren · `mailto:`/`tel:` gesetzt ✔ · 3 Breakpoints geprüft · CMS-Felder klar benannt ✔ · Assets in Ordnern (`Posters`, `Reels`, `Icons`, `Brand`) · Performance-Check grün · Site-Settings ausgefüllt · Start-here-Seite unveröffentlicht · Remix-Link erzeugt.

---

## 8. Playhead Lite (kostenlose Version)
Eigenes Framer-Projekt aus `site/lite.html`: Hero, Marquee, Reels (6 statische Karten), Services, Testimonials (statisch), Kontakt-Band, Footer. Keine CMS-Collection. Nav-Links zeigen auf Anker. Im Listing klar als „Lite" benennen und auf Playhead (Pro) verweisen — das ist der Upsell.
