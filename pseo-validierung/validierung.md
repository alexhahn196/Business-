# Marktvalidierung: pSEO-Portal für geförderte Weiterbildung (DE)

**Erhebungsdatum:** 28.07.2026
**Geprüfte Hypothese:** Ein programmatisches SEO-Portal (Achsen Beruf × Ort ×
Förderinstrument) erreicht in 12 Monaten 5.000–15.000 organische Sessions/Monat
und monetarisiert diese über Lead-Vermittlung an AZAV-Träger zu 30–80 €/Lead.

**Rohdaten und Skripte:** `pseo-validierung/scripts/`, `pseo-validierung/data/`,
`pseo-validierung/ergebnisse/`. Jede Zahl unten ist entweder nachrechenbar oder
als Annahme gekennzeichnet.

**Evidenz-Label:** `[BELEGT]` eigene Messung oder Primärquelle mit URL ·
`[GESCHÄTZT]` Modellrechnung mit offengelegten Annahmen ·
`[INDIZ]` Marketing-Claim oder schwache Quelle ·
`[UNBEKANNT]` konnte nicht geprüft werden

---

## 1. Verdikt

**Nicht bauen.**

Die Beruf×Ort-Achse trägt keine Information: Bei 29 exakt gemessenen
Städtepaaren überschneiden sich zwei Stadtseiten im Text zu **62,8 %** — und
zwar bei **weit entfernten Städten stärker als bei Nachbarstädten (55,7 %)**.
Der Grund ist strukturell und nicht behebbar: 32,5 % aller Angebote haben mehr
als 50 Termine bundesweit, dieselben Kurse derselben Träger erscheinen also in
jeder Stadt. Hinzu kommt, dass die Datenquelle nur über einen nicht
dokumentierten, mit fremdem Client-Key angesprochenen Endpunkt erreichbar ist,
dessen Betreiber die massenhafte Auswertung ausdrücklich ablehnt — das reißt
Abbruchkriterium 5 unabhängig von allem anderen.

**Die Zahl, die den Ausschlag gibt:** Text-Überschneidung zweier Stadtseiten
**0,628 bei Fernstädten vs. 0,557 bei Nachbarstädten**. Wenn Entfernung die
Ähnlichkeit *nicht* senkt, existiert die geografische Differenzierung nicht,
auf der das ganze Modell beruht.

---

## 2. Ergebnisse je Arbeitspaket

### AP1 — Datenquelle: machbar und legal?

#### Der dokumentierte Endpunkt ist tot

| Endpunkt | HTTP | Bemerkung |
|---|---|---|
| `rest.arbeitsagentur.de/infosysbub/wbsuche/pc/v2/bildungsangebot` | **404** | der in bundesAPI dokumentierte |
| `rest.arbeitsagentur.de/infosysbub/wbsuche/pc/v1/bildungsangebot` | **404** | |
| `rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs` | 200 | **Kontrolle**: gleicher Host, anderer Dienst |
| `rest.mein-now.de/now-prod/suche/pc/v1/bildungsangebot` | 200 | produktiv, mit Key |
| dito, **ohne** `X-API-Key` | **403** | |

`[BELEGT]` — eigene Messung, `data/ap1_endpoint_probe.json`. Die 404 kommt vom
BA-Server selbst (eigene `x-correlationid` im Response-Header), nicht vom Proxy;
die Jobsuche-API auf demselben Host antwortet mit 200.

Der produktive Endpunkt wurde aus dem Frontend-Bundle von
`https://mein-now.de/weiterbildungssuche/` rekonstruiert
(`window.sucheConfig.backendHost`). Der nötige Schlüssel
`X-API-Key: infosysbub-nowsuche` ist die **Client-ID der Weiterbildungssuche
selbst** (`window.oiamConfig.clientId`) — es gibt keinen eigenen Zugang, man
verwendet den Schlüssel der Website weiter. `[BELEGT]`

`web.arbeitsagentur.de/weiterbildungssuche` leitet per 301 auf
`mein-now.de/weiterbildungssuche/` um. KURSNET wurde im Januar 2024 durch
mein NOW abgelöst; `kursnet-finden.arbeitsagentur.de` löst nicht mehr auf.
`[BELEGT]`

#### Stichprobe

1 Request/Sekunde, identifizierbarer User-Agent, kein Vollabzug.
**2.015 Datensätze** (Obergrenze 2.000, Überschreitung um 15 durch
seitenweises Schreiben) plus 384 Aggregat-Requests ohne Datensatzabzug.
`[BELEGT]` — `data/reichweite.jsonl`, `data/ueberlappung.jsonl`,
`data/grid_facetten.jsonl`, `data/rohdaten_felder.jsonl`

#### Feldstruktur und Vollständigkeit (n = 200 Angebote, 738 Termine)

