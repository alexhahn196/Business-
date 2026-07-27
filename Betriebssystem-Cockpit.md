# Das Cockpit

**Der Wochenrhythmus, die Kennzahlen und die Gates — wie das 10k-Betriebssystem gesteuert wird**

*Stand: 27.07.2026 · Teil 3 von 3 · Voraussetzung: `KI-System-10k-Betriebssystem.md` und `KI-Projektfabrik.md` · Tabellenvorlage: `Cockpit-Vorlage.csv`*

---

## Wozu das hier da ist

Die Architektur sagt, was gebaut wird. Die Fabrik sagt, wie. Das Cockpit beantwortet die einzige Frage, die du jede Woche wirklich zu entscheiden hast:

> **Wohin gehen meine nächsten 20 Stunden?**

Alles andere in diesem Dokument dient dieser Frage. Ein Cockpit, das mehr misst, als für diese Entscheidung nötig ist, ist Beschäftigungstherapie — deshalb sind es zwölf Zahlen und nicht vierzig.

---

## Teil 1: Die Leitkennzahl

Es gibt genau eine Zahl, die über die Stundenverteilung entscheidet:

> **€ pro investierter Stunde, je Schicht, rollierend über 90 Tage.**

Warum rollierend über 90 Tage: Ein einzelner Monat ist bei Hit-getriebenen Strömen reines Rauschen. Warum je Schicht: Weil der Gesamtumsatz dir nie sagt, welche Stunde ihn verursacht hat. Warum überhaupt pro Stunde: Weil Stunden deine einzige wirklich knappe Ressource sind — Geld kannst du nachlegen, Werkzeuge kaufen, Zeit nicht.

**Was die Zahl typischerweise zeigt** (und was fast immer überrascht):

| Schicht | € / Stunde, Phase 1–2 | € / Stunde, Phase 3–4 |
|---|---|---|
| A — Cash-Motor | 40–80 € | 120–250 € |
| B — Produkt | **negativ** (nur Kosten) | 100–400 € und steigend |
| C — Distributions-Asset | **0–5 €** | 20–60 € |
| D — Fabrik | nicht direkt messbar | wirkt über alle anderen |

Schicht C ist in Phase 1 rechnerisch fast wertlos. **Das ist kein Argument, sie zu streichen** — sie zahlt über Beweis und Distribution auf A und B ein, und sie compoundet. Es ist das Argument für den harten 6-Stunden-Deckel. Wer diese Zahl nie ausrechnet, verschiebt schleichend Stunden dorthin, wo die Arbeit am angenehmsten ist, statt dorthin, wo sie zahlt. Das ist der häufigste stille Systemfehler.

**Schicht D ist die Ausnahme von der Regel.** Sie hat keinen eigenen €/Stunde-Wert und bekommt ihre 2–3 Stunden trotzdem jede Woche. Ihr Erfolgsmaß ist ein anderes: die fallende Zeit pro Asset in allen anderen Schichten.

---

## Teil 2: Die zwölf Kennzahlen

Mehr braucht es nicht. Erfassung: wöchentlich, Auswertung: monatlich.

**Global (4)**

| # | Kennzahl | Warum |
|---|---|---|
| 1 | **Umsatz gesamt** (€/Monat) | das Ziel |
| 2 | **Deckungsbeitrag** (Umsatz − Tool- und Werbekosten) | Umsatz ohne Marge ist ein Hobby mit Buchhaltung |
| 3 | **Investierte Stunden gesamt**, aufgeteilt nach Schicht | die Eingangsgröße der Leitkennzahl |
| 4 | **Runway** (Monate, die du ohne Einnahmen durchhältst) | der einzige Wert, der über Abbruch entscheidet |

**Schicht A — Cash-Motor (3)**

| # | Kennzahl | Zielwert Phase 2 |
|---|---|---|
| 5 | **Anfragen pro Woche** (Inbound) | ≥5 |
| 6 | **Anfrage → Auftrag** (%) | ≥25 % |
| 7 | **Retainer-Anteil am A-Umsatz** (%) | ≥50 % |

Kennzahl 7 ist die wichtigste des ganzen Cockpits nach der Leitkennzahl. Ein Cash-Motor ohne Retainer-Anteil ist ein Job — er fängt jeden Monat bei null an. Der Weg von 3.000 € auf 8.000 € in Schicht A führt fast nie über mehr Aufträge, sondern über die Umwandlung bestehender Kunden in wiederkehrende.

**Schicht B — Produkt (3)**

| # | Kennzahl | Zielwert nach Launch |
|---|---|---|
| 8 | **MRR** | Gate: 20 zahlende in 90 Tagen |
| 9 | **Besucher → zahlend** (%) | ≥1 % |
| 10 | **Monats-Churn** (%) | ≤7 % |

**Schicht C — Distributions-Asset (2)**

