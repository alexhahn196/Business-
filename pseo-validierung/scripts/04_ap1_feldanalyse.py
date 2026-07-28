#!/usr/bin/env python3
"""
AP1 - Feldstruktur, Vollstaendigkeit, Aktualitaet, Traeger, Geografie.

Liest data/records.jsonl (Stichprobe aus 02_sample.py) und berechnet
je Feld den Befuellungsgrad sowie Kennzahlen zu Traegern und Aktualitaet.

Ergebnis: ergebnisse/ap1_feldanalyse.json + Konsolenausgabe

Aufruf: python3 scripts/04_ap1_feldanalyse.py
"""
import datetime as dt
import json
import os
import sys
from collections import Counter, defaultdict

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RECS = os.path.join(BASE, "data", "records.jsonl")
OUT = os.path.join(BASE, "ergebnisse", "ap1_feldanalyse.json")


def lade(pfad):
    with open(pfad, encoding="utf-8") as f:
        return [json.loads(z) for z in f if z.strip()]


def befuellt(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def main():
    rows = lade(RECS)
    angebote = [r["angebot"] for r in rows]
    # Deduplizierung auf Angebots-ID: dieselbe ID kann in mehreren
    # Beruf/Ort-Abfragen auftauchen.
    uniq = {}
    for a in angebote:
        uniq[a.get("id")] = a
    uniq_list = list(uniq.values())

    n = len(angebote)
    nu = len(uniq_list)

    # --- Feld-Vollstaendigkeit auf Angebotsebene -------------------------
    ANGEBOT_FELDER = ["id", "titel", "inhalt", "weiterbildungsart",
                      "anzahlTermine", "bildungsanbieter", "termine"]
    feld_pct = {}
    for f in ANGEBOT_FELDER:
        c = sum(1 for a in uniq_list if befuellt(a.get(f)))
        feld_pct[f] = round(100 * c / nu, 1) if nu else None

    # verschachtelt: bildungsanbieter
    ba_felder = ["name", "logo", "adresse"]
    for f in ba_felder:
        c = sum(1 for a in uniq_list
                if befuellt((a.get("bildungsanbieter") or {}).get(f)))
        feld_pct[f"bildungsanbieter.{f}"] = round(100 * c / nu, 1) if nu else None
    c = sum(1 for a in uniq_list
            if befuellt(((a.get("bildungsanbieter") or {}).get("adresse")
                         or {}).get("ort")))
    feld_pct["bildungsanbieter.adresse.ort"] = round(100 * c / nu, 1) if nu else None

    # --- Feld-Vollstaendigkeit auf Terminebene ---------------------------
    termine = [t for a in uniq_list for t in (a.get("termine") or [])]
    nt = len(termine)
    TERMIN_FELDER = ["id", "beginn", "ende", "dauer", "dauerId", "kostenWert",
                     "kostenWaehrung", "unterrichtsform", "unterrichtszeit",
                     "adresse", "quelle"]
    termin_pct = {}
    for f in TERMIN_FELDER:
        c = sum(1 for t in termine if befuellt(t.get(f)))
        termin_pct[f] = round(100 * c / nt, 1) if nt else None

    # --- Aktualitaet -----------------------------------------------------
    heute = dt.date.today()
    beginne = []
    for t in termine:
        b = t.get("beginn")
        if isinstance(b, (int, float)) and b > 0:
            try:
                beginne.append(dt.datetime.utcfromtimestamp(b / 1000).date())
            except (OSError, ValueError, OverflowError):
                pass
    vergangen = sum(1 for d in beginne if d < heute)
    aktualitaet = {
        "termine_mit_beginndatum": len(beginne),
        "termine_gesamt": nt,
        "frueheste": min(beginne).isoformat() if beginne else None,
        "spaeteste": max(beginne).isoformat() if beginne else None,
        "anteil_beginn_in_vergangenheit_pct":
            round(100 * vergangen / len(beginne), 1) if beginne else None,
        "stichtag": heute.isoformat(),
    }

    # --- Traeger ---------------------------------------------------------
    traeger = Counter()
    traeger_ort = Counter()
    for a in uniq_list:
        ba = a.get("bildungsanbieter") or {}
        if ba.get("name"):
            traeger[ba["name"]] += 1
        o = (ba.get("adresse") or {}).get("ort")
        if o:
            traeger_ort[o] += 1
    top = traeger.most_common(15)
    summe = sum(traeger.values())
    top10_anteil = (round(100 * sum(c for _, c in traeger.most_common(10))
                          / summe, 1) if summe else None)

    # --- Geografie: Termin-Orte -----------------------------------------
    termin_orte = Counter()
    for t in termine:
        o = (t.get("adresse") or {}).get("ort")
        if o:
            termin_orte[o] += 1

    # --- Traegersitz vs. Kursort ----------------------------------------
    auswaertig = 0
    pruefbar = 0
    for a in uniq_list:
        sitz = ((a.get("bildungsanbieter") or {}).get("adresse")
                or {}).get("ort")
        orte_t = {(t.get("adresse") or {}).get("ort")
                  for t in (a.get("termine") or [])} - {None}
        if sitz and orte_t:
            pruefbar += 1
            if sitz not in orte_t:
                auswaertig += 1

    # --- Angebotsreichweite: wie viele Termine hat ein Angebot? ----------
    at = [a.get("anzahlTermine") or 0 for a in uniq_list]
    at_sorted = sorted(at)
    erg = {
        "stichprobe": {
            "datensaetze_gezogen": n,
            "distinkte_angebote": nu,
            "termine_in_stichprobe": nt,
            "abfragen_beruf_ort": len({(r["beruf"], r["ort"]) for r in rows}),
        },
        "feldvollstaendigkeit_angebot_pct": feld_pct,
        "feldvollstaendigkeit_termin_pct": termin_pct,
        "aktualitaet": aktualitaet,
        "traeger": {
            "distinkte_traeger": len(traeger),
            "angebote_pro_traeger_mittel":
                round(summe / len(traeger), 2) if traeger else None,
            "top10_anteil_an_angeboten_pct": top10_anteil,
            "top15": [{"name": k, "angebote": v} for k, v in top],
        },
        "geografie": {
            "distinkte_termin_orte": len(termin_orte),
            "top15_termin_orte": [{"ort": k, "termine": v}
                                  for k, v in termin_orte.most_common(15)],
            "distinkte_traegersitze": len(traeger_ort),
            "traegersitz_ungleich_kursort_pct":
                round(100 * auswaertig / pruefbar, 1) if pruefbar else None,
            "traegersitz_pruefbar_n": pruefbar,
        },
        "angebotsreichweite": {
            "anzahlTermine_median":
                at_sorted[len(at_sorted) // 2] if at_sorted else None,
            "anzahlTermine_mittel":
                round(sum(at) / len(at), 1) if at else None,
            "anzahlTermine_max": max(at) if at else None,
            "anteil_angebote_mit_ueber_10_terminen_pct":
                round(100 * sum(1 for x in at if x > 10) / len(at), 1)
                if at else None,
        },
        "hinweis_felder": (
            "Die Listen-Antwort /pc/v1/bildungsangebot liefert einen "
            "reduzierten Feldsatz. Foerderart, Abschluss und Zertifizierer "
            "sind nur ueber die Detail-Ressource /pc/v1/bildungsangebot/{id} "
            "bzw. die Facetten-Aggregation verfuegbar."
        ),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(erg, f, ensure_ascii=False, indent=2)

    print("=" * 68)
    print("AP1 - FELDSTRUKTUR UND VOLLSTAENDIGKEIT")
    print("=" * 68)
    print(f"Datensaetze {n}, distinkte Angebote {nu}, Termine {nt}")
    print("\nAngebotsfelder (% befuellt):")
    for k, v in feld_pct.items():
        print(f"  {k:36s} {v}")
    print("\nTerminfelder (% befuellt):")
    for k, v in termin_pct.items():
        print(f"  {k:36s} {v}")
    print(f"\nAktualitaet: {aktualitaet['frueheste']} .. "
          f"{aktualitaet['spaeteste']}, "
          f"{aktualitaet['anteil_beginn_in_vergangenheit_pct']} % vergangen")
    print(f"\nTraeger: {erg['traeger']['distinkte_traeger']} distinkt, "
          f"Top10 halten {top10_anteil} % der Angebote")
    for t in top[:8]:
        print(f"  {t[1]:4d}  {t[0][:60]}")
    print(f"\nTraegersitz != Kursort: "
          f"{erg['geografie']['traegersitz_ungleich_kursort_pct']} %")
    print(f"Angebote mit >10 Terminen bundesweit: "
          f"{erg['angebotsreichweite']['anteil_angebote_mit_ueber_10_terminen_pct']} %")
    print(f"\ngeschrieben: {OUT}")


if __name__ == "__main__":
    main()
