# Das 10k-Betriebssystem

**Ein System, das 10.000 €+/Monat erzeugt — mit KI als Bau- und Produktionsmotor**

*Stand: 27.07.2026 · Baut auf allen 10 Vorarbeiten dieses Repos auf · Teil 1 von 3 (Architektur) · Teil 2: `KI-Projektfabrik.md` (wie gebaut wird) · Teil 3: `Betriebssystem-Cockpit.md` (wie gesteuert wird)*

---

## Warum dieses Dokument anders ist als die neun davor

Die bisherigen Analysen haben eine Frage beantwortet: **„Welches Modell?"** Sie kamen alle zum selben Ergebnis — jedes Einzelmodell liegt bei 4–12 % Wahrscheinlichkeit auf 10k in Monat 6, und der belegte Median liegt bei 2.500–5.000 € nach 6 Monaten mit Durchbruch in Monat 9–15.

Das ist die richtige Antwort auf die falsche Frage. **Ein Modell ist eine Lotterie. Ein System ist ein Geschäft.** Der Unterschied ist nicht Optimismus — er ist strukturell: Ein System hat mehrere Ströme mit unterschiedlichen Zeitprofilen, feste Entscheidungs-Gates, und jeder Strom senkt die Kosten des nächsten. Genau das fehlt bisher.

Dieses Dokument liefert die Architektur. Es erfindet keine neuen Marktzahlen — jede Marktbehauptung stammt aus den bereits recherchierten Dokumenten dieses Repos (verlinkt an Ort und Stelle). Alles Neue ist entweder **Rechnung** (nachvollziehbare Arithmetik) oder **Annahme** (als solche markiert).

---

## Teil 1: Die drei Gesetze, die deine eigene Recherche bewiesen hat

Bevor irgendetwas gebaut wird — das hier ist die Physik des Feldes. Jede Systementscheidung unten folgt daraus.

### Gesetz 1: Produktion ist gratis geworden. Distribution ist der Engpass.

> *„Indie Hacker bauen schicke KI-Fabriken, aber haben kein Geld und keinen Traffic."* — Levels, Juni 2026, zitiert in `IndieHacker-Top5-Modelle-2026.md`

Median-SaaS: 145 $ MRR. Median-App: unter 50 $/Monat nach 12 Monaten. Nur ~6,1 % knacken 10k MRR. Und jeder dokumentierte Gewinner hatte vorher Distribution (Levels: 700k Follower; Kleo: 480k; Marc Lou: seine Audience).

**Konsequenz fürs System:** Zeit, die in „noch ein Asset bauen" fließt, ist fast immer schlechter investiert als Zeit, die in „das gebaute Asset vor Menschen bringen" fließt. Das System muss Bau-Zeit hart deckeln.

### Gesetz 2: KI-Output wird dort bezahlt, wo niemand einem Menschen vertrauen muss.

Das ist der schärfste Befund aus `Pure-KI-TikTokShop-10k-Faktencheck.md` — und er ist verallgemeinerbar:

| Was verkauft wird | Vertrauens-Barriere | Funktioniert reine KI? | Beleg aus dem Repo |
|---|---|---|---|
| **Aufmerksamkeit** (AdSense: Werbetreibender zahlt pro View) | keine | **Ja, belegt** | Adavia Davis, Fortune Dez 2025 — der eine verifizierte pure-KI-Dauerverdiener |
| **Ein B2B-Artefakt** (Kunde kauft ein Ergebnis, das er selbst bewertet) | niedrig | **Ja** | Fiverr „AI UGC"-Kategorie; Upwork +329 % YoY |
| **Software** (funktioniert oder funktioniert nicht) | niedrig | **Ja** | Shopify-Apps, Micro-SaaS-Fälle |
| **Physisches Produkt an einen Fremden** (er muss dir glauben) | **hoch** | **Nein — 0 verifizierte Dauerfälle** | Der komplette US-/DE-/Alle-Nischen-Faktencheck |

Konsumenten-Vertrauen in KI-Creator-Content: von ~60 % (2023) auf ~26 % (Anfang 2026). Marken fordern Provisionen zurück (SharkNinja, 16.07.2026). TikTok labelt automatisch per C2PA.