| Feld | % befüllt | | Terminfeld | % befüllt |
|---|---:|---|---|---:|
| `id`, `titel`, `inhalt` | 100,0 | | `id`, `dauer`, `kostenWert` | 100,0 |
| `bildungsanbieter.name` | 100,0 | | `unterrichtszeit`, `quelle` | 100,0 |
| `bildungsanbieter.adresse.ort/plz` | 100,0 | | `unterrichtsform` | 99,6 |
| `anzahlTermine` | 100,0 | | `adresse` | 91,2 |
| `weiterbildungsart` | 97,0 | | **`beginn` / `ende`** | **59,9** |
| `bildungsanbieter.logo` | 96,0 | | | |

`[BELEGT]` — `ergebnisse/ap1_feldanalyse.json`

Die Kernfelder sind praktisch vollständig. **40 % der Termine haben kein
Beginndatum** — für Seiten, die „nächster Starttermin" ausspielen wollen, ist
das eine relevante Lücke.

Beschreibungstext (`inhalt`) Median **1.254 Zeichen**, ausreichend lang für
Seiteninhalt — aber es ist fremder Text (siehe Rechtsteil).

**Nicht in der Listenantwort enthalten:** Förderart, Abschluss, Zertifizierer,
exakter Preis. Diese kommen nur über die Detail-Ressource
`/pc/v1/bildungsangebot/{id}` oder die Facetten-Aggregation. Für ein Portal
bedeutet das einen zusätzlichen Request pro Angebot. `[BELEGT]`

#### Aktualität

Termine von **2024-07-15 bis 2027-10-24**, nur **4,5 %** der Startdaten liegen
in der Vergangenheit. Die Daten sind aktuell gepflegt. `[BELEGT]`

#### Träger und geografische Verteilung

- **252 distinkte Träger** in der Gesamtstichprobe `[BELEGT]`
- In der 200er-Feldstichprobe: 105 Träger, Top-10 halten **32,0 %** der Angebote
- **42,4 %** der Angebote haben einen Trägersitz, der nicht mit dem Kursort
  übereinstimmt `[BELEGT]`

Der letzte Wert ist der erste Hinweis auf das AP2-Problem: die Anbieter sind
überregional, nicht lokal.

#### Nutzungsbedingungen, robots.txt, Rechtsrisiko

| Quelle | Befund |
|---|---|
| `mein-now.de/robots.txt` | `User-agent: * / Allow: /` `[BELEGT]` |
| `www.arbeitsagentur.de/robots.txt` | `Disallow:` + `Allow: /` `[BELEGT]` |
| `rest.mein-now.de`, `rest.arbeitsagentur.de` | liefern **403** statt robots.txt `[BELEGT]` |

robots.txt verbietet also nichts. Das ist aber nicht der relevante Hebel:

