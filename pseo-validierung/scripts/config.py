"""
Gemeinsame Konfiguration fuer die Marktvalidierung (Fassung 2).

Datenquelle: Weiterbildungssuche der Bundesagentur fuer Arbeit / NOW-Portal.
Endpunkt am 2026-07-28 aus dem Frontend-Bundle von
https://mein-now.de/weiterbildungssuche/ ermittelt (window.sucheConfig.backendHost).

Der in github.com/bundesAPI/weiterbildungssuche-api dokumentierte Endpunkt
rest.arbeitsagentur.de/infosysbub/wbsuche/pc/v2/bildungsangebot liefert
HTTP 404. Beleg: data/ap1_endpoint_probe.json


WARUM FASSUNG 2 - drei Messfehler aus Fassung 1, alle empirisch nachgewiesen:

1. uk=ort ("ganzer Ort") macht einen EXAKTEN Namensabgleich gegen den in den
   Daten hinterlegten Terminort. Staedte, die dort disambiguiert gespeichert
   sind, liefern faelschlich 0 Treffer.
   Beleg: ort=Kassel_9.472_51.312&uk=ort  -> 0 Angebote
          ort=Kassel_9.472_51.312&uk=5    -> 317 Angebote, Terminort
                                             laut Antwort "Kassel, Hessen"
   Betroffen in Fassung 1: Essen, Kassel, Landshut, Nuernberg, Fuerth.
   -> Fassung 2 nutzt durchgehend Umkreissuche uk=5 (5 km). Der Ortsname ist
      dabei nur Label, die Koordinaten steuern die Suche.

2. Umlaute im Ortsnamen wurden transliteriert ("Muenchen" statt "Muenchen").
   Beleg: ort=Muenchen_11.582_48.135 -> 0 ; ort=M<uu>nchen_11.582_48.135 -> 377
   -> Fassung 2 nutzt die korrekte Schreibweise.

3. Mehrwortige Suchbegriffe werden vom Backend STILL umgeschrieben. Das Feld
   removedToken der Antwort weist aus, welches Token entfernt wurde.
   Beleg: sw="Anlagenmechaniker Sanitaer Heizung Klima" -> total=5,
          removedToken="Anlagenmechaniker" (der eigentliche Beruf floss also
          gar nicht in die Suche ein)
          sw="Anlagenmechaniker" -> total=1
   -> Fassung 2 nutzt ausschliesslich EINWORT-Suchbegriffe und protokolliert
      removedToken/korrekturVorschlag je Request mit.

Weitere gemessene Randbedingung: size > 20 liefert HTTP 400.
"""

BACKEND_HOST = "https://rest.mein-now.de/now-prod/suche"
API_KEY = "infosysbub-nowsuche"   # aus window.oiamConfig.clientId des Frontends
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36 "
    "(Marktvalidierung Weiterbildungsportal; Stichprobe, 1 req/s)"
)
RATE_LIMIT_SECONDS = 1.0
PAGE_SIZE = 20            # gemessenes Maximum (ab 24 -> HTTP 400)
UMKREIS_KM = "5"          # Stadt-Proxy

HEADERS = {
    "X-API-Key": API_KEY,
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Referer": "https://mein-now.de/",
}

