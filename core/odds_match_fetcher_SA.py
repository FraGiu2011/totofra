# core/odds_match_fetcher_SA.py

import os
import requests

class OddsMatchFetcherSA:
    def __init__(self):
        self.api_key = os.getenv("odds_api_key")
        self.base_url = "https://api.the-odds-api.com/v4/sports"

        # Squadre Serie A (nomi OddsAPI)
        self.serie_a_teams = {
            "Inter Milan", "AC Milan", "AS Roma", "SS Lazio",
            "Atalanta BC", "Napoli", "Juventus", "Fiorentina",
            "Bologna", "Torino FC", "Genoa CFC", "US Lecce",
            "Udinese Calcio", "Cagliari Calcio", "Hellas Verona",
            "Frosinone Calcio", "US Sassuolo Calcio", "Empoli FC",
            "US Salernitana 1919", "AC Monza"
        }

    def get_matches(self):
        url = f"{self.base_url}/soccer_italy_serie_a/odds"
        params = {
            "apiKey": self.api_key,
            "regions": "eu",
            "markets": "h2h",
            "oddsFormat": "decimal"
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()

    def parse_matches(self, odds_json):
        matches = []

        for m in odds_json:
            home = m["home_team"]
            away = m["away_team"]

            if home not in self.serie_a_teams or away not in self.serie_a_teams:
                continue

            odds = {"1": None, "X": None, "2": None}

            for bookmaker in m["bookmakers"]:
                if bookmaker["key"] != "bet365":
                    continue

                for market in bookmaker["markets"]:
                    if market["key"] == "h2h":
                        for o in market["outcomes"]:
                            if o["name"] == home:
                                odds["1"] = o["price"]
                            elif o["name"] == away:
                                odds["2"] = o["price"]
                            elif o["name"] == "Draw":
                                odds["X"] = o["price"]

            matches.append({
                "home": home,
                "away": away,
                "utcDate": m["commence_time"],
                "odds": odds
            })

        return matches
