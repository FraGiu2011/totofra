from api.api_client import get_matches


def fetch_matchday(competition_id, matchday):
    """
    Restituisce una lista di match normalizzati per il resto del sistema.
    Versione ESTESA: include squadre, ID, gol, odds, stato, data, matchday, stagione.
    """
    data = get_matches(competition_id, matchday)
    matches = data.get("matches", [])

    normalized = []
    for m in matches:

        # Estraggo blocchi per sicurezza
        score = m.get("score", {})
        full_time = score.get("fullTime", {})
        half_time = score.get("halfTime", {})
        odds = m.get("odds", {})

        normalized.append({
            # Squadre
            "home": m["homeTeam"]["name"],
            "away": m["awayTeam"]["name"],

            # ID squadre
            "home_id": m["homeTeam"].get("id"),
            "away_id": m["awayTeam"].get("id"),

            # Data e stato
            "utcDate": m.get("utcDate"),
            "status": m.get("status"),

            # Gol finali
            "fullTime_home": full_time.get("home"),
            "fullTime_away": full_time.get("away"),

            # Gol primo tempo
            "halfTime_home": half_time.get("home"),
            "halfTime_away": half_time.get("away"),

            # Odds (se disponibili)
            "odds_home": odds.get("homeWin"),
            "odds_draw": odds.get("draw"),
            "odds_away": odds.get("awayWin"),

            # Matchday e stagione
            "matchday": m.get("matchday"),
            "season_start": m.get("season", {}).get("startDate"),
            "season_end": m.get("season", {}).get("endDate"),

            # Extra utili per modelli futuri
            "referees": m.get("referees", []),
            "venue": m.get("venue"),
            "lastUpdated": m.get("lastUpdated"),
        })

    return normalized
