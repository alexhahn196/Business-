# Die KI-Projektfabrik

**Wie mit KI Projekte gebaut werden — die Produktionsmaschine hinter dem 10k-Betriebssystem**

*Stand: 27.07.2026 · Teil 2 von 3 · Voraussetzung: `KI-System-10k-Betriebssystem.md` · Danach: `Betriebssystem-Cockpit.md`*

---

## Das Prinzip in einem Satz

**KI baut nicht dein Produkt — KI baut die Fabrik, die deine Produkte baut.**

Der Unterschied ist der ganze Hebel. Wer KI benutzt, um ein Video zu machen, spart eine Stunde. Wer KI benutzt, um eine Video-Pipeline zu bauen, spart jede Stunde danach. Das erste ist ein Werkzeug, das zweite ist ein Vermögenswert — und nur das zweite erklärt, warum ein Solo-Betreiber vier Umsatzströme gleichzeitig führen kann.

Die Zielgröße, an der du die Fabrik misst: **Grenzkosten pro Asset.** Wenn dasselbe Asset in Monat 6 ein Fünftel der Zeit kostet wie in Monat 1, hast du deine Kapazität verfünffacht, ohne eine Stunde länger zu arbeiten. Das ist die einzige Form von Skalierung, die einem Einzelnen offensteht.

---

## Teil 1: Die fünf Rollen

Nicht „ich frage die KI was". Fünf klar getrennte Rollen mit festen Aufträgen, festen Ausgabeformaten und — das ist das Entscheidende — **fester Befugnis, was sie entscheiden dürfen und was nicht.**

| Rolle | Auftrag | Ausgabe | Darf entscheiden | Darf **nie** entscheiden |
|---|---|---|---|---|
| **Scout** | Problem finden und belegen | Entscheidungs-Memo mit Belegen **und Gegenthese** | nichts — liefert nur Material | ob gebaut wird |
| **Architekt** | Umfang festlegen | Spezifikation + Abnahmekriterien + Erfolgsmetrik | Schnitt und Reihenfolge | ob das Problem echt ist |
| **Builder** | Bauen | lauffähiges Asset | technische Umsetzung | Umfangserweiterungen |
| **Operator** | Betreiben | Templates, Texte, Abläufe, Support-Bausteine | Formulierungen, Varianten | Preise, Zusagen an Kunden |
| **Prüfer** | Widerlegen | Mängelliste nach Schwere | nichts — liefert Einwände | ob freigegeben wird |

**Die eine Regel, die alles trägt:**

> **KI hat nie das letzte Wort bei Fakten, Recht und Freigabe.**

Das ist keine Vorsicht, es ist die Lehre aus deinen eigenen Recherchen: halluzinierte Produktdetails = „Produkt nicht wie beschrieben" = Strike (`TikTok-Shop-Machbarkeitsanalyse.md`); erfundene Vergleichsaussagen = Abmahnung nach § 6 UWG (`TikTok-Start-0-auf-1000-Playbook.md`); KI-Ich-Form-Bewertungen = Fake-Testimonial. Jeder dieser Fälle kostet mehr als alles, was die Automatisierung je eingespart hat.

### Die fünf Standing-Prompts

Einmal anlegen, immer wiederverwenden. `{…}` ausfüllen.

**1 — Scout**

```
Rolle: Skeptischer Rechercheur. Du arbeitest gegen mich, nicht für mich.

Auftrag: Prüfe die Idee "{IDEE}" für {ZIELGRUPPE} im Markt {MARKT}.

Liefere in genau dieser Reihenfolge:
1. NACHFRAGEBELEG: Wer zahlt heute nachweislich für die Lösung dieses
   Problems, und wie viel? Nur belegbare Quellen mit Datum.
   Wenn du keinen Beleg findest, schreibe "kein Nachfragebeleg gefunden" —
   erfinde nichts und leite nichts aus Plausibilität ab.
2. WETTBEWERB: Wer macht es bereits? Preise, Größe, Schwächen.
3. GEGENTHESE: Die drei stärksten Gründe, warum das NICHT funktioniert.
   Nimm diesen Teil ernster als Teil 1.
4. TÖTUNGS-TEST: Welche eine Tatsache, wenn wahr, macht die Idee wertlos?
   Wie prüfe ich sie in unter 2 Stunden?
5. VERDIKT: bauen / nicht bauen / erst {TEST} durchführen.

Markiere jede Zahl als [belegt: Quelle+Datum], [geschätzt] oder [Annahme].
Unbelegte Zahlen sind schlimmer als gar keine.
```

**2 — Architekt**

