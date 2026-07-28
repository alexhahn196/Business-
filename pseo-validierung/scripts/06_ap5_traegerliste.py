#!/usr/bin/env python3
"""
AP5 - Traegerliste als Grundlage fuer telefonische Validierung.

Erzeugt aus den bereits erhobenen Stichproben (reichweite.jsonl,
ueberlappung.jsonl, rohdaten_felder.jsonl) eine Liste der haeufigsten
Bildungstraeger mit Sitz, Fachgebieten und Angebotszahl.

WICHTIG: Telefonnummern und Ansprechpartner sind NICHT enthalten. Die
Weiterbildungssuche liefert diese Felder in der Listenantwort nicht; sie
muessten je Traeger einzeln recherchiert werden. Was hier steht, ist
gemessen - nichts davon ist geschaetzt oder ergaenzt.

Ergebnis: ergebnisse/ap5_traegerliste.json + ergebnisse/ap5_traegerliste.md

Aufruf: python3 scripts/06_ap5_traegerliste.py
"""
import json
import os
from collections import defaultdict

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def lade(name):
    p = os.path.join(BASE, "data", name)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(z) for z in f if z.strip()]


def main():
    traeger = defaultdict(lambda: {"angebote": 0, "sitze": defaultdict(int),
                                   "fachgebiete": defaultdict(int),
                                   "staedte": defaultdict(int),
                                   "termine_summe": 0})

    for r in lade("reichweite.jsonl"):
        nm = r.get("traeger")
        if not nm:
            continue
        t = traeger[nm]
        t["angebote"] += 1
        t["termine_summe"] += r.get("anzahlTermine") or 0
        if r.get("traeger_ort"):
            t["sitze"][r["traeger_ort"]] += 1
        t["fachgebiete"][r["beruf"]] += 1

    for r in lade("ueberlappung.jsonl"):
        for a in r.get("angebote", []):
            nm = a.get("traeger")
            if not nm:
                continue
            t = traeger[nm]
            t["angebote"] += 1
            t["termine_summe"] += a.get("anzahlTermine") or 0
            if a.get("traeger_ort"):
                t["sitze"][a["traeger_ort"]] += 1
            t["fachgebiete"][r["beruf"]] += 1
            t["staedte"][r["ort"]] += 1

    liste = []
    for nm, t in traeger.items():
        sitz = max(t["sitze"].items(), key=lambda x: x[1])[0] if t["sitze"] else None
        fach = sorted(t["fachgebiete"].items(), key=lambda x: -x[1])[:4]
        liste.append({
            "traeger": nm,
            "sitz_laut_daten": sitz,
            "angebote_in_stichprobe": t["angebote"],
            "termine_bundesweit_summe": t["termine_summe"],
            "fachgebiete_top": [f for f, _ in fach],
            "in_staedten_der_stichprobe": sorted(t["staedte"]),
            "kontakt": "nicht erhoben - je Traeger einzeln zu recherchieren",
        })
    liste.sort(key=lambda x: -x["angebote_in_stichprobe"])
    top = liste[:30]

    os.makedirs(os.path.join(BASE, "ergebnisse"), exist_ok=True)
    with open(os.path.join(BASE, "ergebnisse", "ap5_traegerliste.json"),
              "w", encoding="utf-8") as f:
        json.dump({"traeger_distinkt_gesamt": len(liste), "top30": top},
                  f, ensure_ascii=False, indent=2)

    zeilen = ["# AP5 - Bildungstraeger aus der Stichprobe",
              "",
              f"Distinkte Traeger in der Stichprobe: **{len(liste)}**",
              "",
              "Grundlage: eigene Messung an der Weiterbildungssuche der "
              "Bundesagentur fuer Arbeit (2026-07-28).",
              "Kontaktdaten sind in der Listenantwort der Schnittstelle nicht "
              "enthalten und wurden bewusst nicht ergaenzt.",
              "",
              "| # | Traeger | Sitz | Angebote (Stichprobe) | Termine bundesweit | Fachgebiete |",
              "|---|---------|------|----------------------:|-------------------:|-------------|"]
    for i, t in enumerate(top, 1):
        zeilen.append(
            f"| {i} | {t['traeger']} | {t['sitz_laut_daten'] or '-'} | "
            f"{t['angebote_in_stichprobe']} | {t['termine_bundesweit_summe']} | "
            f"{', '.join(t['fachgebiete_top'])} |")
    with open(os.path.join(BASE, "ergebnisse", "ap5_traegerliste.md"),
              "w", encoding="utf-8") as f:
        f.write("\n".join(zeilen) + "\n")

    print(f"distinkte Traeger: {len(liste)}")
    for t in top[:15]:
        print(f"  {t['angebote_in_stichprobe']:4d} Angebote | "
              f"{t['termine_bundesweit_summe']:6d} Termine | "
              f"{t['traeger'][:48]:48s} | {t['sitz_laut_daten']}")
    print("\ngeschrieben: ergebnisse/ap5_traegerliste.{json,md}")


if __name__ == "__main__":
    main()
