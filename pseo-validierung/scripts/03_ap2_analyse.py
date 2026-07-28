#!/usr/bin/env python3
"""
AP2 - Differenzierungsanalyse (Fassung 2).

Eingabe:
  data/grid_facetten.jsonl   Aggregate je Beruf x Ort  (Umkreis 5 km)
  data/ueberlappung.jsonl    vollstaendige Angebots-ID-Listen je Beruf x Ort
  data/reichweite.jsonl      bundesweite Angebote je Beruf inkl. anzahlTermine

Ausgabe:
  ergebnisse/ap2_ergebnisse.json  + Konsolenreport

Alle Formeln stehen im Klartext im Code.
Aufruf: python3 scripts/03_ap2_analyse.py
"""
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import FERNPAARE, NACHBARPAARE

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(BASE, "ergebnisse", "ap2_ergebnisse.json")


def lade(name):
    p = os.path.join(BASE, "data", name)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(z) for z in f if z.strip()]


def tokens(txt):
    t = re.sub(r"<[^>]+>", " ", txt or "")
    t = re.sub(r"&[a-zA-Z#0-9]+;", " ", t)
    return {w for w in re.findall(r"\w+", t.lower()) if len(w) > 3}


def mw(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 3) if xs else None


def median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


# ---------------------------------------------------------------------------
# 1) Verteilung der Angebotszahl je Beruf x Ort
# ---------------------------------------------------------------------------
def verteilung(grid):
    ok = [g for g in grid if g.get("http_status") == 200
          and g.get("anzahl_angebote") is not None]
    n = len(ok)
    if not n:
        return {"fehler": "keine gueltigen Grid-Zeilen"}
    b0 = sum(1 for g in ok if g["anzahl_angebote"] == 0)
    b12 = sum(1 for g in ok if 1 <= g["anzahl_angebote"] <= 2)
    b3 = sum(1 for g in ok if g["anzahl_angebote"] >= 3)

    per = defaultdict(list)
    for g in ok:
        per[g["klasse"]].append(g["anzahl_angebote"])

    return {
        "kombinationen_gemessen": n,
        "requests_fehlerhaft": sum(1 for g in grid
                                   if g.get("http_status") != 200),
        "anteil_0_pct": round(100 * b0 / n, 1),
        "anteil_1_2_pct": round(100 * b12 / n, 1),
        "anteil_3plus_pct": round(100 * b3 / n, 1),
        "ABBRUCH_anteil_unter_2_pct": round(100 * (b0 + b12) / n, 1),
        "median_angebote": median([g["anzahl_angebote"] for g in ok]),
        "je_stadtklasse": {
            k: {"n": len(v), "median": median(v),
                "anteil_unter_2_pct": round(100 * sum(1 for x in v if x < 2)
                                            / len(v), 1)}
            for k, v in per.items()},
    }


# ---------------------------------------------------------------------------
# 2) Varianz je Kombination (aus den Facetten)
# ---------------------------------------------------------------------------
def varianz(grid):
    ok = [g for g in grid if g.get("http_status") == 200
          and (g.get("anzahl_angebote") or 0) > 0]

    def anz(feld):
        out = []
        for g in ok:
            d = g.get(feld)
            if isinstance(d, dict):
                out.append(len([k for k, v in d.items() if v]))
            elif isinstance(d, list):
                out.append(len(d))
        return out

    lern = []
    for g in ok:
        lf = g.get("lernformen") or {}
        lern.append(sum(len([k for k, v in sub.items() if v])
                        for sub in lf.values() if isinstance(sub, dict)))

    return {
        "basis_kombinationen_mit_angeboten": len(ok),
        "dauerklassen": {"mittel": mw(anz("dauer")),
                         "median": median(anz("dauer"))},
        "kostenklassen": {"mittel": mw(anz("kosten")),
                          "median": median(anz("kosten"))},
        "foerderarten": {"mittel": mw(anz("foerderart")),
                         "median": median(anz("foerderart")),
                         "max": max(anz("foerderart") or [0])},
        "lernformen": {"mittel": mw(lern), "median": median(lern)},
    }


