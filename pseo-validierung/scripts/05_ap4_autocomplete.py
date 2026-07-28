#!/usr/bin/env python3
"""
AP4 - Nachfrage-Proxy ueber Google Autocomplete.

WICHTIG ZUR EVIDENZSTUFE:
Autocomplete liefert KEINE Suchvolumina. Es zeigt nur, welche Fortsetzungen
Google haeufig genug sieht, um sie vorzuschlagen. Als Nachfragebeleg ist das
deutlich schwaecher als ein Keyword-Tool. In dieser Umgebung sind keine
Zugangsdaten fuer DataForSEO/Ahrefs/Sistrix/Google Ads vorhanden (geprueft),
deshalb dieser Proxy.

Gemessen wird:
  1. Welche Staedte schlaegt Google zu "umschulung <beruf> " vor?
     -> Staedte, die ueberhaupt erscheinen, haben nennenswerte Nachfrage.
  2. Erscheint zu "<beruf> <stadt>" ueberhaupt eine Fortsetzung?
     -> Test auf Existenz von Longtail-Nachfrage je Stadtgroesse.

Ergebnis: data/ap4_autocomplete.json + ergebnisse/ap4_autocomplete.json

Aufruf: python3 scripts/05_ap4_autocomplete.py
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BERUFE, ORTE

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ROH = os.path.join(BASE, "data", "ap4_autocomplete.json")
OUT = os.path.join(BASE, "ergebnisse", "ap4_autocomplete.json")

ENDPOINT = "https://suggestqueries.google.com/complete/search"
PAUSE = 1.0

# Berufsbezeichnungen wie sie ein Suchender eintippt
BERUF_SUCHFORM = {
    "Fachinformatiker": "fachinformatiker",
    "Büromanagement": "kaufmann für büromanagement",
    "Pflegefachkraft": "pflegefachkraft",
    "Erzieher": "erzieher",
    "Berufskraftfahrer": "berufskraftfahrer",
    "Elektroniker": "elektroniker",
    "Finanzbuchhaltung": "finanzbuchhaltung",
    "Lagerlogistik": "fachkraft für lagerlogistik",
    "Mechatroniker": "mechatroniker",
    "Steuerfachangestellte": "steuerfachangestellte",
    "Einzelhandel": "kaufmann im einzelhandel",
    "Immobilienkaufmann": "immobilienkaufmann",
    "Sozialassistent": "sozialassistent",
    "Anlagenmechaniker": "anlagenmechaniker",
    "Webentwickler": "webentwickler",
    "Mediengestalter": "mediengestalter",
}


def suggest(q):
    url = ENDPOINT + "?" + urllib.parse.urlencode(
        {"client": "firefox", "hl": "de", "gl": "de", "q": q})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
            return d[1] if len(d) > 1 else []
    except Exception:                                          # noqa: BLE001
        return None


def main():
    staedte = [o[0] for o in ORTE]
    staedte_lower = {s.lower(): s for s in staedte}
    klasse = {o[0]: o[3] for o in ORTE}

    ergebnis = {"erhoben_am": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "hinweis": ("Autocomplete ist kein Suchvolumen. Schwaechere "
                            "Evidenzstufe als ein Keyword-Tool."),
                "berufsachse": {}, "stadtachse": {}}

    # --- 1) Welche Staedte schlaegt Google je Beruf vor? -----------------
    print("1) Staedtevorschlaege je Beruf")
    for beruf, form in BERUF_SUCHFORM.items():
        vor = suggest(f"umschulung {form} ")
        time.sleep(PAUSE)
        staedte_treffer = []
        if vor:
            for v in vor:
                for low, orig in staedte_lower.items():
                    if low in v.lower() and orig not in staedte_treffer:
                        staedte_treffer.append(orig)
        ergebnis["berufsachse"][beruf] = {
            "query": f"umschulung {form} ",
            "vorschlaege": vor,
            "staedte_aus_unserer_liste": staedte_treffer,
            "n_vorschlaege": len(vor) if vor else 0,
        }
        print(f"   {beruf:22s} {len(vor) if vor else 0:2d} Vorschlaege, "
              f"Staedte: {staedte_treffer}")

    # --- 2) Gibt es zu "<beruf> <stadt>" ueberhaupt Vorschlaege? ---------
    print("\n2) Longtail-Test je Stadt (Beruf: fachinformatiker, pflegefachkraft)")
    for beruf in ("fachinformatiker", "pflegefachkraft"):
        ergebnis["stadtachse"][beruf] = {}
        for name, *_rest in ORTE:
            q = f"umschulung {beruf} {name.lower()}"
            vor = suggest(q)
            time.sleep(PAUSE)
            ergebnis["stadtachse"][beruf][name] = {
                "query": q, "klasse": klasse[name],
                "n_vorschlaege": len(vor) if vor else 0,
                "vorschlaege": vor,
            }
            print(f"   {beruf[:16]:16s} {name:20s} {klasse[name]:6s} "
                  f"-> {len(vor) if vor else 0} Vorschlaege")

    os.makedirs(os.path.dirname(ROH), exist_ok=True)
    with open(ROH, "w", encoding="utf-8") as f:
        json.dump(ergebnis, f, ensure_ascii=False, indent=2)

    # --- Auswertung ------------------------------------------------------
    aus = {}
    for beruf, d in ergebnis["stadtachse"].items():
        per_klasse = {}
        for name, v in d.items():
            k = v["klasse"]
            per_klasse.setdefault(k, [0, 0])
            per_klasse[k][1] += 1
            if v["n_vorschlaege"] > 0:
                per_klasse[k][0] += 1
        aus[beruf] = {k: {"staedte_mit_vorschlag": a, "staedte_gesamt": b,
                          "anteil_pct": round(100 * a / b, 1) if b else None}
                      for k, (a, b) in per_klasse.items()}

    staedte_genannt = sorted({s for d in ergebnis["berufsachse"].values()
                              for s in d["staedte_aus_unserer_liste"]})
    zus = {
        "staedte_die_google_ueberhaupt_vorschlaegt": staedte_genannt,
        "davon_klassen": {s: klasse[s] for s in staedte_genannt},
        "longtail_abdeckung_je_stadtklasse": aus,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(zus, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("Staedte, die Google ueberhaupt vorschlaegt:", staedte_genannt)
    for b, d in aus.items():
        print(f"\n{b}:")
        for k, v in d.items():
            print(f"   {k:7s} {v['staedte_mit_vorschlag']}/{v['staedte_gesamt']} "
                  f"= {v['anteil_pct']} % der Staedte mit Vorschlag")
    print(f"\ngeschrieben: {OUT}")


if __name__ == "__main__":
    main()