**Konsequenz fürs System:** Der Hauptumsatzstrom darf nicht davon abhängen, dass ein Fremder aufgrund synthetischen Contents ein physisches Produkt kauft. Genau dieser Weg — Affiliate-Provision aus KI-Videos — war der Plan der ersten neun Dokumente, und er ist der schlechteste im ganzen Feld.

### Gesetz 3: Der Preis pro Kunde bestimmt, wie viel Distribution du brauchst.

Das ist die eigentliche Schlüssel-Erkenntnis, und sie steht bisher nirgends explizit im Repo. Reine Arithmetik, keine Marktbehauptung:

| Was du verkaufst | € pro Kunde/Monat | Kunden für 10k | Nötige Reichweite (Größenordnung¹) |
|---|---|---|---|
| TikTok-Shop-Affiliate-Provision | ~4–5 € pro Verkauf | **2.000–2.500 Verkäufe** | 0,5–1,5 Mio. Views/Monat |
| Digitalprodukt einmalig (49–97 €) | ~30 € netto nach Gebühren/Affiliates | **330 Käufe/Monat** | 30–100k Kontakte/Monat |
| Micro-SaaS-Abo | 29 € | **345 zahlende** | 10–30k Besucher/Monat, dauerhaft |
| Community-Abo | 97 € | **103 Mitglieder** | 5–15k erreichte Menschen |
| B2B-Festpreis-Paket | 500 € | **20 Aufträge/Monat** | ~200–400 Angebots-Aufrufe |
| **B2B-Retainer** | **2.000 €** | **5 Kunden** | **~50–100 qualifizierte Gespräche — insgesamt, nicht pro Monat** |

¹ *Reichweite-Spalte = grobe Planungs-Größenordnung aus Standard-Conversion-Annahmen (0,3–1 % View→Kauf bei Shop-Videos laut `TikTok-Shop-Machbarkeitsanalyse.md`; 1–3 % Besucher→zahlend bei SaaS). Keine Messwerte — Planungshilfe, um Größenordnungen zu vergleichen.*

Lies die Tabelle von unten nach oben. **Fünf Kunden gegen 2.500 Verkäufe.** Beides ergibt 10.000 €. Der einzige Unterschied ist der Preis pro Kunde — und der bestimmt, ob du eine Millionen-Reichweite brauchst oder fünf Menschen mit Budget.

Und genau hier liegt die Arbitrage, die KI 2026 eröffnet: KI hat die **Produktionskosten** eines Werbevideos, eines Reports, eines kleinen Tools gegen null gedrückt — aber sie hat den **Marktpreis** für dasselbe Artefakt bei einem Unternehmen nicht gesenkt, weil das Unternehmen die Alternative (Agentur, Freelancer, eigene Zeit) weiter zu Altpreisen kalkuliert. Grenzkosten 1–15 $ pro Video, Marktpreis 50–500 $ — das steht bereits in `KI-Geschaeftsmodelle-10k.md`, Platz 2. Es wurde nur nie als *strukturelles Prinzip* behandelt.

**Konsequenz fürs System — und das ist die zentrale Empfehlung dieses Dokuments:**

> **Baue von oben nach unten, nicht von unten nach oben.**
> Starte bei dem höchsten Preispunkt, den du mit KI ehrlich bedienen kannst, weil er die geringste Distribution braucht. Nutze den Cash und den Beweis daraus, um die langsamen, compoundenden Schichten zu finanzieren.

