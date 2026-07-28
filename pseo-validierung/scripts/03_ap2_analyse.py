#!/usr/bin/env python3
"""
AP2 - Differenzierungsanalyse.

Liest data/grid_facetten.jsonl und data/records.jsonl und berechnet:

  1. Verteilung der Angebotszahl je Kombination Beruf x Ort
     (Anteil Seiten mit 0 / 1-2 / 3+ Angeboten)
  2. Distinkte Traeger und Varianz (Dauer, Lernform, Kosten) je Kombination
  3. Duplikats-Simulation fuer Nachbarstadt-Paare im selben Bundesland
  4. Maximal sinnvolle Seitenzahl

Alle Formeln stehen im Klartext im Code. Ergebnis:
  ergebnisse/ap2_ergebnisse.json  (maschinenlesbar)
  Konsolenausgabe                 (lesbar)

Aufruf: python3 scripts/03_ap2_analyse.py
"""
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BERUFE, NACHBARPAARE, ORTE

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
GRID = os.path.join(BASE, "data", "grid_facetten.jsonl")
RECS = os.path.join(BASE, "data", "records.jsonl")
OUT = os.path.join(BASE, "ergebnisse", "ap2_ergebnisse.json")


def lade(pfad):
    zeilen = []
    with open(pfad, encoding="utf-8") as f:
        for z in f:
            z = z.strip()
            if z:
                zeilen.append(json.loads(z))
    return zeilen


def tokens(html):
    """Grobe Wort-Tokenisierung nach HTML-Entfernung (fuer Textvergleich)."""
    txt = re.sub(r"<[^>]+>", " ", html or "")
    txt = re.sub(r"&[a-zA-Z]+;", " ", txt)
    return [t for t in re.findall(r"\w+", txt.lower()) if len(t) > 2]


# ---------------------------------------------------------------------------
# 1) Verteilung Angebotszahl je Beruf x Ort
# ---------------------------------------------------------------------------
def verteilung(grid):
    ok = [g for g in grid if g.get("http_status") == 200
          and g.get("anzahl_angebote") is not None]
    fehler = [g for g in grid if g.get("http_status") != 200]

    n = len(ok)
    b0 = sum(1 for g in ok if g["anzahl_angebote"] == 0)
    b12 = sum(1 for g in ok if 1 <= g["anzahl_angebote"] <= 2)
    b3 = sum(1 for g in ok if g["anzahl_angebote"] >= 3)
    b10 = sum(1 for g in ok if g["anzahl_angebote"] >= 10)
    unter2 = b0 + b12

    per_klasse = defaultdict(lambda: {"n": 0, "0": 0, "1-2": 0, "3+": 0,
                                      "summe_angebote": 0})
    for g in ok:
        k = per_klasse[g["klasse"]]
        k["n"] += 1
        k["summe_angebote"] += g["anzahl_angebote"]
        if g["anzahl_angebote"] == 0:
            k["0"] += 1
        elif g["anzahl_angebote"] <= 2:
            k["1-2"] += 1
        else:
            k["3+"] += 1

    return {
        "kombinationen_gemessen": n,
        "requests_fehlerhaft": len(fehler),
        "anteil_0_angebote_pct": round(100 * b0 / n, 1) if n else None,
        "anteil_1_2_angebote_pct": round(100 * b12 / n, 1) if n else None,
        "anteil_3plus_angebote_pct": round(100 * b3 / n, 1) if n else None,
        "anteil_10plus_angebote_pct": round(100 * b10 / n, 1) if n else None,
        "ABBRUCHKRITERIUM_unter_2_angebote_pct":
            round(100 * unter2 / n, 1) if n else None,
        "je_stadtklasse": {k: {
            **v,
            "anteil_unter_2_pct": round(100 * (v["0"] + v["1-2"]) / v["n"], 1)
                                  if v["n"] else None,
            "median_hinweis": "siehe summe_angebote/n",
        } for k, v in per_klasse.items()},
    }