| # | Kennzahl | Zielwert |
|---|---|---|
| 11 | **Veröffentlichungen pro Woche** (Kadenz) | exakt der versprochene Takt, ohne Ausnahme |
| 12 | **Bestes Qualitätssignal der Plattform** (CTR × Wiedergabedauer bzw. Completion + Speicherungen) | steigend über 8 Wochen |

Nicht Follower, nicht Views. Beides sind Ergebnisse, keine Steuergrößen. Kadenz und Qualitätssignal sind das, was du kontrollierst — genau die Unterscheidung, die `TikTok-Start-0-auf-1000-Playbook.md` bereits getroffen hat („nicht auf Views allein starren").

---

## Teil 3: Der Rhythmus

### Täglich — 10 Minuten, am Ende des Arbeitsblocks

Drei Zeilen in die Vorlage: Stunden je Schicht, was fertig wurde, was blockiert. Das ist alles. Die Stundenerfassung ist der unbeliebteste Teil des Systems und die Voraussetzung für die einzige Kennzahl, die zählt — ohne sie ist das Cockpit Dekoration.

### Wöchentlich — Montag, 30 Minuten

1. Zwölf Kennzahlen eintragen (10 min).
2. Leitkennzahl je Schicht ausrechnen (5 min).
3. **Die Stundenverteilung für diese Woche festlegen** (10 min) — das ist der eigentliche Zweck des Termins.
4. Eine Sache benennen, die diese Woche fertig werden muss (5 min).

Regel für Schritt 3: **Verschiebe pro Woche höchstens 20 % der Stunden.** Ruckartige Umverteilung nach einer guten oder schlechten Woche ist Rauschen-Folgen, und Rauschen-Folgen ist die zuverlässigste Art, nie etwas zu Ende zu bringen.

### Monatlich — 90 Minuten

1. Monatsabschluss: Umsatz, Deckungsbeitrag, Stunden, €/Stunde je Schicht.
2. **Gate-Prüfung** (siehe Teil 4).
3. **Tool-Audit:** Jedes Abo — welcher Schicht dient es, was hat es diesen Monat verdient? Ungenutzt oder verwaist → kündigen. Sofort, nicht „nächsten Monat".
4. Steuer-Rücklage prüfen: 40 % jeder Einnahme auf dem separaten Konto?
5. Fabrik-Blick: Ist die Zeit pro Asset gefallen? Wenn nein — welcher Baustein fehlt?

### Quartalsweise — ein halber Tag

1. **Portfolio-Entscheidung:** Welche Schicht bekommt im nächsten Quartal mehr Stunden, welche weniger? Auf Basis der 90-Tage-Leitkennzahl, nicht auf Basis des Gefühls.
2. **Fabrik-Wartung:** Prompts durchgehen, Bausteine aussortieren, Bibliothek aufräumen.
3. **Der ehrliche Blick:** Bin ich weiter im System, oder mache ich nur noch das, was Spaß macht? (Häufigste Antwort in Quartal 2: Schicht C hat sich unbemerkt 12 Stunden genommen.)
4. Runway neu rechnen.

---

## Teil 4: Das Gate-Protokoll

Gates sind Zustände, keine Termine. Sie werden monatlich geprüft und haben genau drei mögliche Ausgänge.

### Die Gates

| Gate | Bedingung | Bei Erfüllung |
|---|---|---|
| **A1 — Erster Euro** | 1.000 €/Monat aus Schicht A, ≥5 Bewertungen | Preise um 20–30 % erhöhen, Einstiegspaket streichen |
| **A2 — Motor läuft** | 3.000 €/Monat aus A, ≥1 Retainer | Stundenlimit auf A setzen; Schicht B starten |
| **A3 — Motor trägt** | 5.000 €/Monat aus A, Retainer-Anteil ≥50 % | A-Stunden einfrieren; alle Zusatzstunden in B |
| **B1 — Produkt validiert** | 20 zahlende Kunden binnen 90 Tagen nach Launch | weiterbauen, Distribution über C verstärken |
| **B2 — Produkt trägt** | 2.000 € MRR, Churn ≤7 % | A-Aufträge selektiv ablehnen, Preise weiter erhöhen |
| **C1 — Asset trägt** | Qualitätssignal 8 Wochen steigend, Monetarisierung erreicht | Deckel von 6 h auf 8 h erhöhen — mehr nicht |
| **Z — Ziel** | 10.000 €/Monat, kein Strom über 60 % | Konzentrationsrisiko prüfen, Rechtsform prüfen |

### Die drei Ausgänge

**1. Erfüllt → skalieren.** Die Handlung steht in der Tabelle. Nicht „weiter so", sondern die konkrete nächste Stufe.

**2. Verfehlt, erster Durchgang → eine Sache ändern, 90 Tage neu.** Genau eine: Angebot, Preis oder Zielgruppe. Wer zwei Dinge gleichzeitig ändert, weiß danach nicht, welche gewirkt hat.

**3. Verfehlt, zweiter Durchgang → Stunden halbieren.** Nicht einstellen, nicht verdoppeln. Halbieren, und die freigewordenen Stunden gehen in die Schicht mit der besten Leitkennzahl. Ein zweimal verfehltes Gate ist ein Signal über den Markt, nicht über deine Anstrengung — und der übliche Fehler ist, an dieser Stelle mehr zu investieren statt weniger.

### Die Skalier-Regel (die Kehrseite)

Wenn ein Strom **das Dreifache seines Ziels** liefert, gehen alle freien Stunden dorthin — sofort, ohne die Wochengrenze von 20 %. Diese Regel gewinnt mehr Geld als alle Kill-Regeln zusammen, und sie wird seltener befolgt, weil Erfolg sich nicht nach Handlungsbedarf anfühlt. Das ist dieselbe Logik wie das Viral-Protokoll aus `TikTok-Start-0-auf-1000-Playbook.md` (Review-Punkt 4): Wenn etwas läuft, fällt der Plan, und du schiebst nach.

### Die Abbruchbedingung des Gesamtsystems

Genau eine, und sie ist bewusst hart und bewusst niedrig:

> **Runway unter 3 Monate.** Dann: Stunden zurück in bezahlte Arbeit, System auf Sparflamme (nur Schicht C, 2 h/Woche), Puffer wieder aufbauen.

Kein anderes Ereignis beendet das System. Nicht ein schlechter Monat, nicht ein gesperrter Account, nicht ein gescheitertes Produkt — dafür sind die einzelnen Gates da. Und ausdrücklich nicht: „Monat 6 und noch keine 10k." Das ist laut deiner eigenen Recherche der Median, nicht das Scheitern.

---

## Teil 5: Frühwarnsignale

Dinge, die im Umsatz erst drei Monate später sichtbar werden:

| Signal | Was es bedeutet | Handlung |
|---|---|---|
| Schicht-C-Stunden steigen zwei Wochen in Folge über den Deckel | Flucht in die angenehme Arbeit | Deckel durchsetzen, nicht diskutieren |
| Anfragen konstant, Auftragsquote fällt | Angebot oder Preis passen nicht mehr | Angebotsseite überarbeiten, nicht mehr Anfragen jagen |
| Retainer-Anteil fällt | Rückfall ins Projektgeschäft | Nächsten drei Kunden ausschließlich Retainer anbieten |
| Zeit pro Asset steigt statt zu fallen | Fabrik verwahrlost | Fabrik-Tag einschieben |
| Tool-Kosten steigen ohne Umsatzanstieg | leises Margensterben | Tool-Audit vorziehen |
| Vier Wochen ohne veröffentlichtes Asset in irgendeiner Schicht | das eigentliche Abbruchrisiko | Umfang halbieren, irgendetwas Kleines fertigstellen |
| Ein Strom über 60 % des Umsatzes | Klumpenrisiko | Nächstes Quartal in den zweitstärksten Strom |
| Sprint-Sterbequote an Tag 2 unter 40 % | zu nachsichtig mit eigenen Ideen | Scout-Prompt schärfen, Gegenthese ernster nehmen |

---

## Teil 6: Die Tabellenvorlage

`Cockpit-Vorlage.csv` liegt daneben und lässt sich direkt in ein Tabellenprogramm laden. Drei Blöcke:

**Block 1 — Wochenerfassung:** je eine Zeile pro Woche mit Stunden je Schicht, Umsatz je Schicht, Kosten, den zwölf Kennzahlen.

**Block 2 — Berechnet:** €/Stunde je Schicht (rollierend 90 Tage), Deckungsbeitrag, Runway.

**Block 3 — Gate-Log:** je eine Zeile pro Gate-Prüfung mit Datum, Gate, Ergebnis (erfüllt / erster Durchgang verfehlt / zweiter Durchgang verfehlt), beschlossene Handlung. **Dieser Block ist der wertvollste des ganzen Cockpits** — er ist nach zwölf Monaten die einzige ehrliche Antwort auf die Frage, ob du dein eigenes System befolgt hast oder nur zugeschaut.

---

## Der Kern in fünf Sätzen

Es gibt eine Leitkennzahl — € pro Stunde je Schicht über 90 Tage —, und sie beantwortet die einzige wöchentliche Entscheidung: wohin die Stunden gehen. Zwölf Kennzahlen reichen; alles darüber ist Beschäftigung. Gates sind Zustände, nicht Termine, und ein zweimal verfehltes Gate halbiert Stunden statt sie zu verdoppeln. Die Skalier-Regel — dreifaches Ziel zieht alle freien Stunden — verdient mehr Geld als jede Kill-Regel und wird seltener befolgt. Und die einzige Bedingung, die das ganze System beendet, ist ein Runway unter drei Monaten; alles andere ist ein Gate, kein Ende.
