#!/usr/bin/env python3
"""
AP1 + AP2 - Stichprobenerhebung aus der NOW-Weiterbildungssuche.

Zwei Erhebungen:

  A) FACETTEN-GRID (Grundlage AP2)
     Fuer jede Kombination Beruf x Ort ein Request an /pc/v1/facettenaggregations.
     Liefert Aggregatzahlen (Anzahl Angebote, Foerderarten, Dauer, Lernform,
     Kosten) OHNE Einzeldatensaetze zu ziehen. -> data/grid_facetten.jsonl

  B) DATENSATZ-STICHPROBE (Grundlage AP1-Feldstruktur + AP2-Duplikatsanalyse)
     Fuer eine Teilmenge echte Angebotsdatensaetze inkl. Traegernamen.
     Hartes Limit: MAX_RECORDS Datensaetze. -> data/records.jsonl

Rate-Limit: 1 Request/Sekunde. Sauberer, identifizierbarer User-Agent.
Kein Vollabzug.

Aufruf: python3 scripts/02_sample.py
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (BACKEND_HOST, BERUFE, HEADERS, NACHBARPAARE, ORTE,
                    RATE_LIMIT_SECONDS, ort_param)

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

MAX_RECORDS = 2000        # harte Obergrenze laut Auftrag
PAGE_SIZE = 25            # Datensaetze pro Detail-Request

# Staedte fuer die Datensatz-Stichprobe: alle Nachbarpaar-Staedte plus
# je zwei Mittel-/Kleinstaedte als Kontrast.
DETAIL_ORTE = sorted({s for paar in NACHBARPAARE for s in paar} |
                     {"Bottrop", "Jena", "Nordhorn", "Prenzlau"})
DETAIL_BERUFE = BERUFE[:8]

_records_gezogen = 0


def get(pfad, params):
    url = f"{BACKEND_HOST}{pfad}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode("utf-8")), r.status, url
    except urllib.error.HTTPError as e:
        return None, e.code, url
    except Exception as e:                                    # noqa: BLE001
        return None, f"ERR:{e!r}", url


def facetten(beruf, ort_p):
    return get("/pc/v1/facettenaggregations",
               {"sw": beruf, "ort": ort_p, "uk": "ort"})


def angebote(beruf, ort_p, size=PAGE_SIZE, page=0):
    return get("/pc/v1/bildungsangebot",
               {"sw": beruf, "ort": ort_p, "uk": "ort",
                "page": page, "size": size})


def lauf_grid():
    """A) Facetten-Grid Beruf x Ort."""
    out = os.path.join(DATA, "grid_facetten.jsonl")
    gesamt = len(BERUFE) * len(ORTE)
    n = 0
    with open(out, "w", encoding="utf-8") as f:
        for name, lon, lat, klasse, bl, ew in ORTE:
            op = ort_param(name, lon, lat)
            for beruf in BERUFE:
                d, status, url = facetten(beruf, op)
                n += 1
                zeile = {
                    "beruf": beruf, "ort": name, "klasse": klasse,
                    "bundesland": bl, "einwohner": ew,
                    "ort_param": op, "http_status": status, "url": url,
                }
                if isinstance(d, dict):
                    zeile["anzahl_angebote"] = (
                        d.get("ANZAHL_ANGEBOTE_GESAMT", {}).get("COUNT"))
                    zeile["foerderart"] = d.get("FOERDERART")
                    zeile["dauer"] = d.get("DAUER")
                    zeile["lernformen"] = d.get("LERNFORMEN")
                    zeile["weiterbildungsart"] = d.get("WEITERBILDUNGSART")
                    zeile["kosten"] = d.get("KOSTEN")
                    zeile["unterrichtszeit"] = d.get("UNTERRICHTSZEIT")
                f.write(json.dumps(zeile, ensure_ascii=False) + "\n")
                f.flush()
                if n % 25 == 0:
                    print(f"  grid {n}/{gesamt}", flush=True)
                time.sleep(RATE_LIMIT_SECONDS)
    print(f"Grid fertig: {n} Requests -> {out}", flush=True)


def lauf_records():
    """B) Datensatz-Stichprobe, hart gedeckelt auf MAX_RECORDS."""
    global _records_gezogen
    out = os.path.join(DATA, "records.jsonl")
    ortmap = {o[0]: o for o in ORTE}
    n_req = 0
    with open(out, "w", encoding="utf-8") as f:
        for ortname in DETAIL_ORTE:
            if ortname not in ortmap:
                continue
            name, lon, lat, klasse, bl, ew = ortmap[ortname]
            op = ort_param(name, lon, lat)
            for beruf in DETAIL_BERUFE:
                if _records_gezogen >= MAX_RECORDS:
                    print("MAX_RECORDS erreicht - Abbruch der Stichprobe.",
                          flush=True)
                    return
                d, status, url = angebote(beruf, op)
                n_req += 1
                items = []
                total = None
                if isinstance(d, dict):
                    items = d.get("_embedded", {}).get(
                        "bildungsangebotDTOList", []) or []
                    total = d.get("page", {}).get("totalElements")
                for it in items:
                    if _records_gezogen >= MAX_RECORDS:
                        break
                    f.write(json.dumps(
                        {"beruf": beruf, "ort": name, "klasse": klasse,
                         "bundesland": bl, "total_elements": total,
                         "http_status": status, "angebot": it},
                        ensure_ascii=False) + "\n")
                    _records_gezogen += 1
                f.flush()
                print(f"  records {ortname}/{beruf}: +{len(items)} "
                      f"(kumuliert {_records_gezogen})", flush=True)
                time.sleep(RATE_LIMIT_SECONDS)
    print(f"Records fertig: {n_req} Requests, {_records_gezogen} Datensaetze "
          f"-> {out}", flush=True)


def main():
    os.makedirs(DATA, exist_ok=True)
    print(f"Start {time.strftime('%H:%M:%S')} | "
          f"{len(BERUFE)} Berufe x {len(ORTE)} Orte", flush=True)
    lauf_grid()
    lauf_records()
    print(f"Ende {time.strftime('%H:%M:%S')}", flush=True)


if __name__ == "__main__":
    main()
