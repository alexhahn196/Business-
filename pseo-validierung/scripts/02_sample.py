#!/usr/bin/env python3
"""
AP1 + AP2 - Stichprobenerhebung aus der NOW-Weiterbildungssuche (Fassung 2).

Drei Erhebungen:

  A) FACETTEN-GRID  -> data/grid_facetten.jsonl
     Je Kombination Beruf x Ort ein Request an /pc/v1/facettenaggregations.
     Liefert Aggregate (Anzahl Angebote, Foerderart, Dauer, Lernform, Kosten)
     OHNE Einzeldatensaetze. Grundlage der AP2-Verteilung.

  B) UEBERSCHNEIDUNG -> data/ueberlappung.jsonl
     Fuer ausgewaehlte Berufe mit kleiner Treffermenge werden die Angebots-IDs
     je Stadt VOLLSTAENDIG paginiert. Damit laesst sich exakt messen, wie stark
     sich die Angebotslisten zweier Staedte ueberschneiden.

  C) BUNDESWEITE REICHWEITE -> data/reichweite.jsonl
     Je Beruf die ersten Seiten ohne Ortsfilter, um die Verteilung von
     anzahlTermine (wie viele Termine hat ein Angebot bundesweit?) zu messen.

Rate-Limit 1 Request/Sekunde, sauberer User-Agent, kein Vollabzug,
harte Obergrenze MAX_RECORDS Datensaetze.

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
from config import (BACKEND_HOST, BERUFE, BERUFE_UEBERLAPPUNG, HEADERS,
                    ORT_INDEX, ORTE, ORTE_UEBERLAPPUNG, PAGE_SIZE,
                    RATE_LIMIT_SECONDS, UMKREIS_KM, ort_param)

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

MAX_RECORDS = 2000
MAX_PAGES_UEBERLAPPUNG = 10     # 10 * 20 = max. 200 Angebote je Kombination
REICHWEITE_SEITEN = 2           # je Beruf 2 Seiten a 20 = 40 Angebote

_records = 0


def get(pfad, params):
    url = f"{BACKEND_HOST}{pfad}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode("utf-8")), r.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception as e:                                    # noqa: BLE001
        return None, f"ERR:{e!r}"


def ortparams(ortname):
    name, lon, lat, *_ = ORT_INDEX[ortname]
    return {"ort": ort_param(name, lon, lat), "uk": UMKREIS_KM}


# ---------------------------------------------------------------------------
def lauf_grid():
    out = os.path.join(DATA, "grid_facetten.jsonl")
    gesamt = len(BERUFE) * len(ORTE)
    n = 0
    with open(out, "w", encoding="utf-8") as f:
        for name, lon, lat, klasse, bl, ew in ORTE:
            p_ort = {"ort": ort_param(name, lon, lat), "uk": UMKREIS_KM}
            for beruf in BERUFE:
                d, status = get("/pc/v1/facettenaggregations",
                                {"sw": beruf, **p_ort})
                n += 1
                z = {"beruf": beruf, "ort": name, "klasse": klasse,
                     "bundesland": bl, "einwohner": ew,
                     "umkreis_km": UMKREIS_KM, "http_status": status}
                if isinstance(d, dict):
                    z["anzahl_angebote"] = d.get(
                        "ANZAHL_ANGEBOTE_GESAMT", {}).get("COUNT")
                    for k in ("FOERDERART", "DAUER", "LERNFORMEN",
                              "WEITERBILDUNGSART", "KOSTEN", "UNTERRICHTSZEIT",
                              "REGIONEN"):
                        z[k.lower()] = d.get(k)
                f.write(json.dumps(z, ensure_ascii=False) + "\n")
                f.flush()
                if n % 40 == 0:
                    print(f"  grid {n}/{gesamt}", flush=True)
                time.sleep(RATE_LIMIT_SECONDS)
    print(f"A) Grid fertig: {n} Requests -> {out}", flush=True)


# ---------------------------------------------------------------------------
def lauf_ueberlappung():
    """Vollstaendige Angebots-ID-Listen je (Beruf, Ort)."""
    global _records
    out = os.path.join(DATA, "ueberlappung.jsonl")
    with open(out, "w", encoding="utf-8") as f:
        for beruf in BERUFE_UEBERLAPPUNG:
            for ortname in ORTE_UEBERLAPPUNG:
                p_ort = ortparams(ortname)
                seite, total, angebote, vollstaendig = 0, None, [], True
                while seite < MAX_PAGES_UEBERLAPPUNG:
                    if _records >= MAX_RECORDS:
                        print("MAX_RECORDS erreicht.", flush=True)
                        vollstaendig = False
                        break
                    d, status = get("/pc/v1/bildungsangebot",
                                    {"sw": beruf, **p_ort,
                                     "page": seite, "size": PAGE_SIZE})
                    time.sleep(RATE_LIMIT_SECONDS)
                    if not isinstance(d, dict):
                        vollstaendig = False
                        break
                    total = d.get("page", {}).get("totalElements")
                    items = d.get("_embedded", {}).get(
                        "bildungsangebotDTOList", []) or []
                    for a in items:
                        angebote.append({
                            "id": a.get("id"),
                            "titel": a.get("titel"),
                            "inhalt": a.get("inhalt"),
                            "anzahlTermine": a.get("anzahlTermine"),
                            "weiterbildungsart": a.get("weiterbildungsart"),
                            "traeger": (a.get("bildungsanbieter") or {}).get("name"),
                            "traeger_ort": ((a.get("bildungsanbieter") or {})
                                            .get("adresse") or {}).get("ort"),
                            "termin_orte": sorted({
                                (t.get("adresse") or {}).get("ort")
                                for t in (a.get("termine") or [])} - {None}),
                            "unterrichtsformen": sorted({
                                (t.get("unterrichtsform") or {}).get("bezeichnung")
                                for t in (a.get("termine") or [])} - {None}),
                        })
                        _records += 1
                    seite += 1
                    if total is None or seite * PAGE_SIZE >= total:
                        break
                else:
                    vollstaendig = False
                f.write(json.dumps(
                    {"beruf": beruf, "ort": ortname,
                     "klasse": ORT_INDEX[ortname][3],
                     "total_elements": total, "seiten_geholt": seite,
                     "vollstaendig": vollstaendig,
                     "angebote": angebote}, ensure_ascii=False) + "\n")
                f.flush()
                print(f"  ueberlappung {beruf}/{ortname}: "
                      f"{len(angebote)}/{total} vollst={vollstaendig} "
                      f"(kum. {_records})", flush=True)
    print(f"B) Ueberlappung fertig -> {out}", flush=True)


# ---------------------------------------------------------------------------
def lauf_reichweite():
    """Verteilung von anzahlTermine je Beruf, ohne Ortsfilter."""
    global _records
    out = os.path.join(DATA, "reichweite.jsonl")
    with open(out, "w", encoding="utf-8") as f:
        for beruf in BERUFE:
            total = None
            for seite in range(REICHWEITE_SEITEN):
                if _records >= MAX_RECORDS:
                    print("MAX_RECORDS erreicht.", flush=True)
                    return
                d, status = get("/pc/v1/bildungsangebot",
                                {"sw": beruf, "page": seite,
                                 "size": PAGE_SIZE})
                time.sleep(RATE_LIMIT_SECONDS)
                if not isinstance(d, dict):
                    break
                total = d.get("page", {}).get("totalElements")
                for a in (d.get("_embedded", {})
                          .get("bildungsangebotDTOList", []) or []):
                    f.write(json.dumps({
                        "beruf": beruf, "total_bundesweit": total,
                        "removedToken": d.get("removedToken"),
                        "korrekturVorschlag": d.get("korrekturVorschlag"),
                        "id": a.get("id"), "titel": a.get("titel"),
                        "anzahlTermine": a.get("anzahlTermine"),
                        "traeger": (a.get("bildungsanbieter") or {}).get("name"),
                        "traeger_ort": ((a.get("bildungsanbieter") or {})
                                        .get("adresse") or {}).get("ort"),
                        "termin_orte_stichprobe": sorted({
                            (t.get("adresse") or {}).get("ort")
                            for t in (a.get("termine") or [])} - {None}),
                        "inhalt_laenge": len(a.get("inhalt") or ""),
                        "felder_vorhanden": sorted(a.keys()),
                        "termin_felder": sorted(
                            (a.get("termine") or [{}])[0].keys())
                            if a.get("termine") else [],
                    }, ensure_ascii=False) + "\n")
                    _records += 1
                f.flush()
            print(f"  reichweite {beruf}: total={total} (kum. {_records})",
                  flush=True)
    print(f"C) Reichweite fertig -> {out}", flush=True)


def main():
    os.makedirs(DATA, exist_ok=True)
    print(f"Start {time.strftime('%H:%M:%S')} | {len(BERUFE)} Berufe x "
          f"{len(ORTE)} Orte, Umkreis {UMKREIS_KM} km", flush=True)
    lauf_reichweite()
    lauf_ueberlappung()
    lauf_grid()
    print(f"Ende {time.strftime('%H:%M:%S')} | Datensaetze gesamt: {_records}",
          flush=True)


if __name__ == "__main__":
    main()
