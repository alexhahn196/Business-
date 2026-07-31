# VR Facility – Onepage

Moderne, einseitige Website für einen Facility-Management-Dienstleister.
Alles steckt in `index.html` – kein Build, kein Framework. Datei doppelklicken
oder auf einen beliebigen Webserver legen, fertig.

## Aufbau

Hero → Branchen-Leiste → Leistungen (6 Karten) → Kennzahlen → Warum wir →
Ablauf (4 Schritte) → Referenzen → Kontakt → Call-to-Action → Footer

Technisch: Dark Theme, Sticky-Navigation mit Blur, Scroll-Reveal-Animationen,
animierte Zähler, Mobile-Menü, responsiv ab 360 px. Berücksichtigt
`prefers-reduced-motion`; ohne JavaScript bleibt der Inhalt sichtbar.

## Was vor dem Livegang angepasst werden muss

Die Seite enthält **Platzhalter-Inhalte**. Vor der Veröffentlichung ersetzen:

| Was | Wo |
|---|---|
| Telefon `030 123 456 789`, Notdienst `030 123 456 700` | Navigation, Kontakt, CTA, Footer |
| E-Mail `kontakt@vr-facility.de` | Kontakt, CTA, Footer, Formular-Handler im `<script>` |
| Adresse `Musterstraße 12, 10115 Berlin` | Kontakt, Footer |
| Kennzahlen (120 Objekte, 15 Jahre, 98 %, 4,9/5 aus 86 Bewertungen) | `data-count`-Attribute, Hero-Karte |
| Referenzen / Zitate | Abschnitt `#referenzen` |
| Aussagen wie „ISO 9001", „Festpreisgarantie", „< 2 Std." | Hero, Leistungen, USP-Liste |
| Impressum, Datenschutz, AGB | Footer – zeigen aktuell auf `#kontakt` |

Rechtlicher Hinweis: Impressum und Datenschutzerklärung sind in Deutschland
Pflicht und fehlen noch. Werbeaussagen (Zertifizierungen, Reaktionszeiten,
Bewertungen) nur übernehmen, wenn sie tatsächlich zutreffen.

## Kontaktformular

Ohne Backend öffnet das Formular eine vorbereitete E-Mail im Mailprogramm des
Besuchers. Für den echten Betrieb im `<form id="contact-form">` ein
`action`/`method`-Paar auf den eigenen Endpoint setzen und den
`submit`-Handler am Ende des `<script>`-Blocks entfernen.

## Bilder

Die Fotos werden von Unsplash geladen (kostenlos nutzbar, auch kommerziell,
ohne Bildnachweis-Pflicht). Für Ladezeit und Unabhängigkeit besser eigene
Objektfotos verwenden: die `src`-URLs in den `<img>`-Tags durch lokale Pfade
ersetzen. Ohne Internetverbindung bleiben die Bildflächen leer – Layout und
Text funktionieren weiterhin.

Die Schriften (Manrope, Space Grotesk) kommen von Google Fonts. Wer keine
externen Requests möchte, bindet sie lokal ein – als Fallback greifen
System-Schriften.
