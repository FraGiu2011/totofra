import requests
import pandas as pd
from worldcup.worldcup_calendar_2026 import CALENDAR_2026

API_KEY = None  # Se vuoi usare API-Football, inserisci qui la tua key

# ============================================================
# FETCH MATCHES (API FOOTBALL)
# ============================================================

def fetch_worldcup_matches():
    if API_KEY is None:
        return []

    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "league": 1,      # FIFA World Cup
        "season": 2026
    }
    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if "response" not in data:
            return []

        matches = data["response"]
        return matches

    except Exception:
        return []


# ============================================================
# FILTER MATCHES BY STAGE
# ============================================================

def filter_stage(matches, stage_name):
    rows = []

    for m in matches:
        if m["league"]["round"] != stage_name:
            continue

        rows.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "date": m["fixture"]["date"],
            "status": m["fixture"]["status"]["short"],
            "goals_home": m["goals"]["home"],
            "goals_away": m["goals"]["away"],
            "odds_home": None,
            "odds_draw": None,
            "odds_away": None,
            "logo_home": m["teams"]["home"]["logo"],
            "logo_away": m["teams"]["away"]["logo"]
        })

    return pd.DataFrame(rows)


# ============================================================
# MAIN LOADER — VERSIONE COMPLETA CON OTTAVI
# ============================================================

def load_phasefinals_real():
    matches = fetch_worldcup_matches()

    # ========================================================
    # CASO 1 — API NON HA DATI (Mondiale futuro)
    # → Usa calendario 2026 completo
    # ========================================================
    if len(matches) == 0:
        return {
            "round_of_16": pd.DataFrame(CALENDAR_2026["round_of_16"]),
            "quarters": pd.DataFrame(CALENDAR_2026["quarters"]),
            "semifinals": pd.DataFrame(CALENDAR_2026["semifinals"]),
            "final": pd.DataFrame(CALENDAR_2026["final"])
        }

    # ========================================================
    # CASO 2 — API HA DATI REALI (Mondiale passato)
    # ========================================================

    quarters = filter_stage(matches, "Quarter-finals")
    semis = filter_stage(matches, "Semi-finals")
    final = filter_stage(matches, "Final")

    # Gli ottavi NON esistono nei dati API-Football del Mondiale
    return {
        "round_of_16": pd.DataFrame([]),
        "quarters": quarters,
        "semifinals": semis,
        "final": final
    }