# ---------------------------------------------------------------------------
# 2) Varianz je Kombination (aus Facetten) + distinkte Traeger (aus Records)
# ---------------------------------------------------------------------------
def varianz(grid, recs):
    ok = [g for g in grid if g.get("http_status") == 200
          and (g.get("anzahl_angebote") or 0) > 0]

    def n_distinct(feld):
        werte = []
        for g in ok:
            d = g.get(feld) or {}
            if isinstance(d, dict):
                werte.append(len([k for k, v in d.items() if v]))
            elif isinstance(d, list):
                werte.append(len(d))
        return werte

    dauer = n_distinct("dauer")
    kosten = n_distinct("kosten")
    foerder = n_distinct("foerderart")

    # Lernformen ist verschachtelt: {VORORT:{...}, DIGITAL:{...}, ...}
    lern = []
    for g in ok:
        lf = g.get("lernformen") or {}
        c = 0
        for _, sub in lf.items():
            if isinstance(sub, dict):
                c += len([k for k, v in sub.items() if v])
        lern.append(c)

    # distinkte Traeger je Kombination aus der Datensatz-Stichprobe
    traeger = defaultdict(set)
    angebote_je_komb = defaultdict(set)
    for r in recs:
        key = (r["beruf"], r["ort"])
        a = r["angebot"]
        nm = (a.get("bildungsanbieter") or {}).get("name")
        if nm:
            traeger[key].add(nm)
        angebote_je_komb[key].add(a.get("id"))

    tz = [len(v) for v in traeger.values()]

    def mw(xs):
        return round(sum(xs) / len(xs), 2) if xs else None

    def median(xs):
        if not xs:
            return None
        s = sorted(xs)
        m = len(s) // 2
        return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2

    return {
        "basis_kombinationen_mit_angeboten": len(ok),
        "distinkte_dauerklassen": {"mittel": mw(dauer), "median": median(dauer),
                                   "max": max(dauer) if dauer else None},
        "distinkte_kostenklassen": {"mittel": mw(kosten),
                                    "median": median(kosten)},
        "distinkte_foerderarten": {"mittel": mw(foerder),
                                   "median": median(foerder),
                                   "max": max(foerder) if foerder else None},
        "distinkte_lernformen": {"mittel": mw(lern), "median": median(lern)},
        "traeger_je_kombination_stichprobe": {
            "n_kombinationen": len(tz), "mittel": mw(tz),
            "median": median(tz), "max": max(tz) if tz else None,
            "anteil_mit_1_traeger_pct":
                round(100 * sum(1 for x in tz if x <= 1) / len(tz), 1)
                if tz else None,
        },
    }