```
Rolle: Produkt-Architekt mit hartem Umfangs-Budget.

Eingabe: {SCOUT-MEMO}
Budget: {X} Arbeitstage, eine Person, KI-gestützt.

Liefere:
1. KLEINSTE NÜTZLICHE VERSION: Was ist das Minimum, für das jemand
   heute zahlen würde? Nicht das Minimum, das lauffähig ist.
2. AUSDRÜCKLICH NICHT DABEI: Liste von 10 Dingen, die verlockend sind
   und in Version 1 nicht vorkommen.
3. ABNAHMEKRITERIEN: 5-8 prüfbare Sätze der Form "Ein Nutzer kann X,
   und das Ergebnis ist Y." Keine Absichtserklärungen.
4. ERFOLGSMETRIK: Die eine Zahl, die nach 30 Tagen entscheidet, plus
   der Schwellenwert, ab dem weitergebaut wird.
5. BAUREIHENFOLGE: Riskantestes zuerst. Was am ehesten scheitert,
   wird zuerst gebaut, nicht zuletzt.

Wenn der Umfang nicht ins Budget passt, kürze den Umfang.
Verlängere nie das Budget.
```

**3 — Builder** (an Claude Code / die Coding-Umgebung)

```
Kontext: {SPEZIFIKATION}. Ich bin Einzelbetreiber, ich muss das in
6 Monaten noch selbst warten können.

Regeln:
- Langweilige, verbreitete Technik. Keine Frameworks, die du erklären musst.
- Jeder Schritt lauffähig und benutzbar — kein Big-Bang am Ende.
- Fehler laut und sichtbar, nicht still abgefangen.
- Keine Funktion, die nicht in den Abnahmekriterien steht.
- Zeig mir nach jedem Abschnitt, wie ich es selbst prüfe.

Beginne mit dem riskantesten Teil laut Baureihenfolge.
Bevor du baust: nenne die Annahmen, die du triffst, in 5 Zeilen.
```

**4 — Operator**

```
Rolle: Betriebsleiter. Du machst aus einem gebauten Ding ein
betreibbares Ding.

Eingabe: {ASSET}, Zielgruppe {ZIELGRUPPE}, Tonalität {TON}.

Liefere:
1. Angebotsseite: Überschrift, 3 Nutzenversprechen, Preise, FAQ (8 Fragen),
   Einwandbehandlung (5 häufigste).
2. Ablauf vom Auftrag bis zur Lieferung als Checkliste — jeder Schritt
   entweder [automatisch] oder [ich, X Minuten].
3. 10 Support-Textbausteine für die wahrscheinlichsten Anfragen.
4. Erste 10 Inhalte/Assets nach demselben Muster.

Keine Superlative, keine Erfolgsversprechen, keine Zahlen, die ich nicht
belegen kann. Deutsche Rechtslage: keine Wirkversprechen, keine
Vergleichswerbung gegen benannte Marken.
```

**5 — Prüfer**

```
Rolle: Gegner. Dein Auftrag ist, dieses Asset zu zerstören,
bevor ein Kunde es tut.

Eingabe: {ASSET/LIEFERUNG}

Prüfe getrennt und liefere je eine Mängelliste, sortiert nach Schwere:
A) FAKTEN: Jede überprüfbare Behauptung — belegt, falsch oder unbelegt?
   Unbelegt zählt als Mangel.
B) RECHT (Deutschland): Werbekennzeichnung, Impressum, KI-Kennzeichnung,
   Vergleichswerbung/§ 6 UWG, Heilversprechen, Marken- und Namensnutzung,
   Nutzungsrechte an Fremdmaterial.
C) QUALITÄT: Wo sieht/klingt das nach Massenware? Wo würde ein Kunde
   sagen "das hätte ich auch selbst gekonnt"?
D) VERSPRECHEN: Sage ich irgendwo etwas zu, das ich nicht halten kann?

Für jeden Mangel: Schweregrad (blockierend / wichtig / kosmetisch)
und die kleinste Korrektur, die ihn behebt.
Sag ausdrücklich "keine blockierenden Mängel", wenn es so ist —
aber suche zuerst ernsthaft.
```

---

## Teil 2: Der 14-Tage-Sprint

Jedes Asset im System — ein neues Dienstleistungsangebot, ein Tool, eine Content-Serie, eine interne Automatisierung — entsteht im gleichen Takt. Immer 14 Tage. Wenn es nicht in 14 Tage passt, war der Umfang falsch, nicht die Frist.

