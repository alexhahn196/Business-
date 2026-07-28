"""
Gemeinsame Konfiguration fuer die Marktvalidierung.

Datenquelle: Weiterbildungssuche der Bundesagentur fuer Arbeit / NOW-Portal.
Endpunkt ermittelt am 2026-07-28 aus dem Frontend-Bundle von
https://mein-now.de/weiterbildungssuche/ (window.sucheConfig.backendHost).

WICHTIG: Der in github.com/bundesAPI/weiterbildungssuche-api dokumentierte
Endpunkt rest.arbeitsagentur.de/infosysbub/wbsuche/pc/v2/bildungsangebot
liefert seit (mindestens) 2026-07-28 HTTP 404. Siehe data/ap1_endpoint_probe.json.
"""

BACKEND_HOST = "https://rest.mein-now.de/now-prod/suche"
API_KEY = "infosysbub-nowsuche"   # aus window.oiamConfig.clientId des Frontends
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36 "
    "(Marktvalidierung Weiterbildungsportal; Stichprobe, 1 req/s)"
)
RATE_LIMIT_SECONDS = 1.0

HEADERS = {
    "X-API-Key": API_KEY,
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Referer": "https://mein-now.de/",
}

# ---------------------------------------------------------------------------
# Achse "Ort"
# Format des ort-Parameters: <Name>_<lon>_<lat>  (vom Frontend so gebaut)
# Koordinaten gerundet auf 3 Nachkommastellen, Quelle: OpenStreetMap/Wikipedia
# Stadtgroessen-Klassen nach amtlicher Definition:
#   GROSS  = Grossstadt   (>= 100.000 Einwohner)
#   MITTEL = Mittelstadt  (20.000 - 100.000)
#   KLEIN  = Kleinstadt   (5.000 - 20.000)
# ---------------------------------------------------------------------------
ORTE = [
    # (Name, lon, lat, Klasse, Bundesland, Einwohner_ca)
    ("Berlin",              13.405, 52.520, "GROSS",  "BE", 3_850_000),
    ("Hamburg",              9.993, 53.551, "GROSS",  "HH", 1_910_000),
    ("Muenchen",            11.582, 48.135, "GROSS",  "BY", 1_510_000),
    ("Koeln",                6.960, 50.937, "GROSS",  "NW", 1_090_000),
    ("Frankfurt am Main",    8.682, 50.111, "GROSS",  "HE",   775_000),
    ("Stuttgart",            9.183, 48.776, "GROSS",  "BW",   635_000),
    ("Leipzig",             12.374, 51.340, "GROSS",  "SN",   620_000),
    ("Dortmund",             7.466, 51.514, "GROSS",  "NW",   590_000),
    ("Essen",                7.013, 51.456, "GROSS",  "NW",   580_000),
    ("Bochum",               7.216, 51.482, "GROSS",  "NW",   365_000),
    ("Nuernberg",           11.078, 49.452, "GROSS",  "BY",   530_000),
    ("Fuerth",              10.990, 49.478, "GROSS",  "BY",   130_000),
    ("Rostock",             12.141, 54.092, "GROSS",  "MV",   210_000),
    ("Kassel",               9.480, 51.312, "GROSS",  "HE",   205_000),

    ("Bottrop",              6.923, 51.523, "MITTEL", "NW",   117_000),
    ("Siegen",               8.024, 50.875, "MITTEL", "NW",   103_000),
    ("Jena",                11.586, 50.927, "MITTEL", "TH",   111_000),
    ("Gera",                12.083, 50.881, "MITTEL", "TH",    92_000),
    ("Landshut",            12.151, 48.537, "MITTEL", "BY",    73_000),
    ("Bamberg",             10.888, 49.891, "MITTEL", "BY",    77_000),
    ("Zwickau",             12.496, 50.718, "MITTEL", "SN",    87_000),
    ("Stralsund",           13.078, 54.309, "MITTEL", "MV",    59_000),
    ("Emden",                7.206, 53.359, "MITTEL", "NI",    50_000),
    ("Pirmasens",            7.601, 49.201, "MITTEL", "RP",    40_000),

    ("Nordhorn",             7.070, 52.431, "KLEIN",  "NI",    54_000),
    ("Coesfeld",             7.170, 51.945, "KLEIN",  "NW",    37_000),
    ("Cuxhaven",             8.694, 53.859, "KLEIN",  "NI",    48_000),
    ("Weiden in der Oberpfalz", 12.157, 49.677, "KLEIN", "BY", 43_000),
    ("Prenzlau",            13.863, 53.316, "KLEIN",  "BB",    19_000),
    ("Zeitz",               12.136, 51.049, "KLEIN",  "ST",    27_000),
]

# ---------------------------------------------------------------------------
# Achse "Beruf"
# Auswahl: die in Deutschland gaengigsten Umschulungs-/Weiterbildungsziele.
# Bewusst breit gestreut (kaufmaennisch, IT, Pflege, Technik, Logistik),
# damit die Verteilung nicht durch eine einzelne Branche verzerrt wird.
# ---------------------------------------------------------------------------
BERUFE = [
    "Kaufmann fuer Bueromanagement",
    "Fachinformatiker",
    "Pflegefachkraft",
    "Erzieher",
    "Berufskraftfahrer",
    "Elektroniker",
    "Finanzbuchhaltung",
    "Fachkraft fuer Lagerlogistik",
    "Mechatroniker",
    "Steuerfachangestellte",
    "Kaufmann im Einzelhandel",
    "Immobilienkaufmann",
    "Sozialassistent",
    "Anlagenmechaniker Sanitaer Heizung Klima",
    "Webentwickler",
    "Mediengestalter",
]

# Nachbarstadt-Paare im selben Bundesland fuer die Duplikats-Simulation (AP2)
NACHBARPAARE = [
    ("Dortmund", "Bochum"),      # NRW, ca. 20 km
    ("Nuernberg", "Fuerth"),     # BY, ca. 7 km
    ("Essen", "Bochum"),         # NRW, ca. 15 km
]


def ort_param(name, lon, lat):
    """Baut den ort-Parameter im Format des NOW-Frontends."""
    return f"{name}_{lon}_{lat}"
