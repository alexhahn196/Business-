#!/usr/bin/env python3
"""
AP1 - Schritt 1: Welche Endpunkte der BA-Weiterbildungssuche sind erreichbar?

Prueft den in der bundesAPI-Dokumentation genannten Endpunkt gegen den
tatsaechlich vom NOW-Frontend genutzten Endpunkt. Ergebnis nach
data/ap1_endpoint_probe.json.

Aufruf: python3 scripts/01_ap1_endpoint_probe.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import HEADERS, RATE_LIMIT_SECONDS, USER_AGENT

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data",
                   "ap1_endpoint_probe.json")

KANDIDATEN = [
    # (Label, URL, API-Key-Header-Wert)
    ("bundesAPI-Doku v2 (dokumentierter Endpunkt)",
     "https://rest.arbeitsagentur.de/infosysbub/wbsuche/pc/v2/bildungsangebot"
     "?orte=Erlangen_11.005_49.595&uk=Bundesweit&bg=false&page=0",
     "infosysbub-wbsuche"),
    ("bundesAPI-Doku v1",
     "https://rest.arbeitsagentur.de/infosysbub/wbsuche/pc/v1/bildungsangebot"
     "?orte=Erlangen_11.005_49.595&uk=Bundesweit&bg=false&page=0",
     "infosysbub-wbsuche"),
    ("Kontrolle: Jobsuche-API der BA (anderer Dienst, gleicher Host)",
     "https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/jobs"
     "?was=Koch&size=1",
     "jobboerse-jobsuche"),
    ("NOW-Frontend produktiv (aus window.sucheConfig.backendHost)",
     "https://rest.mein-now.de/now-prod/suche/pc/v1/bildungsangebot"
     "?sw=Umschulung&ortsunabhaengig=true&page=0&size=1",
     "infosysbub-nowsuche"),
    ("NOW-Frontend produktiv, OHNE API-Key",
     "https://rest.mein-now.de/now-prod/suche/pc/v1/bildungsangebot"
     "?sw=Umschulung&ortsunabhaengig=true&page=0&size=1",
     None),
    ("NOW Facetten-Aggregation",
     "https://rest.mein-now.de/now-prod/suche/pc/v1/facettenaggregations"
     "?sw=Umschulung&ortsunabhaengig=true",
     "infosysbub-nowsuche"),
]


def probe(url, api_key):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json",
               "Referer": "https://mein-now.de/"}
    if api_key:
        headers["X-API-Key"] = api_key
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            body = r.read(4000).decode("utf-8", "replace")
            return {"http_status": r.status, "body_prefix": body[:400]}
    except urllib.error.HTTPError as e:
        body = e.read(2000).decode("utf-8", "replace")
        return {"http_status": e.code, "body_prefix": body[:400]}
    except Exception as e:                                    # noqa: BLE001
        return {"http_status": None, "error": repr(e)}


def main():
    ergebnisse = []
    for label, url, key in KANDIDATEN:
        res = probe(url, key)
        res.update({"label": label, "url": url, "api_key": key})
        ergebnisse.append(res)
        print(f"{res['http_status']}  {label}")
        time.sleep(RATE_LIMIT_SECONDS)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"erhoben_am": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                               time.gmtime()),
                   "ergebnisse": ergebnisse}, f, ensure_ascii=False, indent=2)
    print(f"\ngeschrieben: {OUT}")


if __name__ == "__main__":
    main()