| Tag | Rolle | Ergebnis | Abbruchpunkt |
|---|---|---|---|
| **1–2** | Scout | Entscheidungs-Memo mit Nachfragebeleg und Gegenthese | **Kein Nachfragebeleg → Ende.** Hier stirbt die Mehrheit — und das ist der billigste Tod im ganzen System |
| **3** | Architekt | Spezifikation, Abnahmekriterien, Erfolgsmetrik, Baureihenfolge | Umfang passt nicht in 14 Tage → kürzen, nicht verlängern |
| **4–8** | Builder | benutzbare Version, alle Abnahmekriterien erfüllt | Riskantester Teil funktioniert an Tag 6 nicht → Ende |
| **9–10** | Operator | Angebotsseite, Ablauf, Textbausteine, erste 10 Inhalte | — |
| **11–12** | Prüfer + du | Mängelliste abgearbeitet, blockierende Mängel = null | blockierender Rechtsmangel ohne Lösung → Ende |
| **13** | du | Veröffentlichung. Messpunkt im Cockpit eingetragen | — |
| **14** | du | Rückblick: Was wandert in die Bausteinbibliothek? | — |

**Danach: 30 Tage messen, nicht anfassen.** Dann das Gate aus dem Cockpit. Der häufigste teure Fehler ist Nachbessern in Woche 3, bevor irgendein Signal da ist.

### Warum Tag 1–2 die wichtigsten sind

Der Bau ist billig geworden — deshalb ist die Versuchung, sofort zu bauen, größer als je zuvor. Genau das beschreibt Levels' „KI-Fabriken ohne Traffic" aus deiner Indie-Hacker-Recherche. **Ein Scout-Memo, das mit „kein Nachfragebeleg gefunden" endet, ist ein voller Erfolg des Sprints** — es hat dir zwölf Tage gespart. Zähle im Cockpit mit, wie viele Sprints an Tag 2 sterben. Wenn die Quote unter 40 % liegt, bist du zu nachsichtig mit deinen eigenen Ideen.

---

## Teil 3: Die Bausteinbibliothek — der Teil, der compoundet

Nach jedem Sprint wandert alles Wiederverwendbare in eine Bibliothek. Das ist der Mechanismus, der Sprint Nr. 8 dreimal schneller macht als Sprint Nr. 1.

| Kategorie | Inhalt | Wird wiederverwendet von |
|---|---|---|
| **Prompts** | Die fünf Rollen + jede bewährte Spezialisierung | allen Schichten |
| **Hook-Bibliothek** | Jeder Hook mit gemessener Completion/CTR, sortiert nach Typ | Schicht A und C |
| **Video-Templates** | Schnittvorlagen, Untertitel-Stile, Intros, Charakter-Presets, eingefrorene Stimmen | Schicht A und C |
| **Code-Bausteine** | Auth, Abrechnung, Onboarding, Mail, Admin-Ansicht — einmal gebaut, nie wieder | Schicht B |
| **Texte** | Angebotsseiten, Angebote, FAQ, Support-Bausteine, Rechnungstexte | Schicht A und B |
| **Rechts-Bausteine** | Kennzeichnungshinweise, AGB-Kern, Nutzungsrechte-Klauseln (anwaltlich einmal geprüft) | allen Schichten |
| **Checklisten** | Abnahme, Veröffentlichung, Prüfer-Durchlauf | allen Schichten |

**Die Regel:** Was du zum zweiten Mal machst, wird beim zweiten Mal zum Baustein — nicht beim dritten. Und `TikTok-Start-0-auf-1000-Playbook.md`, Review-Punkt 8, hat den Grund schon genannt: Bei Account- oder Datenverlust ist der Neustart dann ein Wiederhochladen statt ein Neuaufbau.

---

## Teil 4: Grenzkosten — was die Fabrik konkret bringt

Planwerte für ein typisches Asset, Erfahrungswerte aus den Repo-Dokumenten plus Rechnung. Der Punkt ist nicht die exakte Zahl, sondern die Kurve:

| Asset | ohne Fabrik | Sprint 1 | ab Sprint 5 (Bibliothek greift) |
|---|---|---|---|
| Werbevideo-Variante | 3–5 h | 60–90 min | **10–20 min** |
| Vollständiges Kundenpaket (8 Varianten) | 2–3 Tage | 6–8 h | **3–4 h** |
| Landing- / Angebotsseite | 1–2 Tage | 4 h | **45 min** |
| Kleines Tool (benutzbare Version) | Wochen | 5–8 Tage | **3–5 Tage** |
| Kanal-Episode (Recherche → fertig) | 8–12 h | 5 h | **3 h** |

Der wirtschaftliche Effekt, an Schicht A gerechnet: Ein Standard-Paket zu 449 € bei 6 h Aufwand sind 75 €/Stunde. Dasselbe Paket bei 3,5 h sind 128 €/Stunde. **Ohne einen Cent Preiserhöhung und ohne eine Stunde Mehrarbeit ist das der Unterschied zwischen einem Nebenverdienst und einem Geschäft.**