# ---------------------------------------------------------------------------
# 3) Duplikats-Simulation Nachbarstaedte
# ---------------------------------------------------------------------------
def duplikate(recs, boilerplate_anteile=(0.40, 0.60)):
    """
    Misst fuer jedes Nachbarpaar und jeden Beruf:
      - Jaccard-Ueberschneidung der Angebots-IDs
      - Containment (Anteil der Angebote von Stadt A, die auch in B liegen)
      - Token-Ueberschneidung der Beschreibungstexte (inhalt)

    Danach: Anteil identischen Seiteninhalts bei Standard-Template.
      Formel: identisch = B + (1 - B) * token_ueberschneidung
      B = Boilerplate-Anteil der Seite (Intro, Foerder-Erklaerung, FAQ, CTA),
          der bei einem Standard-Template zwischen zwei Stadtseiten
          konstruktionsbedingt identisch ist.
    """
    idx = defaultdict(list)
    for r in recs:
        idx[(r["beruf"], r["ort"])].append(r["angebot"])

    paare = []
    for a, b in NACHBARPAARE:
        for beruf in BERUFE:
            ra, rb = idx.get((beruf, a)), idx.get((beruf, b))
            if not ra or not rb:
                continue
            ida = {x.get("id") for x in ra}
            idb = {x.get("id") for x in rb}
            schnitt = ida & idb
            union = ida | idb
            ta, tb = set(), set()
            for x in ra:
                ta |= set(tokens(x.get("inhalt")))
                ta |= set(tokens(x.get("titel")))
            for x in rb:
                tb |= set(tokens(x.get("inhalt")))
                tb |= set(tokens(x.get("titel")))
            tok_j = len(ta & tb) / len(ta | tb) if (ta | tb) else 0.0

            traeger_a = {(x.get("bildungsanbieter") or {}).get("name")
                         for x in ra}
            traeger_b = {(x.get("bildungsanbieter") or {}).get("name")
                         for x in rb}
            tr_union = (traeger_a | traeger_b) - {None}
            tr_schnitt = (traeger_a & traeger_b) - {None}

            paare.append({
                "paar": f"{a}/{b}", "beruf": beruf,
                "n_angebote_a": len(ida), "n_angebote_b": len(idb),
                "angebote_identisch": len(schnitt),
                "jaccard_angebots_ids": round(len(schnitt) / len(union), 3)
                                        if union else None,
                "containment_a_in_b": round(len(schnitt) / len(ida), 3)
                                      if ida else None,
                "token_ueberschneidung_text": round(tok_j, 3),
                "traeger_jaccard": round(len(tr_schnitt) / len(tr_union), 3)
                                   if tr_union else None,
            })

    if not paare:
        return {"hinweis": "keine vergleichbaren Paare in der Stichprobe"}

    def mw(key):
        xs = [p[key] for p in paare if p.get(key) is not None]
        return round(sum(xs) / len(xs), 3) if xs else None

    tok_mw = mw("token_ueberschneidung_text")
    szenarien = {}
    for B in boilerplate_anteile:
        szenarien[f"boilerplate_{int(B*100)}pct"] = {
            "formel": "identisch = B + (1-B) * token_ueberschneidung",
            "B": B,
            "token_ueberschneidung": tok_mw,
            "anteil_identischer_seiteninhalt_pct":
                round(100 * (B + (1 - B) * tok_mw), 1)
                if tok_mw is not None else None,
        }

    return {
        "n_vergleiche": len(paare),
        "mittelwerte": {
            "jaccard_angebots_ids": mw("jaccard_angebots_ids"),
            "containment_a_in_b": mw("containment_a_in_b"),
            "token_ueberschneidung_text": tok_mw,
            "traeger_jaccard": mw("traeger_jaccard"),
        },
        "template_szenarien": szenarien,
        "einzelvergleiche": paare,
    }


# ---------------------------------------------------------------------------
# 4) Maximal sinnvolle Seitenzahl
# ---------------------------------------------------------------------------
def seitenzahl(grid, schwelle=3):
    """
    Hochrechnung auf das Gesamtuniversum.

    Formel:
      seiten_sinnvoll = anteil_kombis_mit_>=schwelle_angeboten
                        * n_berufe_gesamt * n_orte_gesamt

    Annahmen (explizit):
      n_orte_gesamt   = 2.056 Staedte in DE ab 5.000 Einwohnern
                        (Destatis-Groessenordnung, gerundet)
      n_berufe_gesamt = 250 realistisch bespielbare Weiterbildungs-/
                        Umschulungsberufe
    Die Stichprobe ist bei den Orten bewusst zugunsten grosser Staedte
    verzerrt (14 von 30 Grossstaedte, real ca. 80 von 2.056). Deshalb
    zusaetzlich eine einwohnergewichtete Variante.
    """
    ok = [g for g in grid if g.get("http_status") == 200
          and g.get("anzahl_angebote") is not None]
    if not ok:
        return {}

    anteil_roh = sum(1 for g in ok if g["anzahl_angebote"] >= schwelle) / len(ok)

    # realitaetsnaehere Gewichtung: Verteilung der deutschen Staedte
    # ab 5.000 EW auf die drei Klassen (Destatis-Groessenordnung)
    real_verteilung = {"GROSS": 80, "MITTEL": 620, "KLEIN": 1356}
    per_klasse = defaultdict(lambda: [0, 0])
    for g in ok:
        per_klasse[g["klasse"]][1] += 1
        if g["anzahl_angebote"] >= schwelle:
            per_klasse[g["klasse"]][0] += 1

    gew_zaehler = 0.0
    gew_nenner = 0
    klassen_detail = {}
    for k, n_real in real_verteilung.items():
        tref, ges = per_klasse.get(k, [0, 0])
        q = tref / ges if ges else 0.0
        klassen_detail[k] = {"anteil_>=%d_in_stichprobe" % schwelle:
                             round(q, 3),
                             "staedte_real": n_real,
                             "stichprobe_n": ges}
        gew_zaehler += q * n_real
        gew_nenner += n_real
    anteil_gew = gew_zaehler / gew_nenner if gew_nenner else 0.0

    N_ORTE, N_BERUFE = 2056, 250
    return {
        "schwelle_angebote": schwelle,
        "annahmen": {"n_orte_gesamt": N_ORTE, "n_berufe_gesamt": N_BERUFE,
                     "theoretisch_moegliche_seiten": N_ORTE * N_BERUFE},
        "anteil_tragfaehig_ungewichtet": round(anteil_roh, 3),
        "anteil_tragfaehig_einwohnergewichtet": round(anteil_gew, 3),
        "klassen_detail": klassen_detail,
        "seiten_ungewichtet": int(anteil_roh * N_ORTE * N_BERUFE),
        "seiten_einwohnergewichtet": int(anteil_gew * N_ORTE * N_BERUFE),
    }


