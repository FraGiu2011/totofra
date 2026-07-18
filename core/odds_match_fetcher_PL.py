# core/odds_match_fetcher_PL.py

import os
import requests

class OddsMatchFetcherPL:
    def __init__(self):
        self.api_key = os.getenv("odds_api_key") or "3746648243eb75f8f0087e96ec4684d3"
        print("[DEBUG] API KEY letta da ambiente:", self.api_key)
        self.base_url = "https://api.the-odds-api.com/v4/sports"

    def get_matches(self):
        url = f"{self.base_url}/soccer_italy_serie_a/odds"
        params = {
            "apiKey": self.api_key,
            "regions": "uk,eu,us",
            "markets": "h2h",
            "oddsFormat": "decimal"
        }

        print("[DEBUG] URL:", url)
        print("[DEBUG] Params:", params)

        r = requests.get(url, params=params)
        print("[DEBUG] Status:", r.status_code)
        print("[DEBUG] Raw text:", r.text[:500])

        return r.json()

    def parse_matches(self, odds_json):
        matches = []

        for m in odds_json:
            home = m["home_team"]
            away = m["away_team"]

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