Der Instinkt sagt das Gegenteil („erst Reichweite aufbauen, dann monetarisieren"). Der Instinkt ist hier falsch, weil Reichweite die teuerste und langsamste Ressource im ganzen System ist — 12–24 Monate laut jeder einzelnen Vorarbeit.

---

## Teil 2: Die Architektur — vier Schichten, ein Schwungrad

Das System besteht aus vier Schichten. Sie starten **nicht** gleichzeitig, aber sie sind von Anfang an aufeinander ausgelegt.

```
   Schicht C — DISTRIBUTIONS-ASSET (SignalSpace)
   langsam · compoundend · liefert Beweis + Inbound
            │  Beweis, Reichweite, Vertrauen
            ▼
   Schicht A — CASH-MOTOR (B2B, produktisiert)
   schnell · aktiv · finanziert alles         ─────┐
            │  Cash + Problemkenntnis              │  bezahlt
            ▼                                      │  die Stunden
   Schicht B — PRODUKT-SCHICHT (MRR)               │
   langsam · compoundend · kauft Zeit zurück ──────┘
            ▲
            │  senkt Grenzkosten aller drei
   Schicht D — KI-BETRIEBSSYSTEM (die Fabrik)
```

### Schicht A — Der Cash-Motor: produktisierte KI-Kreativarbeit für Unternehmen

**Was:** Feste Pakete statt Stundensätze. KI-produzierte Werbe-/Content-Assets für kleine und mittlere Unternehmen und E-Commerce-Marken — Video-Ad-Varianten, Produktvideo-Sets, Content-Pakete, Landingpages.

**Warum zuerst:** Höchster Preis pro Kunde → geringste nötige Distribution (Gesetz 3). Erster Umsatz in Wochen statt Monaten. Kein Algorithmus-Glück. Und es ist das Modell mit dem klarsten belegten B2B-Preis in deiner eigenen Recherche (`KI-Geschaeftsmodelle-10k.md`, Platz 2: Median M6 3.500–5.000 €).

**Preisleiter (Planwerte, an den Repo-Zahlen kalibriert):**

| Stufe | Angebot | Preis | Deine Zeit | Zweck |
|---|---|---|---|---|
| Einstieg | 3 Ad-Varianten, ein Produkt | 149 € | 1,5–2 h | Bewertungen, Türöffner |
| Standard | 8 Varianten + Hook-Matrix | 449 € | 3–4 h | Der Brot-und-Butter-Verkauf |
| Premium | 15 Varianten + Testplan + Report | 990 € | 6–8 h | Ankerpreis, macht Standard billig |
| **Retainer** | **monatlich 12–20 Assets + Testzyklus** | **1.500–2.500 €/Monat** | **8–12 h/Monat** | **Das eigentliche Ziel** |

**Die 10k-Rechnung für Schicht A allein:** 4 Retainer × 2.000 € = 8.000 € bei ~40 h Arbeit im Monat. Das ist ~200 €/Stunde — und es ist der einzige Weg im ganzen Repo, der 10k mit weniger als drei Stunden Distributionsarbeit pro Woche erreichbar macht.

**Der ehrliche Haken — zweimal:**

1. **Zeit gegen Geld.** Schicht A hört auf zu zahlen, wenn du aufhörst. `IndieHacker-Top5-Modelle-2026.md` listet das unter „die vier Fallen" — zu Recht. **Deshalb ist Schicht A ausdrücklich der Finanzier, nicht das Ziel.** Sie kauft die Stunden für Schicht B.
2. **Der Kaltstart ist der schwerste Teil des ganzen Systems.** Die ersten 10 Aufträge auf einem Marktplatz ohne Bewertungen sind hart (Fiverrs Success-Score). Dein Kriterium „keine Kaltakquise" ist auf Marktplätzen erfüllt — die Suche bringt die Käufer — aber es kostet dich Geschwindigkeit, und du musst wissen wofür.

**Die Lösung für den Kaltstart, die keine Kaltakquise ist** (drei Wege, parallel):
- **Spec-Portfolio:** 10 Assets für echte, aber nicht beauftragte Marken produzieren. Kostet 2 Wochenenden, kostet null Euro, ersetzt Referenzen. Das ist Standard in der Kreativbranche und völlig legitim, solange nichts als echte Zusammenarbeit dargestellt wird.
- **Warmes Seeding:** 3–5 Pilotprojekte zu 50 % Preis oder gratis gegen Bewertung + Erlaubnis zur Referenznennung — im eigenen Umfeld (Bekannte mit Firma, lokaler Handel, Vereine). Das ist kein Kaltverkauf, es ist Beweisaufbau.
- **Schicht C als Schaufenster:** Dein SignalSpace-Kanal und jedes gute Video sind das Portfolio. `Parfuem-Talking-Bottle-Format-Bewertung.md`, Review-Punkt 2, hat das bereits erkannt: *„Jedes gute Video zusätzlich als Portfolio-Stück archivieren."* Genau das ist es — nur ist es jetzt kein Nebeneffekt mehr, sondern der Zweck.

**Meilenstein-Gate A:** 1.000 €/Monat aus Schicht A innerhalb von 90 Tagen ab erstem veröffentlichten Angebot. Verfehlt → Angebot ändern (Nische, Preis, Format), nicht das Modell.

### Schicht B — Die Produkt-Schicht: MRR, mit Claude Code gebaut

**Was:** Ein kleines B2B-Tool oder Abo-Produkt (Micro-SaaS), gebaut mit KI, für ein Problem, das dir deine Schicht-A-Kunden gezeigt haben.

**Warum zweitens und nicht zuerst:** Weil `IndieHacker-Top5-Modelle-2026.md` genau das beantwortet — „Boring vertikales B2B-Micro-SaaS" ist das Modell mit dem durabelsten Burggraben (Workflow- und Regulierungs-Lock-in, den Foundation-Models nicht absorbieren; realistische Solo-Decke 5–30k MRR). Aber der Engpass ist nicht das Bauen, sondern **zu wissen, welches Problem echtes Geld wert ist.** Diese Information bekommst du geschenkt, wenn du erst ein halbes Jahr für zahlende Unternehmen gearbeitet hast. Wer zuerst baut, rät.

**Der Kandidaten-Filter (alle fünf müssen erfüllt sein):**
1. Das Problem ist dir bei ≥3 Schicht-A-Kunden **unabhängig** begegnet.
2. Es kostet den Kunden messbar Zeit oder Geld (er kann die Zahl nennen).
3. Es ist zu klein für einen großen Anbieter und zu speziell für ein Foundation-Model.
4. Ein deutschsprachiger/DACH-Winkel ist verteidigbar (Regulierung, Sprache, Support) — der einzige Burggraben, den ein Solo-Betreiber gegen globale Konkurrenz hat, laut `KI-Geschaeftsmodelle-10k.md` Platz 5.
5. Du kannst eine benutzbare Version in **≤14 Tagen** bauen (siehe `KI-Projektfabrik.md`).

**Die 10k-Rechnung für Schicht B:** 120 Kunden × 29 €/Monat = 3.480 € MRR. Bei ~6 % Monats-Churn (die Repo-Benchmark) heißt „halten" ~7 Neukunden/Monat. Das ist ein realistisches Zwischenziel für Monat 12–18 — nicht für Monat 6.

**Meilenstein-Gate B:** 20 zahlende Kunden innerhalb von 90 Tagen nach Launch. Verfehlt → **einmal** das Angebot/Preis/Zielgruppe ändern, dann 90 weitere Tage. Zweites Mal verfehlt → einstellen und das nächste Problem aus der Liste nehmen. Nicht endlos nachbessern.

### Schicht C — Das Distributions-Asset: SignalSpace

**Was:** Der bestehende YouTube-Kanal, im Economy/Tech-Winkel, wöchentliche Kadenz. Die Analyse dazu steht bereits vollständig in `SignalSpace-Nischen-Entscheidung.md` und ändert sich nicht.

**Was sich ändert, ist seine Rolle im System.** Bisher war er als Einnahmequelle gedacht (Erwartung dort: 500–2.000 €/Monat in Monat 12, 10k-Zone Monat 18–30). Im System hat er drei Jobs, und Geld ist der unwichtigste davon:

1. **Beweis für Schicht A.** Ein laufender Kanal mit erkennbarer Handschrift ist die glaubwürdigste Referenz, die ein Kreativ-Dienstleister haben kann — er zeigt Format-Denken, Kadenz und Qualität an einem echten Asset.
2. **Distribution für Schicht B.** Wenn das Tool launcht, hast du bereits einen Kanal, der es ausspielt. Das ist exakt der Faktor, den Gesetz 1 als den entscheidenden markiert.
3. **Eigene Einnahmen** (Ads, Sponsoring, später eigenes Produkt) — 1.000–3.000 €/Monat ab Monat 12–18, realistisch-gut.

**Das harte Zeitbudget:** Schicht C bekommt **maximal 6 h/Woche**, egal wie gut oder schlecht es läuft. Das ist keine Willkür — es ist die Konsequenz aus Gesetz 3: Schicht C hat den niedrigsten Preis pro Kunde im System und deshalb den schlechtesten €/Stunde-Wert, bis sie sehr groß ist. Ohne Deckel frisst sie das Budget der Schichten, die zahlen. Diese Deckelung ist die häufigste Regel, gegen die du verstoßen wirst, und die, die am meisten kostet.

**Und die Parfüm-TikTok-Linie?** Ehrliche Einordnung nach eigenem Faktencheck: Als Einnahmequelle ist sie der schlechteste Weg im ganzen Repo (2.000–2.500 Verkäufe für 10k, plus die Vertrauens-Mauer aus Gesetz 2). **Als Trainings- und Portfolio-Linie für Schicht A ist sie wertvoll** — du lernst Hook-Systematik, Charakter-Pipeline und Schnitt an einem echten Publikum, und jedes Video ist ein verkaufbares Arbeitsbeispiel. Führe sie so weiter, wenn sie dir Spaß macht (Motivation treibt Kadenz), aber trage sie im Cockpit unter „Schicht D: Fähigkeitsaufbau", nicht unter „Umsatz". Damit ist auch klar, wann sie stirbt: wenn sie keine Fähigkeiten mehr aufbaut.

### Schicht D — Das KI-Betriebssystem: die Fabrik selbst

**Was:** Prompts, Agenten-Rollen, Templates, Bausteinbibliothek, Cockpit. Zahlt keinen Euro direkt und ist trotzdem die Schicht, die über 12 Monate den größten Unterschied macht — weil sie die Grenzkosten *aller* anderen Schichten senkt.

Der Effekt ist multiplikativ, nicht additiv: Wenn ein Video-Asset im Monat 1 drei Stunden kostet und im Monat 6 vierzig Minuten, hast du deine Kapazität verfünffacht, ohne eine Stunde mehr zu arbeiten. **Das ist der eigentliche „Einsatz von KI im Projektaufbau"** — nicht KI, die Content macht, sondern KI, die die Maschine baut, die Content macht.

Vollständig ausgearbeitet in **`KI-Projektfabrik.md`**.

---

## Teil 3: Das Schwungrad — warum die Schichten zusammen mehr sind

Der Grund, warum das ein System ist und keine Liste von vier Nebenjobs:

| Von | Nach | Was fließt |
|---|---|---|
| C → A | Distributions-Asset → Cash-Motor | Beweis, Portfolio, gelegentlich Inbound-Anfragen |
| A → B | Cash-Motor → Produkt-Schicht | **Geld** (finanziert die Bauzeit) und **Problemkenntnis** (sagt dir, was zu bauen ist) |
| B → A | Produkt-Schicht → Cash-Motor | MRR kauft Stunden zurück → du kannst A-Aufträge ablehnen und die Preise erhöhen |
| C → B | Distributions-Asset → Produkt-Schicht | Launch-Kanal, erste Nutzer, Feedback |
| D → alle | Fabrik → alles | Grenzkosten pro Asset sinken über die Zeit gegen null |

Der wichtigste Pfeil ist **A → B**. Ohne ihn ist Schicht B Raten, und Raten ist der Grund für die 97-%-Ausfallquote in Gesetz 1. Mit ihm ist Schicht B eine informierte Wette mit bereits bezahlter Bauzeit.

---

## Teil 4: Der Pfad — Meilenstein-Gates statt Kalender

Kalenderpläne scheitern, weil sie so tun, als wäre die Reihenfolge zeitgesteuert. Sie ist zustandsgesteuert. **Du gehst zur nächsten Phase, wenn das Gate erfüllt ist — nicht, wenn der Monat um ist.**

Zwei Geschwindigkeiten, weil die Vorarbeiten widersprüchliche Annahmen über deine Zeit machen (`IndieHacker-Top5-Modelle-2026.md` sagt Vollzeitjob + ~10 h/Woche; die TikTok-Dokumente rechnen mit 15–25 h). **Stunden sind nach „nicht aufhören" der zweitgrößte Hebel im ganzen System** — deshalb hier beides ehrlich:

| Phase | Gate (Zustand, nicht Datum) | bei ~25 h/Woche | bei ~10 h/Woche |
|---|---|---|---|
| **0 — Fundament** | Gewerbe läuft, Stack steht, Cockpit befüllt, 10 Spec-Arbeiten fertig, Angebot online | Woche 1–3 | Woche 1–6 |
| **1 — Erster Euro** | 1.000 €/Monat aus Schicht A, ≥5 Bewertungen | Monat 2–4 | Monat 4–8 |
| **2 — Motor läuft** | 3.000 €/Monat aus A, davon ≥1 Retainer, 1 validiertes B-Problem | Monat 4–7 | Monat 8–14 |
| **3 — Zweite Schicht** | Schicht B live, 20 zahlende Kunden; A hält 3.000–5.000 € | Monat 7–11 | Monat 14–20 |
| **4 — Stapel schließt** | 10.000 €+ aus ≥3 Strömen, kein Strom über 60 % | Monat 11–18 | Monat 20–30 |

**Phase 0 im Detail** (das ist die einzige Phase, die du sofort komplett ausführen kannst):

1. Gewerbeanmeldung (15–65 €) + Fragebogen zur steuerlichen Erfassung + USt-IdNr beantragen. **Vor** dem ersten Euro — kommerzielle Absicht besteht ab Start.
2. Geschäftskonto, Buchhaltungstool, Steuer-Rücklagenkonto (Regel: 40 % jeder Einnahme sofort umbuchen).
3. Tool-Stack aufsetzen und deckeln (siehe unten).
4. Cockpit aus `Betriebssystem-Cockpit.md` anlegen und mit Nullwerten befüllen.
5. Die fünf Standing-Prompts aus `KI-Projektfabrik.md` anlegen und testen.
6. **10 Spec-Arbeiten produzieren** — das ist die eigentliche Arbeit dieser Phase und der Grund, warum Phase 1 überhaupt starten kann.
7. Angebot veröffentlichen: Marktplatz-Profil + eine eigene einseitige Angebotsseite mit Preisen. Preise sichtbar machen — das filtert vor und ersetzt Verkaufsgespräche.

---

## Teil 5: Budget — Zeit und Geld

**Zeitverteilung (bei 25 h/Woche, Phase 1–2):**

| Schicht | Stunden/Woche | Anteil |
|---|---|---|
| A — Cash-Motor (Lieferung + Angebotspflege) | 12 h | 48 % |
| B — Produkt (ab Phase 2; vorher 0) | 4 h | 16 % |
| C — Distributions-Asset | **max. 6 h** | 24 % |
| D — Fabrik (Templates, Automatisierung, Cockpit) | 3 h | 12 % |

Bei 10 h/Woche: A bekommt 6 h, C bekommt 2 h, D bekommt 2 h, B startet erst nach Gate 2. **Nicht alles anteilig kürzen** — das ergibt vier halbtote Schichten. Lieber zwei Schichten richtig.

**Laufende Kosten (Planwerte):**

| Posten | €/Monat |
|---|---|
| KI-Modelle + Coding-Umgebung | 60–120 |
| Video-/Audio-/Bild-Tools | 80–150 |
| Hosting, Domains, Mail | 20–40 |
| Buchhaltung, Impressum-Service | 30–50 |
| Werbebudget (erst ab Phase 2, nur auf Bewiesenes) | 0–300 |
| **Summe** | **190–660** |

**Kapitalbedarf:** 2.500–4.000 € Puffer für 12 Monate. Der wichtigste Satz aus `KI-Geschaeftsmodelle-10k.md`: *„Plane die Kosten so, dass du 9–12 Monate durchhältst — das ist statistisch der größte Erfolgsfaktor."* Das gilt hier unverändert.

**Die Tool-Regel:** Jedes Abo braucht eine Schicht, der es zugeordnet ist, und stirbt, wenn diese Schicht stirbt. Monatlicher Cockpit-Check. Tool-Kosten sind die leiseste Art, ein Geschäft unprofitabel zu machen.

---

## Teil 6: Was Deutschland bei 10k/Monat verlangt

Bei 10.000 €/Monat = 120.000 €/Jahr ändert sich die Rechtslage gegenüber dem Start deutlich. Das gehört ins System, nicht in eine spätere Panik-Woche:

- **Kleinunternehmerregelung endet.** § 19 UStG greift bis 25.000 € Vorjahr / 100.000 € laufendes Jahr. Bei diesem Ziel ist Regelbesteuerung von Anfang an der richtige Weg — inkl. USt-Voranmeldung (im Gründungsjahr regelmäßig monatlich) und USt-IdNr für EU-B2B.
- **Reverse-Charge bei ausländischen Plattformen** (Fiverr, Shopify u. ä.): Leistung wird ohne deutsche USt abgerechnet, du musst sie korrekt erklären. Das ist Routine, aber es muss ab Rechnung 1 richtig laufen.
- **Rücklage 40–45 %** jeder Einnahme sofort auf ein separates Konto (Einkommensteuer + Gewerbesteuer + USt-Zahllast). Die zweite Jahreshälfte des zweiten Jahres ist der klassische Punkt, an dem Vorauszahlungen plus Nachzahlung gleichzeitig kommen.
- **Rechtsform:** Einzelunternehmen reicht bis in den mittleren fünfstelligen Jahresgewinn. Ab ~60–80k Gewinn lohnt die Prüfung einer UG/GmbH (Haftung, Thesaurierung) — mit Steuerberater, nicht mit KI.
- **Urheberrecht an KI-Output — der Punkt, der in Schicht A wirklich zählt.** Rein KI-generierte Inhalte haben in Deutschland mangels menschlicher Schöpfung typischerweise keinen Urheberrechtsschutz. Für dich heißt das: Du kannst einem Kunden keine exklusiven Urheberrechte an etwas übertragen, an dem keine bestehen. Das muss vertraglich sauber geregelt sein (Nutzungsrechte, Exklusivitätszusagen, Haftung). **Ein Anwalt für einen einmaligen AGB-/Vertragscheck ist hier die beste 300–600 € im ganzen System.**
- **Scheinselbstständigkeit** bei Retainern: mehrere Kunden, eigene Betriebsmittel, eigene Preisgestaltung, keine Weisungsgebundenheit. Bei 4 Retainern unkritisch, bei 1 großem Kunden relevant.
- **Werbekennzeichnung, Impressum (§ 5 DDG), KI-Kennzeichnung (EU AI Act Art. 50 ab 02.08.2026)** — unverändert aus den Vorarbeiten, gilt für alles Öffentliche.

*Kein Rechts- oder Steuerrat — das sind die Punkte, die du mit Steuerberater und Anwalt klären musst. Ein Steuerberater ab Phase 1 kostet 80–200 €/Monat und ist bei diesem Ziel keine Option, sondern Infrastruktur.*

---

## Teil 7: Risikoregister

| Risiko | Wirkung | Gegenmaßnahme im System |
|---|---|---|
| **Du hörst in Monat 4–7 auf** | Totalverlust | Der mit Abstand größte. Gegenmittel: Meilenstein-Gates statt Kalender (kein „ich bin hinter dem Plan"-Gefühl), 12-Monats-Runway, Schicht A liefert früh sichtbaren Cash |
| Plattform-Sperre (TikTok/YouTube/Marktplatz) | Ein Strom auf null | Kein Strom über 60 % des Umsatzes; alles Produzierte lokal archiviert; Kundenkontakte außerhalb der Plattform |
| Preisverfall bei KI-Kreativarbeit | Schicht A schrumpft | Nach oben verkaufen: Strategie, Testmatrix, Rechtssicherheit, DACH-Sprache — nie über Preis konkurrieren; früh in Retainer überführen |
| Schicht A frisst alle Stunden | B startet nie | Hartes Stundenlimit auf A ab Gate 2; Preiserhöhung statt Mehrarbeit; Auftragsablehnung ist ein Erfolgssignal |
| Falsches B-Problem gebaut | 6 Wochen weg | Der 5-Punkte-Filter; ≤14-Tage-Sprint; 90-Tage-Gate mit exakt einem Nachbesserungsversuch |
| Regulatorik (AI Act, Plattform-Policies) | Format wird unbrauchbar | Kennzeichnung ab Tag 1; keine Modelle, deren Existenz von Nicht-Kennzeichnung abhängt |
| KI-Halluzination in einer Kundenlieferung | Reputations- und Rechtsschaden | Der Prüfer-Schritt in jedem Sprint (`KI-Projektfabrik.md`) — KI hat nie das letzte Wort bei Fakten, Recht, Freigabe |
| Tool-Kosten wachsen unbemerkt | Marge stirbt leise | Monatlicher Tool-Audit im Cockpit; jedes Abo hat eine zugeordnete Schicht |

---

## Teil 8: Die ehrliche Wahrscheinlichkeit

Deine bisherigen Dokumente haben pro Einzelmodell 4–12 % auf 10k in Monat 6 kalibriert und den realistischen Durchbruch bei Monat 9–15 verortet. Dieses System ändert die Physik nicht — es ändert drei Dinge, und nur die:

1. **Es startet beim höchsten Preispunkt** (Gesetz 3) → weniger Distribution nötig → früherer Cash → längerer Atem.
2. **Es stapelt drei Ströme** statt auf einen zu setzen → 10k besteht aus 3.500 + 3.500 + 3.000, nicht aus einem 10k-Treffer.
3. **Es hat Gates und Kill-Regeln** → Verlierer sterben in 90 Tagen statt in 12 Monaten → mehr Versuche pro Jahr bei gleichem Zeitbudget.

**Meine kalibrierte Einschätzung** — konsistent mit den Basisraten deiner eigenen Recherche, ausdrücklich Urteil und keine Messung:

| Zeitpunkt | 25 h/Woche | 10 h/Woche |
|---|---|---|
| 3.000 €/Monat | Monat 6–9 · ~50 % | Monat 12–16 · ~35 % |
| **10.000 €/Monat** | **Monat 12–18 · ~25–30 %** | **Monat 20–30 · ~12–18 %** |
| 10.000 €/Monat innerhalb von 6 Monaten | ~5 % | <2 % |

Die 6-Monats-Zahl ist kein Planwert, sondern der Ausreißer — bei jedem Modell und auch hier. Wer dir etwas anderes verkauft, verkauft dir einen Kurs; dieser Satz stand schon in deinem ersten Dokument und ist nach zehn Recherchen unverändert richtig.

**Was diese Zahlen wirklich sagen:** Die häufigste Todesursache ist nicht die falsche Modellwahl. Sie ist Monat 5, wenn 800 € auf dem Konto stehen statt der erhofften 4.000, und der Plan „ab Monat 6: 10k" sagt, dass du gescheitert bist. Du bist dann nicht gescheitert — du bist im Median. Genau dafür sind die Gates da: Sie messen Zustände, die du kontrollierst, nicht Daten, die du nicht kontrollierst.

---

## Der Kern in fünf Sätzen

1. Produktion ist gratis, Distribution ist der Engpass — also darf Bauzeit niemals unbegrenzt sein.
2. KI-Output wird bezahlt, wo kein Fremder einem Menschen vertrauen muss — Aufmerksamkeit, B2B-Artefakte, Software; nicht: physische Produkte an Fremde verkaufen.
3. Der Preis pro Kunde bestimmt die nötige Reichweite — fünf Retainer-Kunden ersetzen 2.500 Affiliate-Verkäufe, also **baue von oben nach unten**.
4. 10k entsteht als Stapel aus drei Strömen mit verschiedenen Zeitprofilen, die sich gegenseitig finanzieren — nicht als ein Treffer.
5. Der einzige Faktor, der jede Wahrscheinlichkeit in diesem Dokument dominiert, ist, ob du in Monat 7 noch da bist.

---

**Weiter:** `KI-Projektfabrik.md` (wie KI die Assets baut) → `Betriebssystem-Cockpit.md` (der Wochenrhythmus, die Kennzahlen, die Gates).

*Marktdaten und Fallzahlen in diesem Dokument stammen ausschließlich aus den bereits recherchierten Dokumenten dieses Repos (jeweils benannt). Alle Preise, Zeitbudgets, Rampen und Wahrscheinlichkeiten sind Rechnung oder kalibriertes Urteil und als solche markiert — sie sind Planungswerte, keine Messwerte. Rechts- und Steuerhinweise sind Orientierung, kein Rat.*