def main():
    grid = lade(GRID)
    recs = lade(RECS) if os.path.exists(RECS) else []

    erg = {
        "stichprobe": {
            "grid_requests": len(grid),
            "datensaetze_gezogen": len(recs),
            "berufe": len(BERUFE), "orte": len(ORTE),
        },
        "1_verteilung": verteilung(grid),
        "2_varianz": varianz(grid, recs),
        "3_duplikate_nachbarstaedte": duplikate(recs),
        "4_seitenzahl": seitenzahl(grid, schwelle=3),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(erg, f, ensure_ascii=False, indent=2)

    v = erg["1_verteilung"]
    print("=" * 68)
    print("AP2 - DIFFERENZIERUNGSANALYSE")
    print("=" * 68)
    print(f"Kombinationen gemessen : {v['kombinationen_gemessen']}")
    print(f"Datensaetze gezogen    : {len(recs)}")
    print(f"  0 Angebote           : {v['anteil_0_angebote_pct']} %")
    print(f"  1-2 Angebote         : {v['anteil_1_2_angebote_pct']} %")
    print(f"  3+ Angebote          : {v['anteil_3plus_angebote_pct']} %")
    print(f"  10+ Angebote         : {v['anteil_10plus_angebote_pct']} %")
    print(f"  --> < 2 Angebote     : "
          f"{v['ABBRUCHKRITERIUM_unter_2_angebote_pct']} %  "
          f"(Abbruchkriterium: > 50 %)")
    print("\nJe Stadtklasse:")
    for k, d in v["je_stadtklasse"].items():
        print(f"  {k:7s} n={d['n']:4d}  <2 Angebote: {d['anteil_unter_2_pct']} %")
    d = erg["3_duplikate_nachbarstaedte"]
    if "mittelwerte" in d:
        print("\nNachbarstadt-Duplikate:")
        print(f"  Vergleiche               : {d['n_vergleiche']}")
        print(f"  Jaccard Angebots-IDs     : {d['mittelwerte']['jaccard_angebots_ids']}")
        print(f"  Containment A in B       : {d['mittelwerte']['containment_a_in_b']}")
        print(f"  Token-Ueberschneidung    : {d['mittelwerte']['token_ueberschneidung_text']}")
        print(f"  Traeger-Jaccard          : {d['mittelwerte']['traeger_jaccard']}")
        for k, s in d["template_szenarien"].items():
            print(f"  {k}: {s['anteil_identischer_seiteninhalt_pct']} % identisch")
    s = erg["4_seitenzahl"]
    if s:
        print("\nSeitenzahl:")
        print(f"  theoretisch              : {s['annahmen']['theoretisch_moegliche_seiten']:,}")
        print(f"  tragfaehig (ungewichtet) : {s['seiten_ungewichtet']:,}")
        print(f"  tragfaehig (gewichtet)   : {s['seiten_einwohnergewichtet']:,}")
    print(f"\ngeschrieben: {OUT}")


if __name__ == "__main__":
    main()
