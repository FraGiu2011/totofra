import os
import requests

class OddsFetcher:
    def __init__(self):
        self.api_key = os.getenv("odds_api_key")
        self.base_url = "https://api.the-odds-api.com/v4/sports"

    def get_odds(self, sport_key="soccer_epl", regions="eu", markets="h2h,totals"):
        """
        sport_key:
            - soccer_epl → Premier League
            - soccer_ita_seria → Serie A
        regions:
            eu → include Bet365
        markets:
            h2h → 1X2
            totals → Over/Under
            btts → GG/NG
        """

        url = f"{self.base_url}/{sport_key}/odds"
        params = {
            "apiKey": self.api_key,
            "regions": regions,
            "markets": markets,
            "oddsFormat": "decimal"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def extract_bet365(self, odds_json):
        """
        Estrae SOLO le quote Bet365 per ogni match.
        Restituisce un dict:
        {
            "home - away": {
                "1": quota,
                "X": quota,
                "2": quota,
                "over25": quota,
                "under25": quota,
                "gg": quota,
                "ng": quota
            }
        }
        """

        out = {}

        for match in odds_json:
            home = match["home_team"]
            away = match["away_team"]
            key = f"{home} - {away}"

            out[key] = {
                "1": None, "X": None, "2": None,
                "over25": None, "under25": None,
                "gg": None, "ng": None
            }

            for bookmaker in match["bookmakers"]:
                if bookmaker["key"] != "bet365":
                    continue

                for market in bookmaker["markets"]:

                    # 1X2
                    if market["key"] == "h2h":
                        for o in market["outcomes"]:
                            if o["name"] == home:
                                out[key]["1"] = o["price"]
                            elif o["name"] == away:
                                out[key]["2"] = o["price"]
                            elif o["name"] == "Draw":
                                out[key]["X"] = o["price"]

                    # Over/Under
                    if market["key"] == "totals":
                        for o in market["outcomes"]:
                            if o["name"] == "Over 2.5":
                                out[key]["over25"] = o["price"]
                            if o["name"] == "Under 2.5":
                                out[key]["under25"] = o["price"]

                    # GG/NG
                    if market["key"] == "btts":
                        for o in market["outcomes"]:
                            if o["name"] == "Yes":
                                out[key]["gg"] = o["price"]
                            if o["name"] == "No":
                                out[key]["ng"] = o["price"]

        return out