# ---------------------------------------------------------------------------
# Achse "Ort"  -  Format: <Name>_<lon>_<lat>
# Koordinaten: OpenStreetMap/Wikipedia, 3 Nachkommastellen.
# Klassen: GROSS >=100.000 EW, MITTEL 20.000-100.000, KLEIN 5.000-20.000
# ---------------------------------------------------------------------------
ORTE = [
    ("Berlin",            13.405, 52.520, "GROSS",  "BE", 3_850_000),
    ("Hamburg",            9.993, 53.551, "GROSS",  "HH", 1_910_000),
    ("München",           11.582, 48.135, "GROSS",  "BY", 1_510_000),
    ("Köln",               6.960, 50.937, "GROSS",  "NW", 1_090_000),
    ("Frankfurt am Main",  8.682, 50.111, "GROSS",  "HE",   775_000),
    ("Stuttgart",          9.183, 48.776, "GROSS",  "BW",   635_000),
    ("Leipzig",           12.374, 51.340, "GROSS",  "SN",   620_000),
    ("Dortmund",           7.466, 51.514, "GROSS",  "NW",   590_000),
    ("Essen",              7.012, 51.456, "GROSS",  "NW",   580_000),
    ("Bochum",             7.216, 51.482, "GROSS",  "NW",   365_000),
    ("Nürnberg",          11.078, 49.452, "GROSS",  "BY",   530_000),
    ("Kassel",             9.472, 51.312, "GROSS",  "HE",   205_000),

    ("Bottrop",            6.923, 51.523, "MITTEL", "NW",   117_000),
    ("Siegen",             8.024, 50.875, "MITTEL", "NW",   103_000),
    ("Jena",              11.586, 50.927, "MITTEL", "TH",   111_000),
    ("Gera",              12.083, 50.881, "MITTEL", "TH",    92_000),
    ("Landshut",          12.151, 48.537, "MITTEL", "BY",    73_000),
    ("Zwickau",           12.496, 50.718, "MITTEL", "SN",    87_000),
    ("Stralsund",         13.078, 54.309, "MITTEL", "MV",    59_000),
    ("Pirmasens",          7.601, 49.201, "MITTEL", "RP",    40_000),

    ("Nordhorn",           7.070, 52.431, "KLEIN",  "NI",    54_000),
    ("Coesfeld",           7.170, 51.945, "KLEIN",  "NW",    37_000),
    ("Prenzlau",          13.863, 53.316, "KLEIN",  "BB",    19_000),
    ("Zeitz",             12.136, 51.049, "KLEIN",  "ST",    27_000),
]

# ---------------------------------------------------------------------------
# Achse "Beruf"  -  ausschliesslich EINWORT-Begriffe (siehe Messfehler 3)
# ---------------------------------------------------------------------------
BERUFE = [
    "Fachinformatiker",
    "Büromanagement",
    "Pflegefachkraft",
    "Erzieher",
    "Berufskraftfahrer",
    "Elektroniker",
    "Finanzbuchhaltung",
    "Lagerlogistik",
    "Mechatroniker",
    "Steuerfachangestellte",
    "Einzelhandel",
    "Immobilienkaufmann",
    "Sozialassistent",
    "Anlagenmechaniker",
    "Webentwickler",
    "Mediengestalter",
]

# Berufe mit kleiner Treffermenge -> vollstaendige Paginierung moeglich,
# dadurch exakte Ueberschneidungsmessung auf Angebots-ID-Ebene.
BERUFE_UEBERLAPPUNG = [
    "Steuerfachangestellte",
    "Immobilienkaufmann",
    "Lagerlogistik",
    "Einzelhandel",
]

# Staedte fuer die Ueberschneidungsmessung:
# zwei Nachbarpaare plus zwei weit entfernte Kontrollstaedte.
ORTE_UEBERLAPPUNG = ["Dortmund", "Bochum", "Nürnberg", "Leipzig",
                     "Hamburg", "Stralsund"]

NACHBARPAARE = [
    ("Dortmund", "Bochum"),   # NRW, ca. 20 km
    ("Essen", "Bochum"),      # NRW, ca. 15 km
]
# Kontrollpaare: weit auseinander, verschiedene Bundeslaender
FERNPAARE = [
    ("Hamburg", "Nürnberg"),
    ("Leipzig", "Dortmund"),
    ("Stralsund", "Nürnberg"),
]


def ort_param(name, lon, lat):
    return f"{name}_{lon}_{lat}"


ORT_INDEX = {o[0]: o for o in ORTE}