# ---------------------------------------------------------------------------
# 3) Ueberschneidung zwischen Staedten  (KERNMESSUNG)
# ---------------------------------------------------------------------------
def ueberlappung(ueb, boilerplate=(0.40, 0.60)):
    idx = {(r["beruf"], r["ort"]): r for r in ueb}
    unvollstaendig = [f'{r["beruf"]}/{r["ort"]}' for r in ueb
                      if not r.get("vollstaendig")]

    def vergleich(a, b, typ):
        raus = []
        for (beruf, ort), r in idx.items():
            if ort != a:
                continue
            rb = idx.get((beruf, b))
            if not rb:
                continue
            ida = {x["id"] for x in r["angebote"]}
            idb = {x["id"] for x in rb["angebote"]}
            if not ida or not idb:
                continue
            schnitt, union = ida & idb, ida | idb
            ta = set()
            tb = set()
            for x in r["angebote"]:
                ta |= tokens(x.get("inhalt")) | tokens(x.get("titel"))
            for x in rb["angebote"]:
                tb |= tokens(x.get("inhalt")) | tokens(x.get("titel"))
            tra = {x.get("traeger") for x in r["angebote"]} - {None}
            trb = {x.get("traeger") for x in rb["angebote"]} - {None}
            raus.append({
                "typ": typ, "paar": f"{a}/{b}", "beruf": beruf,
                "n_a": len(ida), "n_b": len(idb),
                "identische_angebote": len(schnitt),
                "jaccard_ids": round(len(schnitt) / len(union), 3),
                "containment_kleinere_in_groessere":
                    round(len(schnitt) / min(len(ida), len(idb)), 3),
                "token_ueberschneidung":
                    round(len(ta & tb) / len(ta | tb), 3) if (ta | tb) else None,
                "traeger_jaccard":
                    round(len((tra & trb)) / len(tra | trb), 3)
                    if (tra | trb) else None,
                "vollstaendig": bool(r.get("vollstaendig")
                                     and rb.get("vollstaendig")),
            })
        return raus

    alle = []
    for a, b in NACHBARPAARE:
        alle += vergleich(a, b, "nachbar")
    for a, b in FERNPAARE:
        alle += vergleich(a, b, "fern")

    if not alle:
        return {"hinweis": "keine vergleichbaren Paare"}

    def block(typ):
        # Nur vollstaendig paginierte Paare: bei abgeschnittenen Listen waere
        # die Schnittmenge systematisch zu klein und die Aussage wertlos.
        s = [x for x in alle if x["typ"] == typ and x["vollstaendig"]]
        if not s:
            return None
        tok = mw([x["token_ueberschneidung"] for x in s])
        return {
            "n_vergleiche": len(s),
            "jaccard_ids": mw([x["jaccard_ids"] for x in s]),
            "containment": mw([x["containment_kleinere_in_groessere"]
                               for x in s]),
            "token_ueberschneidung": tok,
            "traeger_jaccard": mw([x["traeger_jaccard"] for x in s]),
            "beruecksichtigte_berufe": sorted({x["beruf"] for x in s}),
            "ausgeschlossen_unvollstaendig": len(
                [x for x in alle if x["typ"] == typ and not x["vollstaendig"]]),
            "template_szenarien": {
                f"boilerplate_{int(B*100)}pct": {
                    "formel": "identisch = B + (1-B) * token_ueberschneidung",
                    "B": B,
                    "anteil_identischer_seiteninhalt_pct":
                        round(100 * (B + (1 - B) * tok), 1)
                        if tok is not None else None,
                } for B in boilerplate},
        }

    return {
        "hinweis_boilerplate": (
            "B = Anteil der Seite, der bei einem Standard-Template zwischen "
            "zwei Stadtseiten konstruktionsbedingt gleich ist (Intro, "
            "Foerder-Erklaerung, FAQ, Navigation, CTA). B ist eine ANNAHME, "
            "keine Messung. Gemessen ist nur token_ueberschneidung."),
        "kombinationen_unvollstaendig_paginiert": unvollstaendig,
        "nachbarstaedte": block("nachbar"),
        "fernstaedte_kontrolle": block("fern"),
        "einzelvergleiche": alle,
    }


# ---------------------------------------------------------------------------
# 4) Bundesweite Reichweite der Angebote
# ---------------------------------------------------------------------------
def reichweite(reich):
    if not reich:
        return {}
    at = [r.get("anzahlTermine") or 0 for r in reich]
    verzerrt = [r["beruf"] for r in reich if r.get("removedToken")]
    je_beruf = {}
    for r in reich:
        je_beruf.setdefault(r["beruf"], r.get("total_bundesweit"))
    traeger = defaultdict(int)
    for r in reich:
        if r.get("traeger"):
            traeger[r["traeger"]] += 1
    summe = sum(traeger.values())
    top10 = sorted(traeger.items(), key=lambda x: -x[1])[:10]
    return {
        "angebote_in_stichprobe": len(reich),
        "anzahlTermine": {
            "median": median(at), "mittel": mw(at), "max": max(at),
            "anteil_ueber_10_termine_pct":
                round(100 * sum(1 for x in at if x > 10) / len(at), 1),
            "anteil_ueber_50_termine_pct":
                round(100 * sum(1 for x in at if x > 50) / len(at), 1),
            "anteil_genau_1_termin_pct":
                round(100 * sum(1 for x in at if x == 1) / len(at), 1),
        },
        "bundesweite_treffer_je_beruf": je_beruf,
        "berufe_mit_query_verzerrung": sorted(set(verzerrt)),
        "traeger": {
            "distinkt": len(traeger),
            "top10_anteil_pct": round(100 * sum(c for _, c in top10) / summe, 1)
                                if summe else None,
            "top10": [{"name": k, "angebote": v} for k, v in top10],
        },
    }


