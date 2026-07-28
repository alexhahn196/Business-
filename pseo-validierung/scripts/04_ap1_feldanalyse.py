#!/usr/bin/env python3
"""
AP1 - Feldstruktur, Vollstaendigkeit, Aktualitaet, Traeger, Geografie.

Zieht eine kleine Rohdaten-Stichprobe (Default 200 Angebote, 1 req/s) und
misst je Feld den Befuellungsgrad. Zusaetzlich Aktualitaet der Termine und
das Verhaeltnis Traegersitz zu Kursort.

Rohdaten:  data/rohdaten_felder.jsonl
Ergebnis:  ergebnisse/ap1_feldanalyse.json

Aufruf: python3 scripts/04_ap1_feldanalyse.py
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (BACKEND_HOST, BERUFE, HEADERS, PAGE_SIZE,
                    RATE_LIMIT_SECONDS)

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ROH = os.path.join(BASE, "data", "rohdaten_felder.jsonl")
OUT = os.path.join(BASE, "ergebnisse", "ap1_feldanalyse.json")

ZIEL_ANGEBOTE = 200


def get(params):
    url = f"{BACKEND_HOST}/pc/v1/bildungsangebot?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode("utf-8"))
    except (urllib.error.HTTPError, Exception):               # noqa: BLE001
        return None


def ziehe():
    """Ein Angebot je Beruf ueber mehrere Seiten, bis ZIEL_ANGEBOTE erreicht."""
    gesehen, raus = set(), []
    seite = 0
    while len(raus) < ZIEL_ANGEBOTE and seite < 4:
        for beruf in BERUFE:
            if len(raus) >= ZIEL_ANGEBOTE:
                break
            d = get({"sw": beruf, "page": seite, "size": PAGE_SIZE})
            time.sleep(RATE_LIMIT_SECONDS)
            if not isinstance(d, dict):
                continue
            for a in (d.get("_embedded", {})
                      .get("bildungsangebotDTOList", []) or []):
                if a.get("id") in gesehen or len(raus) >= ZIEL_ANGEBOTE:
                    continue
                gesehen.add(a.get("id"))
                a["_beruf_query"] = beruf
                raus.append(a)
            print(f"  gezogen {len(raus)}/{ZIEL_ANGEBOTE}", flush=True)
        seite += 1
    return raus


def befuellt(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def main():
    if os.path.exists(ROH):
        angebote = [json.loads(z) for z in open(ROH, encoding="utf-8")
                    if z.strip()]
        print(f"nutze vorhandene Rohdaten: {len(angebote)} Angebote")
    else:
        print("ziehe Rohdaten ...")
        angebote = ziehe()
        os.makedirs(os.path.dirname(ROH), exist_ok=True)
        with open(ROH, "w", encoding="utf-8") as f:
            for a in angebote:
                f.write(json.dumps(a, ensure_ascii=False) + "\n")

    n = len(angebote)
    if not n:
        print("keine Daten")
        return

    # --- Feld-Vollstaendigkeit Angebotsebene ----------------------------
    alle_felder = sorted({k for a in angebote for k in a
                          if not k.startswith("_")})
    feld_pct = {f: round(100 * sum(1 for a in angebote if befuellt(a.get(f)))
                         / n, 1) for f in alle_felder}
    for f in ("name", "logo", "adresse"):
        feld_pct[f"bildungsanbieter.{f}"] = round(
            100 * sum(1 for a in angebote
                      if befuellt((a.get("bildungsanbieter") or {}).get(f)))
            / n, 1)
    for f in ("ort", "plz"):
        feld_pct[f"bildungsanbieter.adresse.{f}"] = round(
            100 * sum(1 for a in angebote
                      if befuellt(((a.get("bildungsanbieter") or {})
                                   .get("adresse") or {}).get(f))) / n, 1)

    # --- Terminebene -----------------------------------------------------
    termine = [t for a in angebote for t in (a.get("termine") or [])]
    nt = len(termine)
    t_felder = sorted({k for t in termine for k in t})
    termin_pct = {f: round(100 * sum(1 for t in termine if befuellt(t.get(f)))
                           / nt, 1) for f in t_felder} if nt else {}

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

    # --- Traeger und Geografie ------------------------------------------
    traeger = Counter(a["bildungsanbieter"]["name"] for a in angebote
                      if (a.get("bildungsanbieter") or {}).get("name"))
    sitze = Counter(((a.get("bildungsanbieter") or {}).get("adresse") or {})
                    .get("ort") for a in angebote
                    if ((a.get("bildungsanbieter") or {}).get("adresse")
                        or {}).get("ort"))
    termin_orte = Counter((t.get("adresse") or {}).get("ort") for t in termine
                          if (t.get("adresse") or {}).get("ort"))

    auswaertig = pruefbar = 0
    for a in angebote:
        sitz = ((a.get("bildungsanbieter") or {}).get("adresse") or {}).get("ort")
        orte = {(t.get("adresse") or {}).get("ort")
                for t in (a.get("termine") or [])} - {None}
        if sitz and orte:
            pruefbar += 1
            if sitz not in orte:
                auswaertig += 1

    inhalt_len = [len(a.get("inhalt") or "") for a in angebote]
    inhalt_len_s = sorted(inhalt_len)

    erg = {
        "stichprobe": {"angebote": n, "termine_im_listing": nt,
                       "hinweis": ("Die Listen-Antwort liefert je Angebot "
                                   "maximal 5 Termine, waehrend anzahlTermine "
                                   "den wahren Wert nennt. Terminfeld-Quoten "
                                   "beziehen sich auf diese 5er-Teilmenge.")},
        "feldvollstaendigkeit_angebot_pct": feld_pct,
        "feldvollstaendigkeit_termin_pct": termin_pct,
        "inhalt_laenge_zeichen": {
            "median": inhalt_len_s[len(inhalt_len_s) // 2],
            "min": min(inhalt_len), "max": max(inhalt_len),
            "anteil_unter_500_zeichen_pct":
                round(100 * sum(1 for x in inhalt_len if x < 500) / n, 1)},
        "aktualitaet": {
            "stichtag": heute.isoformat(),
            "termine_mit_beginn": len(beginne),
            "frueheste": min(beginne).isoformat() if beginne else None,
            "spaeteste": max(beginne).isoformat() if beginne else None,
            "anteil_beginn_vergangen_pct":
                round(100 * vergangen / len(beginne), 1) if beginne else None},
        "traeger": {
            "distinkt": len(traeger),
            "top10_anteil_pct":
                round(100 * sum(c for _, c in traeger.most_common(10))
                      / sum(traeger.values()), 1) if traeger else None,
            "top15": [{"name": k, "angebote": v}
                      for k, v in traeger.most_common(15)]},
        "geografie": {
            "distinkte_traegersitze": len(sitze),
            "distinkte_termin_orte_in_stichprobe": len(termin_orte),
            "traegersitz_ungleich_kursort_pct":
                round(100 * auswaertig / pruefbar, 1) if pruefbar else None,
            "pruefbar_n": pruefbar,
            "top10_traegersitze": [{"ort": k, "angebote": v}
                                   for k, v in sitze.most_common(10)]},
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(erg, f, ensure_ascii=False, indent=2)

    print("=" * 70)
    print(f"AP1 - FELDANALYSE  ({n} Angebote, {nt} Termine)")
    print("=" * 70)
    print("Angebotsfelder (% befuellt):")
    for k, v in sorted(feld_pct.items()):
        print(f"  {k:38s} {v}")
    print("Terminfelder (% befuellt):")
    for k, v in sorted(termin_pct.items()):
        print(f"  {k:38s} {v}")
    a = erg["aktualitaet"]
    print(f"\nAktualitaet {a['frueheste']} .. {a['spaeteste']}  "
          f"({a['anteil_beginn_vergangen_pct']} % Beginn in Vergangenheit)")
    print(f"Traeger distinkt: {erg['traeger']['distinkt']}, "
          f"Top10 {erg['traeger']['top10_anteil_pct']} %")
    print(f"Traegersitz != Kursort: "
          f"{erg['geografie']['traegersitz_ungleich_kursort_pct']} %")
    print(f"Beschreibungstext Median {erg['inhalt_laenge_zeichen']['median']} Zeichen")
    print(f"\ngeschrieben: {OUT}")


if __name__ == "__main__":
    main()
