#!/usr/bin/env python3
"""
AP6 - Markenrechtliche Vorabpruefung moeglicher Projektnamen.

Abfrage gegen TMview (EUIPO/TMDN), Territorium DE. TMview aggregiert unter
anderem das DPMA-Register. DPMAregister selbst ist eine formularbasierte
Java-Anwendung und laesst sich nicht sauber automatisiert abfragen.

Das ist eine VORABPRUEFUNG, keine markenrechtliche Beurteilung:
geprueft wird nur die Wortidentitaet, nicht Aehnlichkeit, Klassenkollision
oder Verkehrsgeltung. Eine Freigabe ersetzt das nicht.

Ergebnis: ergebnisse/ap6_marken.json
"""
import json
import os
import time
import urllib.request

KANDIDATEN = ["Fördercampus", "Kursgutschein", "Bildungsgutschein24",
              "Weiterbildungsradar", "Umschulungsfinder", "Förderkurs",
              "Kursnavi", "Bildungsnavigator", "Umschulungsradar",
              "Weiterbildungskompass"]

URL = "https://www.tmdn.org/tmview/api/search/results"
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def suche(name):
    body = json.dumps({
        "page": "1", "pageSize": "20", "criteria": "C",
        "basicSearch": name, "territories": ["DE"],
        "fields": ["ST13", "tmName", "applicationNumber", "applicationDate",
                   "tradeMarkStatus", "niceClass", "applicantName"]}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "User-Agent": "Mozilla/5.0 (Marktvalidierung)",
        "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:                                     # noqa: BLE001
        return {"fehler": repr(e)}


def main():
    out = {"erhoben_am": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "quelle": URL, "territorium": "DE",
           "hinweis": ("Nur Wortidentitaets-Vorabpruefung. Keine Pruefung von "
                       "Aehnlichkeit, Nizza-Klassenkollision oder "
                       "Verkehrsgeltung. Ersetzt keine Freigaberecherche."),
           "ergebnisse": {}}
    for n in KANDIDATEN:
        d = suche(n)
        treffer = d.get("tradeMarks", []) if isinstance(d, dict) else []
        out["ergebnisse"][n] = {
            "treffer_gesamt": d.get("totalResults") if isinstance(d, dict) else None,
            "treffer": [{"name": t.get("tmName"),
                         "status": t.get("tradeMarkStatus"),
                         "anmeldenummer": t.get("applicationNumber"),
                         "anmelder": t.get("applicantName"),
                         "klassen": t.get("niceClass")} for t in treffer[:10]],
            "fehler": d.get("fehler") if isinstance(d, dict) else None,
        }
        n_t = out["ergebnisse"][n]["treffer_gesamt"]
        print(f"  {n:24s} Treffer: {n_t}")
        time.sleep(1.5)
    os.makedirs(os.path.join(BASE, "ergebnisse"), exist_ok=True)
    with open(os.path.join(BASE, "ergebnisse", "ap6_marken.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\ngeschrieben: ergebnisse/ap6_marken.json")


if __name__ == "__main__":
    main()
