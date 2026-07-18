import requests
from tipster.base_tipster import BaseTipster

class FootballDataOddsTipster(BaseTipster):

    def __init__(self, api_key):
        self.api_key = api_key

    def get_predictions(self, date_str: str):
        url = "https://api.football-data.org/v4/matches"
        headers = {"X-Auth-Token": self.api_key}
        params = {"dateFrom": date_str, "dateTo": date_str}

        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()

        predictions = []

        for match in data.get("matches", []):
            home = match["homeTeam"]["name"]
            away = match["awayTeam"]["name"]

            odds = match.get("odds", {})
            if not odds:
                continue

            for market in odds.get("markets", []):
                if market["key"] == "1X2":
                    for outcome in market["outcomes"]:
                        predictions.append({
                            "source": "FootballDataOdds",
                            "home": home,
                            "away": away,
                            "market": "1X2",
                            "pick": outcome["name"],
                            "prob": None,
                            "odds": outcome.get("price")
                        })

        return predictions