---

## Teil 5: Die Fabrik pro Schicht

**Schicht A (Cash-Motor):** Die Fabrik ist die Lieferpipeline. Kunde schickt Briefing → Scout-Kurzfassung (Marke, Zielgruppe, Wettbewerbs-Hooks) → Skript- und Hook-Varianten aus der Bibliothek → Produktion aus Templates → **Prüfer-Durchlauf mit Schwerpunkt Recht und Markenkonformität** → deine Freigabe → Lieferung. Der Prüfer-Schritt ist bei Kundenarbeit nicht optional; ein falscher Claim in einem Kundenvideo ist dessen Problem und dein Ruf.

**Schicht B (Produkt):** Der 14-Tage-Sprint in Reinform. Wichtigster Baustein: die Code-Bibliothek — Anmeldung, Abrechnung, Onboarding werden genau einmal gebaut. Ab dem zweiten Tool ist der Sprint überwiegend Fachlogik.

**Schicht C (Distributions-Asset):** Recherche und Faktenprüfung sind hier der Engpass, nicht die Produktion. Für `SignalSpace` heißt das konkret: Der Scout liefert Behauptung, Belege und Gegenbelege inklusive Quellen mit DOI/Datum; der Prüfer prüft jede Aussage gegen die Quelle; die Verdict-Entscheidung triffst du. Genau diese Arbeitsteilung erzeugt die „erkennbare eigene Handschrift und originelle Recherche", die laut `SignalSpace-Nischen-Entscheidung.md` die KI-Slop-Säuberungen überlebt — und sie ist der Grund, warum der Kanal gleichzeitig das beste Arbeitsbeispiel für Schicht A ist.

**Schicht D (die Fabrik selbst):** Jede Woche 2–3 Stunden. Nicht mehr, aber auch nie null. Reihenfolge: erst die Handgriffe automatisieren, die du am häufigsten machst — nicht die, die am interessantesten sind.

---

## Teil 6: Die sechs Fehler, die Automatisierung teuer machen

1. **Automatisieren, bevor etwas funktioniert.** Erst manuell fünfmal machen, dabei den Ablauf aufschreiben, dann automatisieren. Ein automatisierter falscher Prozess produziert Müll schneller.
2. **KI ohne Belegpflicht fragen.** Antworten ohne „[belegt: Quelle+Datum] / [geschätzt] / [Annahme]" sind Rohmaterial, keine Grundlage. Der Scout-Prompt erzwingt das aus genau diesem Grund.
3. **Den Prüfer-Schritt überspringen, weil es eilig ist.** Er dauert 20 Minuten. Eine Abmahnung dauert Monate.
4. **Umfang wächst während des Sprints.** „Wenn wir schon dabei sind" ist der Satz, der aus 14 Tagen sechs Wochen macht. Neue Ideen kommen auf die Liste für den nächsten Sprint, nicht in diesen.
5. **Werkzeuge sammeln statt Bausteine bauen.** Jedes neue Tool kostet Abo, Einarbeitung und Aufmerksamkeit. Ein Baustein in der eigenen Bibliothek kostet einmal Zeit und dann nichts mehr.
6. **Die Fabrik selbst nie warten.** Prompts veralten, Templates werden zu Gewohnheiten, Bausteine sammeln Ballast. Ein Fabrik-Tag pro Quartal: aussortieren, zusammenfassen, neu messen.

---

## Der Kern in vier Sätzen

Fünf Rollen mit klaren Befugnissen ersetzen „ich frage mal die KI" — und die wichtigste Befugnis ist die, die keine Rolle hat: über Fakten, Recht und Freigabe entscheidest du. Jedes Projekt läuft im gleichen 14-Tage-Takt, und ein Sprint, der an Tag 2 stirbt, ist ein Gewinn, kein Verlust. Alles Wiederverwendbare wandert beim zweiten Mal in die Bausteinbibliothek — das ist der einzige Grund, warum Sprint 8 dreimal schneller ist als Sprint 1. Und der ganze Zweck der Fabrik ist eine einzige Zahl: die Zeit pro Asset, gemessen im Cockpit, Monat für Monat fallend.

---

**Weiter:** `Betriebssystem-Cockpit.md` — der Wochenrhythmus, die Kennzahlen und die Gates, die entscheiden, wohin die Stunden gehen.

*Alle Zeit- und Kostenwerte sind Planungsgrößen aus Rechnung und Erfahrungswerten der Repo-Dokumente, keine Messwerte. Rechtshinweise sind Orientierung, kein Rat — den AGB-, Nutzungsrechte- und Kennzeichnungs-Baustein einmal anwaltlich prüfen lassen.*
