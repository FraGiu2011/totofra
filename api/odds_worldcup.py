import requests
import os
from requests.exceptions import HTTPError

class WorldCupOdds:

    BASE_URL = "https://v3.football.api-sports.io"
    WC_ID = 1
    SEASON = 2022

    def __init__(self):
        self.api_key = os.getenv("api_football_key")
        if not self.api_key:
            raise ValueError("API key non trovata.")

        self.headers = {
            "x-apisports-key": self.api_key
        }

    def get_odds(self, home, away):
        url = f"{self.BASE_URL}/odds?league={self.WC_ID}&season={self.SEASON}"

        try:
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
        except HTTPError:
            return None

        data = r.json()["response"]

        for match in data:
            h = match["teams"]["home"]["name"].lower()
            a = match["teams"]["away"]["name"].lower()

            if h == home.lower() and a == away.lower():
                bookmakers = match["bookmakers"]
                if not bookmakers:
                    return None

                markets = bookmakers[0]["bets"]
                for m in markets:
                    if m["name"] == "Match Winner":
                        odds = m["values"]
                        return {
                            "1": float(odds[0]["odd"]),
                            "X": float(odds[1]["odd"]),
                            "2": float(odds[2]["odd"])
                        }

        return None