# ---------------------------------------------------------------------------
# 5) Maximal sinnvolle Seitenzahl
# ---------------------------------------------------------------------------
def seitenzahl(grid, schwelle=3):
    """
    seiten = anteil_kombis_mit_>=schwelle * n_orte * n_berufe

    Annahmen (explizit, nicht gemessen):
      n_orte   = 2.056 Gemeinden ab 5.000 Einwohnern
      n_berufe = 250 bespielbare Weiterbildungsberufe
    Zusaetzlich einwohnergewichtete Variante, weil die Stichprobe
    Grossstaedte ueberrepraesentiert (12 von 24 statt 80 von 2.056).
    """
    ok = [g for g in grid if g.get("http_status") == 200
          and g.get("anzahl_angebote") is not None]
    if not ok:
        return {}
    roh = sum(1 for g in ok if g["anzahl_angebote"] >= schwelle) / len(ok)

    real = {"GROSS": 80, "MITTEL": 620, "KLEIN": 1356}
    per = defaultdict(lambda: [0, 0])
    for g in ok:
        per[g["klasse"]][1] += 1
        if g["anzahl_angebote"] >= schwelle:
            per[g["klasse"]][0] += 1
    z = sum((per[k][0] / per[k][1] if per[k][1] else 0) * n
            for k, n in real.items())
    gew = z / sum(real.values())

    N_ORTE, N_BERUFE = 2056, 250
    return {
        "schwelle": schwelle,
        "annahmen": {"n_orte": N_ORTE, "n_berufe": N_BERUFE,
                     "theoretisch": N_ORTE * N_BERUFE},
        "anteil_tragfaehig_ungewichtet": round(roh, 3),
        "anteil_tragfaehig_gewichtet": round(gew, 3),
        "seiten_ungewichtet": int(roh * N_ORTE * N_BERUFE),
        "seiten_gewichtet": int(gew * N_ORTE * N_BERUFE),
        "klassen": {k: {"anteil": round(per[k][0] / per[k][1], 3)
                        if per[k][1] else None, "stichprobe_n": per[k][1],
                        "staedte_real": n} for k, n in real.items()},
    }


def main():
    grid = lade("grid_facetten.jsonl")
    ueb = lade("ueberlappung.jsonl")
    reich = lade("reichweite.jsonl")

    erg = {
        "stichprobe": {"grid_zeilen": len(grid),
                       "ueberlappungs_kombinationen": len(ueb),
                       "reichweite_angebote": len(reich)},
        "1_verteilung": verteilung(grid),
        "2_varianz": varianz(grid),
        "3_ueberlappung": ueberlappung(ueb),
        "4_reichweite": reichweite(reich),
        "5_seitenzahl": seitenzahl(grid),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(erg, f, ensure_ascii=False, indent=2)

    v = erg["1_verteilung"]
    print("=" * 70)
    print("AP2 - DIFFERENZIERUNGSANALYSE")
    print("=" * 70)
    if "fehler" not in v:
        print(f"Kombinationen Beruf x Ort : {v['kombinationen_gemessen']}")
        print(f"  0 Angebote   : {v['anteil_0_pct']} %")
        print(f"  1-2 Angebote : {v['anteil_1_2_pct']} %")
        print(f"  3+ Angebote  : {v['anteil_3plus_pct']} %")
        print(f"  -> < 2       : {v['ABBRUCH_anteil_unter_2_pct']} %   "
              f"[Abbruch bei > 50 %]")
        print(f"  Median Angebote je Seite: {v['median_angebote']}")
        for k, d in v["je_stadtklasse"].items():
            print(f"    {k:7s} n={d['n']:3d} median={d['median']:6} "
                  f"<2: {d['anteil_unter_2_pct']} %")
    r = erg["4_reichweite"]
    if r:
        a = r["anzahlTermine"]
        print(f"\nBundesweite Reichweite je Angebot (n={r['angebote_in_stichprobe']}):")
        print(f"  Median Termine   : {a['median']}")
        print(f"  >10 Termine      : {a['anteil_ueber_10_termine_pct']} %")
        print(f"  >50 Termine      : {a['anteil_ueber_50_termine_pct']} %")
        print(f"  genau 1 Termin   : {a['anteil_genau_1_termin_pct']} %")
        print(f"  Top-10-Traeger halten {r['traeger']['top10_anteil_pct']} % "
              f"der Angebote ({r['traeger']['distinkt']} Traeger distinkt)")
    u = erg["3_ueberlappung"]
    for lab in ("nachbarstaedte", "fernstaedte_kontrolle"):
        b = u.get(lab)
        if b:
            print(f"\n{lab} (n={b['n_vergleiche']}):")
            print(f"  Jaccard Angebots-IDs : {b['jaccard_ids']}")
            print(f"  Containment          : {b['containment']}")
            print(f"  Token-Ueberschneidung: {b['token_ueberschneidung']}")
            print(f"  Traeger-Jaccard      : {b['traeger_jaccard']}")
            for k, s in b["template_szenarien"].items():
                print(f"    {k}: {s['anteil_identischer_seiteninhalt_pct']} % identisch")
    s = erg["5_seitenzahl"]
    if s:
        print(f"\nSeitenzahl: theoretisch {s['annahmen']['theoretisch']:,} | "
              f"tragfaehig ungew. {s['seiten_ungewichtet']:,} | "
              f"gewichtet {s['seiten_gewichtet']:,}")
    print(f"\ngeschrieben: {OUT}")


if __name__ == "__main__":
    main()
