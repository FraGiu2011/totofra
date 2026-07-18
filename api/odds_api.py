import requests
import os

# Inserisci qui la tua API KEY OddsAPI
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "4b477169b3d04f57a3d33a78e5256f51")

BASE_URL = "https://api.the-odds-api.com/v4/sports/soccer_italy_serie_a/odds"


def get_odds_for_match_SA(home, away):
    """
    Restituisce le quote 1X2 per un match di Serie A.
    Ritorna un dict: {"1": quota1, "X": quotaX, "2": quota2}
    oppure None se non trovate.
    """

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        for match in data:
            h = match["home_team"].lower()
            a = match["away_team"].lower()

            if home.lower() in h and away.lower() in a:
                # Prendiamo il bookmaker Bet365 se disponibile
                for book in match["bookmakers"]:
                    if book["key"] == "bet365":
                        outcomes = book["markets"][0]["outcomes"]

                        odds_dict = {
                            "1": outcomes[0]["price"],
                            "X": outcomes[1]["price"],
                            "2": outcomes[2]["price"]
                        }
                        return odds_dict

        return None

    except Exception as e:
        print(f"Errore OddsAPI: {e}")
        return None
