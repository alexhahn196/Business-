# Manti & Pelmeni – Landingpage

Eigenständige, statische Landingpage in einer Datei (`index.html`) mit 3D-animierten Manti und Pelmeni.
Die Teigtaschen werden prozedural mit Three.js erzeugt – es sind keine 3D-Modelle oder Fotos nötig.

## Öffnen

- `index.html` im Browser öffnen (Doppelklick). Internetverbindung nötig: Three.js und die Schriften kommen per CDN.
- Alternativ lokal ausliefern: `npx serve manti-landing`

## Was die Seite macht

- Hero mit schwebendem Manti (mit Dampf) und Pelmeni-Cluster, Maus-Parallaxe, Scroll-Rotation
- Beim Scrollen fliegen die Objekte von der Hero in ihre Kapitel („Manti“, „Pelmeni“) und in den Bestell-Abschnitt.
  Die Zielpositionen sind einfach DOM-Elemente mit `data-actor="manti"` bzw. `data-actor="pelmeni"`.
- Speisekarte als Preisliste mit Punktlinien, Family-Box als hervorgehobenes Panel
- Ticker, Scroll-Reveals, Zähler, magnetische Buttons, Lese-Fortschritt, Körnung
- Ohne WebGL: Fallback mit Schriftzug statt 3D. `prefers-reduced-motion` wird respektiert.

## Anpassen

- Texte und Preise: direkt im HTML (Abschnitte `#manti`, `#pelmeni`, `#speisekarte`, `#bestellen`)
- Farben und Schriften: CSS-Variablen in `:root` am Anfang der Datei
- Platzhalter ersetzen: Telefonnummer, Adresse, Öffnungszeiten, Bewertungszahlen, Ziel des Buttons „Online bestellen“, Impressum/Datenschutz

## Technik

- Three.js 0.170 über jsdelivr (Import Map), Google Fonts: Bricolage Grotesque, Instrument Sans, DM Mono
- Keine Build-Schritte, keine Abhängigkeiten im Repo