1. **Urheberrecht am Inhalt.** BA-Impressum: *„Die Vervielfältigung von Texten,
   Textteilen und Bildmaterial bedarf der ausdrücklichen vorherigen Zustimmung
   der BA."* Die englischen Terms of Use nennen die BA als Inhaberin des
   Copyrights am Portal und seinen Inhalten. Das Feld `inhalt` — der
   1.254-Zeichen-Beschreibungstext, der den Seiteninhalt tragen soll — ist
   genau solcher Text. `[BELEGT]`
   ([Impressum](https://www.arbeitsagentur.de/impressum),
   [Terms of Use](https://www.arbeitsagentur.de/en/terms-of-use))

2. **Datenbankherstellerrecht, § 87b Abs. 1 S. 2 UrhG.** Wortlaut: *„Der
   Vervielfältigung … eines nach Art oder Umfang wesentlichen Teils der
   Datenbank steht die wiederholte und systematische Vervielfältigung … von
   nach Art und Umfang unwesentlichen Teilen der Datenbank gleich, sofern diese
   Handlungen einer normalen Auswertung der Datenbank zuwiderlaufen oder die
   berechtigten Interessen des Datenbankherstellers unzumutbar
   beeinträchtigen."* `[BELEGT]`
   ([gesetze-im-internet.de](https://www.gesetze-im-internet.de/urhg/__87b.html))

   Der konkrete Risikopunkt: Für Einzelabfragen hat der BGH (Autobahnmaut,
   I ZR 47/08) entschieden, dass weder die Datenbank als Ganzes noch wesentliche
   Teile betroffen sind. Ein pSEO-Portal macht aber genau das, was S. 2
   adressiert — **wiederholte, systematische Entnahme**, um einen dauerhaften
   Spiegel des Bestands zu betreiben. Das ist die kritische Grenze, und sie
   wird vom Geschäftsmodell konstruktiv überschritten, nicht zufällig gestreift.
   *(Keine Rechtsberatung — das ist der Punkt, an dem anwaltliche Prüfung
   ansetzen müsste.)*

3. **Erklärte Haltung des Betreibers.** Die BA hat 2021 zur offenen
   Dokumentation ihrer Schnittstellen erklärt, diese seien für eine komfortable
   Suche gedacht, *„nicht aber für einen massenhaften Zugriff bzw. eine
   massenhafte Auswertung mit technischen Mitteln"*, und hat als Reaktion
   CAPTCHAs eingebaut. **Rechtsschritte gab es nicht** — das ist ein
   Gegenbefund und gehört dazu. `[BELEGT]`
   ([netzpolitik.org](https://netzpolitik.org/2021/open-data-arbeitsagentur-kaempft-gegen-offene-schnittstelle/))

4. **Kein offizieller Bezugsweg.** Das bundesAPI-README stellt selbst fest, die
   BA biete *„bis heute keine offizielle API"* an; das Repository enthält keine
   LICENSE-Datei. Der offizielle Datenfluss läuft **eingehend**: Träger laden
   ihre Kataloge im Format open-Qcat per XML-Upload zu KURSNET/mein NOW hoch.
   Ein ausgehender Bulk- oder Lizenzweg für Dritte ist nicht auffindbar.
   `[BELEGT]` / für das Nichtvorhandensein eines Lizenzwegs: `[UNBEKANNT]` —
   Abwesenheit eines Fundes ist kein Beweis der Abwesenheit.

#### Alternativen

| Quelle | Enthält Kurse mit Träger + Ort? | Bewertung |
|---|---|---|
| `foerderdatenbank.de` | **nein**, nur Förderprogramme | als Kursquelle unbrauchbar `[BELEGT]` |
| GovData | kein BA-Kursdatensatz; nur Statistik und Standortgeodaten | unbrauchbar `[BELEGT]` |
| Landesportale (z. B. `weiterbildung-mv.de`) | ja, aber je Land eigene Struktur | kein bundesweiter Ersatz, Aufwand pro Land `[BELEGT]` als Existenz |
| open-Qcat direkt von Trägern | ja | **einziger sauberer Weg** — erfordert Verträge mit jedem Träger `[BELEGT]` als Format |

Der letzte Punkt ist die einzige rechtlich unproblematische Variante — und sie
kehrt das Geschäftsmodell um: Man braucht die Träger *vor* dem Traffic, nicht
danach.

---

### AP2 — Differenzierungsanalyse *(wichtigstes Paket)*

Grundlage: 16 Berufe × 24 Städte = **384 Kombinationen**, Umkreis 5 km,
Aggregat-Abfrage ohne Datensatzabzug. `data/grid_facetten.jsonl`

#### Verteilung der Angebotszahl je Seite

| | Anteil |
|---|---:|
| 0 Angebote | 18,5 % |
| 1–2 Angebote | 5,2 % |
| 3+ Angebote | 76,3 % |
| **< 2 Angebote (Abbruchkriterium)** | **23,7 %** |

Median: 23 Angebote je Kombination. `[BELEGT]`

| Stadtklasse | n | Median Angebote | < 2 Angebote |
|---|---:|---:|---:|
| GROSS (≥100k) | 192 | 74,5 | 12,0 % |
| MITTEL (20–100k) | 128 | 18,5 | 24,2 % |
| KLEIN (5–20k) | 64 | 3,5 | **45,3 %** |

**Abbruchkriterium 1 ist NICHT gerissen** (23,7 % statt >50 %). Die Menge ist
nicht das Problem.

#### Das Problem ist die Gleichheit, nicht die Knappheit

**Bundesweite Reichweite der Angebote** (n = 624 Angebote über 16 Berufe):

| Termine bundesweit je Angebot | Anteil |
|---|---:|
| genau 1 | 25,3 % |
| > 10 | 44,1 % |
| **> 50** | **32,5 %** |
| Median | 6 |
| Maximum | 2.594 |

`[BELEGT]` — Ein Drittel aller Angebote wird an mehr als 50 Orten angeboten.
Beispiel aus den Rohdaten (`data/reichweite.jsonl`): Angebot `10379341727` der
DAA hat **345 Termine**; allein die fünf in der Antwort mitgelieferten Termine
liegen in Bad Kreuznach, Berlin, Brühl, Frankfurt am Main und Lübeck — quer
durch die Republik. Genau diese Angebote füllen jede Stadtseite.

**Exakt gemessene Überschneidung zwischen Städten**
(vollständig paginierte Angebots-ID-Listen, keine Stichprobenschätzung):

| | Nachbarstädte (n=3) | Fernstädte (n=29) |
|---|---:|---:|
| Jaccard der Angebots-IDs | 0,384 | **0,426** |
| Containment (kleinere in größere) | 0,961 | 0,777 |
| **Token-Überschneidung des Textes** | **0,557** | **0,628** |
| Träger-Jaccard | 0,478 | 0,454 |

`[BELEGT]` — `ergebnisse/ap2_ergebnisse.json`, Feld `3_ueberlappung`

**Das ist der zentrale Befund.** Weit entfernte Städte ähneln sich *stärker*
als Nachbarstädte. Die Ortsachse trägt keine Information. Einzelbeispiele:

| Paar | Beruf | Angebote A/B | identisch | Jaccard | Token |
|---|---|---|---:|---:|---:|
| Dortmund / Leipzig | Steuerfachangestellte | 12 / 13 | 12 | 0,923 | 0,911 |
| Hamburg / Nürnberg | Steuerfachangestellte | 9 / 8 | 8 | 0,889 | 0,933 |
| Bochum / Stralsund | Lagerlogistik | 197 / 161 | 139 | 0,635 | 0,693 |
| Bochum / Dortmund | Immobilienkaufmann | 3 / 5 | 3 | 0,600 | **1,000** |
| Nürnberg / Stralsund | Immobilienkaufmann | 6 / 5 | 4 | 0,571 | **1,000** |

Dortmund und Leipzig liegen 400 km auseinander und hätten bei
„Umschulung Steuerfachangestellte" **12 von 13 identischen Angeboten**.

#### Anteil identischen Seiteninhalts bei Standard-Template

Formel: `identisch = B + (1 − B) × Token-Überschneidung`
`B` = Anteil der Seite, der bei einem Standard-Template zwischen zwei
Stadtseiten konstruktionsbedingt gleich ist (Intro, Förder-Erklärung, FAQ,
Navigation, CTA). **`B` ist eine Annahme, keine Messung.** Gemessen ist nur
die Token-Überschneidung.

| Boilerplate-Anteil B | Nachbarstädte | Fernstädte |
|---|---:|---:|
| 40 % | 73,4 % | 77,7 % |
| 60 % | 82,3 % | 85,1 % |

`[GESCHÄTZT]` auf gemessener Basis. Zwei beliebige Stadtseiten wären zu
**73–85 %** identisch. Das ist das Profil, das zu „Crawled – currently not
indexed" führt.

#### Maximal sinnvolle Seitenzahl

Theoretisch möglich (2.056 Gemeinden ab 5.000 EW × 250 Berufe): **514.000**.

Nach dem reinen Mengenkriterium (≥3 Angebote), einwohnergewichtet:
**304.809** `[GESCHÄTZT]`, Annahmen im Skript offengelegt.

**Diese Zahl ist irreführend und sollte nicht verwendet werden.** Sie
berücksichtigt nur, ob genug Angebote da sind, nicht ob sie sich unterscheiden.
Legt man Differenzierung als Kriterium an, bleibt vom Ortsraster im Wesentlichen
die Ebene, auf der Google überhaupt Nachfrage sieht (siehe AP4): rund **7–12
Großstädte**. Bei 250 Berufen wären das **1.750–3.000 Seiten** — zwei
Größenordnungen unter der Planung und keine pSEO-Grundlage mehr, sondern ein
normales redaktionelles Portal.

---

### AP3 — SERP-Wettbewerb

> **Evidenzstufe beachten:** Für belastbare SERP-Daten wäre ein SERP-API-Zugang
> nötig (DataForSEO, Sistrix, Ahrefs). In dieser Umgebung nicht vorhanden.
> Erhoben wurde über das WebSearch-Werkzeug — **das ist nicht Google**, liefert
> 7–10 statt 10 Treffer und nicht Googles Ranking. Alles hier: `[INDIZ]`.
> Rohdaten: `data/ap3_serp_beobachtung.json`

6 Keywords über Groß-, Mittel- und Kleinstädte, 49 klassifizierte Treffer:

| Seitentyp | Anteil |
|---|---:|
| **Bildungsträger** | **77,6 %** |
| Aggregator | 14,3 % |
| Behörde/Kammer | 4,1 % |
| Redaktion | 4,1 % |

**Kernbefund:** Die Träger betreiben die Beruf×Ort-Seiten **selbst**, mit
erkennbar programmatischen URL-Mustern:

- `wbstraining.de/kurse/lokal/umschulung/<stadt>/<beruf>/`
- `bfw.de/angebot/umschulung/<stadt>/<beruf>/`
- `ibb.com/weiterbildung/<kurs>/ibb-<stadt>`
- `swa.de/standorte/umschulungen-<beruf>-<stadt>/`
- `comcave.de/standorte/<stadt>`

Die geplante Achse ist also bereits von genau den Anbietern besetzt, an die
vermittelt werden soll. Sie haben eigene Kursdaten (kein Rechtsproblem),
eigene Marge und keinen Grund, einen Vermittler dazwischenzulassen.

**Abbruchkriterium 2 ist gerissen** (14,3 % < 20 %) — mit der ausdrücklichen
Einschränkung der schwachen Evidenzbasis.

#### Etablierte Aggregatoren

| Portal | Indexgröße | Ortsachse? |
|---|---:|---|
| kursfinder.de | ~19.816 URLs (Sitemap) | **nur ~24 stadtbezogene Seiten** |
| springest.de | themenbasierte Sitemaps | Themen, nicht Orte |
| weiterbildung.de | **identische robots.txt wie springest.de**, inkl. `/mein-springest` → dieselbe Plattform | — |
| genaumeinkurs.de | robots.txt ohne Sitemap-Verweis | nicht ermittelbar `[UNBEKANNT]` |

`[BELEGT]` (Sitemaps/robots.txt eigener Abruf)

Bemerkenswert: **kursfinder.de hat nach Jahren am Markt gerade 24 Stadtseiten**
bei knapp 20.000 URLs. Der etablierte Aggregator baut die Beruf×Ort-Matrix
nicht. Das ist entweder eine bewusste Entscheidung oder ein bereits gemachter
Fehlschlag — in beiden Fällen ein Warnsignal.

#### Behörde in den SERPs — Gegenbefund

`arbeitsagentur.de` und `mein-now.de` tauchten in **keiner** der sechs Abfragen
auf. `mein-now.de` hat insgesamt nur **220 URLs**, und die Weiterbildungssuche
selbst ist eine Single-URL-Angular-SPA ohne indexierbare Kursseiten. `[BELEGT]`

**Der befürchtete strukturelle Nachteil durch die Behörde besteht nicht.** Das
ist der einzige klar positive Befund der gesamten Untersuchung und wird hier
nicht weggeglättet — er reicht nur nicht, um die anderen aufzuwiegen.

---

### AP4 — Nachfrage

**Suchvolumina: `[UNBEKANNT]`.** In der Umgebung sind keine Zugangsdaten für
DataForSEO, Ahrefs, Sistrix oder Google Ads Keyword Planner vorhanden (geprüft).
Es gibt daher **keine belastbare Aussage** zum adressierbaren Suchvolumen und
keine CPC-Daten.

Ersatzweise Google Autocomplete als **schwächerer Proxy** — er zeigt nicht
Volumen, sondern nur, welche Fortsetzungen Google häufig genug sieht.
`data/ap4_autocomplete.json`

**Welche Städte schlägt Google überhaupt vor?** Über 16 Berufe hinweg genau
sieben: Berlin, Hamburg, Köln, Leipzig, Nürnberg, Dortmund, Essen —
**ausnahmslos Großstädte**. `[INDIZ]`

**Longtail-Test** („umschulung `<beruf>` `<stadt>`", Anteil Städte mit
mindestens einem Vorschlag):

| Stadtklasse | Fachinformatiker | Pflegefachkraft |
|---|---:|---:|
| GROSS | 91,7 % (11/12) | 66,7 % (8/12) |
| MITTEL | 37,5 % (3/8) | 0,0 % (0/8) |
| KLEIN | **0,0 % (0/4)** | **0,0 % (0/4)** |

`[INDIZ]` — Unterhalb der Großstadtebene bricht die erkennbare Nachfrage weg.
Das deckt sich mit AP2: dort, wo es viele Angebote gäbe (Großstädte), sind die
Seiten am ähnlichsten; dort, wo Seiten einzigartig wären (Kleinstädte), sucht
niemand.

**Traffic-Hochrechnung:** bewusst **nicht** durchgeführt. Ohne Suchvolumen wäre
jede Sessions-Zahl eine Zahl ohne Basis. Die Formel wäre
`Sessions = Σ(Suchvolumen_kw × CTR(Position))`, mit branchenüblichen CTRs von
ca. 11 % (Pos. 3) bis 2 % (Pos. 8) — aber ohne den ersten Faktor ist das
Rechnen sinnlos. **Abbruchkriterium 3 ist nicht entscheidbar.**

---

### AP5 — Monetarisierung

#### Zahlt jemand für Leads?

**Ja — die Nachfrageseite existiert.** `[BELEGT]` für die Existenz:

- **genaumeinkurs.de** betreibt eine Seite „Für Bildungsträger – Qualifizierte
  Teilnehmer gewinnen" mit Pay-per-Lead-Modell ohne Grundgebühr. Ein direkter
  Abruf der Seite scheiterte (HTTP 403), die Beschreibung stammt aus dem
  Suchergebnis-Snippet → `[INDIZ]` für die Konditionen, `[BELEGT]` für die
  Existenz des Angebots.
- Es existieren spezialisierte Leadgenerierungs-Agenturen für Bildungsträger.

**Abbruchkriterium 4 ist NICHT gerissen.** Aber:

#### Widersprüchliche Preisangaben — nicht geglättet

| Quelle | Angabe | Label |
|---|---|---|
| vollekurse.com (Agentur-Blog) | CPL **30–100 €** im Bildungssektor | `[INDIZ]` — Marketing-Claim einer Agentur, die genau diese Leistung verkauft |
| **SGD-Partnerprogramm** (Primärquelle) | **5 € pro Lead**, 100 € pro Sale | `[BELEGT]` ([sgd.de](https://www.sgd.de/partnerprogramm.html)) |

Die einzige **öffentlich nachprüfbare** Konditionsangabe der Vertikale liegt bei
**5 € pro Lead** — Faktor 6 bis 16 unter der Hypothese von 30–80 €. Einschränkung:
Die SGD ist Fernstudienanbieter, nicht AZAV-Bildungsgutschein-Träger; die
Segmente sind nicht deckungsgleich. Die 30–80 €-Annahme der Hypothese ist damit
**nicht widerlegt, aber auch durch nichts belegt** außer einem Agentur-Claim,
der den Hypothesenkorridor auffällig genau trifft.

**Google-Ads-Belegung der Ziel-Keywords: `[UNBEKANNT]`.** Das
Anzeigen-Transparenz-Center ließ sich nicht automatisiert abfragen, und das
verwendete Suchwerkzeug trennt Anzeigen nicht von organischen Treffern. Der
beste verfügbare Indikator für Zahlungsbereitschaft — wer schaltet Anzeigen —
konnte damit **nicht** erhoben werden. Das ist eine echte Lücke, weil es die
Kernfrage des Pakets ist.

#### Trägerliste für telefonische Validierung

**252 distinkte Träger** erfasst, Top-30 in `ergebnisse/ap5_traegerliste.md`
mit Name, Sitz, Angebotszahl, bundesweiter Terminzahl und Fachgebieten.
`[BELEGT]` — alles gemessen.

Auszug:

| Träger | Sitz | Angebote (Stichprobe) | Termine bundesweit |
|---|---|---:|---:|
| DAA – Deutsche Angestellten-Akademie gGmbH | Hamburg | 675 | 3.026 |
| Smart Future Campus GmbH | München | 133 | 1.250 |
| Berger Bildungsinstitut GmbH | Kassel | 68 | 1.062 |
| IBB Institut für Berufliche Bildung AG | Buxtehude | 67 | 2.967 |
| alfatraining Bildungszentrum GmbH | Karlsruhe | 64 | 1.476 |
| WBS TRAINING SE | Berlin | 55 | 7.164 |
| GrandEdu GmbH | Herford | 48 | 6.494 |
| Fortbildungsakademie der Wirtschaft (FAW) gGmbH | Köln | 41 | 879 |

**Telefonnummern und Ansprechpartner sind nicht enthalten.** Die Listenantwort
der Schnittstelle liefert diese Felder nicht, und ich habe sie nicht erfunden
oder aus unsicheren Quellen ergänzt. Sie müssten je Träger einzeln recherchiert
werden.

#### Fünf Fragen für das Validierungstelefonat

Bewusst ohne Suggestion, ohne das Produkt zu erwähnen, und so gestellt, dass
Vergangenheitsverhalten statt Absichtserklärungen abgefragt wird:

1. „Wie sind die Teilnehmer, die dieses Jahr bei Ihnen angefangen haben,
   tatsächlich zu Ihnen gekommen — können Sie das grob nach Kanälen aufteilen?"
2. „Was haben Sie im letzten Jahr an externe Anbieter für Teilnehmergewinnung
   gezahlt, und an wen?"
3. „Wenn Ihnen jemand eine Kontaktanfrage weiterleitet: Was muss dabei stehen,
   damit Sie das überhaupt bearbeiten — und was passiert danach bei Ihnen damit?"
4. „Wie viele solcher Anfragen führen bei Ihnen erfahrungsgemäß zu einem
   Kursstart, und wie lange dauert das?"
5. „Welche Kurse bei Ihnen sind aktuell nicht ausgelastet, und woran liegt das
   Ihrer Einschätzung nach?"

Frage 5 ist die wichtigste: Wenn die Kurse voll sind, gibt es keinen Bedarf an
Leads — unabhängig von jedem Preis.

---

### AP6 — Recht und Reputation

#### DSGVO bei Lead-Weitergabe

Die Weitergabe von Interessentendaten an Bildungsträger braucht eine
Einwilligung, die **die Empfänger namentlich benennt**; eine pauschale
Einwilligung („an unsere Partner") genügt nicht. Zweck und Datenumfang müssen
bestimmt sein. `[BELEGT]` als herrschende Auffassung in der Fachliteratur,
`[UNBEKANNT]` als gerichtlich geklärter Einzelfall für diese Vertikale.

**Praktische Konsequenz für das Modell:** Man kann einen Lead nicht an
„denjenigen, der am meisten zahlt" routen, wenn dieser bei Einwilligung noch
nicht feststand. Entweder man nennt alle potenziellen Empfänger vorab — was das
Formular unbrauchbar macht — oder man beschränkt sich pro Formular auf wenige,
fest benannte Träger. Das begrenzt die Skalierbarkeit der Monetarisierung
strukturell.

#### UWG

- **Bezahlte Platzierung muss klar gekennzeichnet sein** (§ 3 Abs. 3 UWG
  i. V. m. Nr. 11a Anhang). Das OLG Karlsruhe hat entschieden, dass ein kleiner
  Hinweis „Anzeige" nicht genügt, wenn das Gesamtbild den Werbecharakter
  überdeckt. Nutzer dürfen keine neutrale, nach objektiven Kriterien sortierte
  Liste vermuten, wo eine kommerzielle Vereinbarung dahintersteht. `[BELEGT]`
- **„Geprüfte Anbieter"** wäre irreführend, solange nichts Eigenes geprüft
  wurde. Die AZAV-Zulassung ist eine Zulassung Dritter, keine eigene Prüfung —
  und sie sagt, wie unten belegt, wenig über Qualität.
- **„Kostenlos"** ist bei Bildungsgutschein-Maßnahmen heikel: kostenlos für die
  Teilnehmenden, finanziert aus Steuermitteln. Die Formulierung ist verbreitet,
  aber angreifbar.

`[BELEGT]` für die Rechtslage, `[UNBEKANNT]` für konkrete Abmahnpraxis in dieser
Nische.

#### Markenrecht

**Weitgehend `[UNBEKANNT]`.** DPMAregister ist eine formularbasierte
Java-Anwendung ohne saubere automatisierte Abfrage. Über die TMview-API
(EUIPO/TMDN, Territorium DE) gelang **genau eine** Abfrage, danach schloss der
Dienst die Verbindungen:

- „Fördercampus" → **0 Treffer** `[BELEGT]`
- Kursgutschein, Weiterbildungsradar, Bildungsnavigator, Umschulungsfinder,
  Förderkurs, Kursnavi, Bildungsgutschein24, Umschulungsradar,
  Weiterbildungskompass → **nicht geprüft** `[UNBEKANNT]`
  (`ergebnisse/ap6_marken.json`, `scripts/07_ap6_marken.py`)

Auch die eine Abfrage ist nur eine Wortidentitätsprüfung — Ähnlichkeit,
Nizza-Klassenkollision und Verkehrsgeltung wurden nicht geprüft.

#### Reputationsrisiko der AZAV-Branche

Hier gibt es dokumentierte, gravierende Probleme. `[BELEGT]` —
[t-online, 27.04.2026](https://www.t-online.de/nachrichten/deutschland/id_101115794/weiterbildung-von-arbeitslosen-ist-systematischer-betrug-.html)

- Daniel Graf (Qualitätsmanagement-Berater für Bildungsträger): *„Zwanzig
  Prozent der Träger arbeiten illegal. Sie greifen Fördermittel im großen Stil
  ab und machen sich dann aus dem Staub."*
- Carina Knie-Nürnberg, Geschäftsführerin der BA-Regionaldirektion
  Berlin-Brandenburg, bestätigt Fälle **„systematischen Betrugs"**, „organisiert"
  und nicht auf Berlin beschränkt.
- Fördervolumen 2026: 4,1 Mrd. €; ~170.000 Teilnehmende 2024; laut Prüfung 2022
  blieben **74 %** vorab eingekaufter Kursplätze ungenutzt (~350 Mio. €);
  September 2025 Festnahmen in Berlin wegen mutmaßlichen Abrechnungsbetrugs von
  ca. 891.000 €.
- Die FAZ hat gesondert über fragwürdige geförderte KI-Weiterbildungen berichtet.
  `[INDIZ]` (Podcast-Ankündigung, Artikel nicht im Volltext geprüft)

**Für ein Vermittlungsportal ist das ein doppeltes Problem:** Man vermittelt in
eine Branche, in der ein zweistelliger Prozentsatz der Anbieter unter
Betrugsverdacht steht — und man vermittelt ausgerechnet die Zielgruppe
(Arbeitslose), die dadurch geschädigt wird. Wer für Leads am meisten zahlt, ist
plausibel nicht der seriöseste Träger. Ein „geprüfte Anbieter"-Versprechen wäre
unter diesen Umständen sowohl UWG-riskant als auch faktisch schwer haltbar.

---

## 3. Abbruchkriterien mit Ist-Werten

| # | Kriterium | Ist-Wert | Gerissen? |
|---|---|---|---|
| 1 | >50 % der Seiten mit <2 Angeboten (AP2) | **23,7 %** (KLEIN: 45,3 %) | **nein** |
| 2 | Aggregatoren <20 % der Top-10, Träger dominieren (AP3) | **14,3 %** Aggregator, **77,6 %** Träger | **ja** `[INDIZ]` |
| 3 | Adressierbares Suchvolumen <50.000/Monat (AP4) | kein Keyword-Tool verfügbar | **nicht entscheidbar** `[UNBEKANNT]` |
| 4 | Keine identifizierbare zahlende Nachfrageseite (AP5) | existiert (Pay-per-Lead-Anbieter aktiv) | **nein** |
| 5 | Datenzugang nur über rechtlich riskantes Scraping (AP1) | keine offizielle API, fremder Client-Key nötig, Betreiber lehnt Massenauswertung ausdrücklich ab, Vervielfältigung laut Impressum zustimmungspflichtig | **ja** `[BELEGT]` |

**Zwei von fünf Kriterien gerissen, eines nicht entscheidbar.** Nach der Regel
des Auftrags („nicht bauen, wenn eines zutrifft") lautet die Empfehlung:
**nicht bauen.**

Hinzu kommt ein Befund, der in keinem Kriterium steht, aber schwerer wiegt als
alle fünf: Die Ortsachse differenziert nicht (Fernstädte ähnlicher als
Nachbarstädte). Kriterium 1 misst die falsche Größe — es fragt nach der Menge
der Angebote, während das Problem ihre Gleichheit ist.

---

## 4. Was ich nicht prüfen konnte — und warum

| Punkt | Grund |
|---|---|
| **Echte Suchvolumina und CPCs** | Keine Zugangsdaten für DataForSEO/Ahrefs/Sistrix/Google Ads in der Umgebung. Ohne sie ist AP4 nicht beantwortbar und Kriterium 3 nicht entscheidbar. Ersatzproxy Autocomplete ist deutlich schwächer. |
| **Echte Google-SERPs** | Kein SERP-API-Zugang. Das verwendete Suchwerkzeug ist nicht Google, liefert 7–10 Treffer statt Top-10 und trennt Anzeigen nicht von organischen Ergebnissen. Alle AP3-Zahlen daher `[INDIZ]`. |
| **Google-Ads-Belegung der Ziel-Keywords** | Anzeigen-Transparenz-Center nicht automatisiert abfragbar. Damit fehlt der beste Einzelindikator für Zahlungsbereitschaft — die Kernfrage von AP5. |
| **Markenrecherche (9 von 10 Namen)** | DPMAregister formularbasiert; TMview-API blockte nach dem ersten Request dauerhaft. |
| **Kontaktdaten der Träger** | In der Listenantwort der Schnittstelle nicht enthalten; nicht ergänzt, um nichts zu erfinden. |
| **Nachbarstadt-Vergleich auf breiter Basis** | Nur 3 vollständig paginierte Nachbarvergleiche (Dortmund/Bochum), weil das 2.000-Datensatz-Limit erreicht war. Die 29 Fernvergleiche sind die belastbarere Basis — und zeigen dasselbe, nur stärker. |
| **Indexgröße von genaumeinkurs.de** | robots.txt ohne Sitemap-Verweis; Seite lieferte bei direktem Abruf HTTP 403. |
| **Ob ein Lizenzweg für BA-Daten existiert** | Nicht auffindbar — das ist kein Beweis, dass es keinen gibt. Eine direkte Anfrage bei der BA wäre der nächste Schritt. |
| **Rechtliche Bewertung** | Keine Rechtsberatung. Die Risikopunkte sind benannt, die Bewertung gehört zu einer Anwältin oder einem Anwalt. |

---

## 5. Wenn Sie es trotzdem bauen wollen

Kein „Bauen"-Verdikt, also entfällt die geforderte Restrisikoliste formal.
Für den Fall, dass Sie anders entscheiden, die drei Punkte nach Schadenshöhe —
und die Bedingungen, unter denen die Analyse kippen würde:

1. **Rechtlicher Datenzugang** (Schadenshöhe: Totalverlust). Die wiederholte,
   systematische Entnahme ist genau der Fall des § 87b Abs. 1 S. 2 UrhG, und die
   Beschreibungstexte sind fremdes Material. Einziger sauberer Weg: open-Qcat
   direkt von den Trägern — was Verträge *vor* dem Traffic erfordert.
2. **Nicht-Indexierung** (Schadenshöhe: gesamte Aufbauzeit). Bei 73–85 %
   Seitenähnlichkeit ist „Crawled – currently not indexed" der Normalfall, nicht
   der Ausnahmefall.
3. **Reputationshaftung** (Schadenshöhe: Marke und Person). Vermittlung in eine
   Branche mit dokumentiertem systematischem Betrug, an eine besonders
   schutzbedürftige Zielgruppe, bei einem Modell, das strukturell den
   zahlungsbereitesten statt den besten Träger bevorzugt.

**Was die Analyse kippen würde:** echte Suchvolumendaten, die zeigen, dass die
Longtail-Achse unterhalb der Großstädte doch Volumen trägt — plus ein
belastbarer Lead-Preis über 30 € aus mindestens fünf Trägergesprächen. Beides
ist mit überschaubarem Aufwand nachholbar (ein Monat Sistrix-Zugang, fünf
Telefonate aus der Liste in `ergebnisse/ap5_traegerliste.md`). Ohne diese zwei
Zahlen ist jede Entscheidung für den Bau eine Wette gegen die hier gemessenen
Befunde.

---

## 6. Nachrechnen

```bash
cd pseo-validierung
python3 scripts/01_ap1_endpoint_probe.py    # Endpunkt-Erreichbarkeit
python3 scripts/02_sample.py                # Stichprobe (ca. 12 Min, 1 req/s)
python3 scripts/03_ap2_analyse.py           # AP2-Auswertung
python3 scripts/04_ap1_feldanalyse.py       # Feldvollständigkeit
python3 scripts/05_ap4_autocomplete.py      # Nachfrage-Proxy
python3 scripts/06_ap5_traegerliste.py      # Trägerliste
python3 scripts/07_ap6_marken.py            # Markenvorabprüfung (TMview drosselt)
```

`scripts/config.py` dokumentiert im Kopf drei Messfehler einer ersten Erhebung
und wie sie belegt wurden — die verworfenen Rohdaten liegen als
`data/*_v1_verworfen.*` bei, damit der Unterschied nachvollziehbar ist.
