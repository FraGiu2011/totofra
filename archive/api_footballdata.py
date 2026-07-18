import requests
import os

class FootballDataAPI:
    BASE_URL = "https://api.football-data.org/v4/"
    
    def __init__(self):
        self.api_key = os.getenv("FOOTBALL_DATA_API_KEY")
        if not self.api_key:
            raise ValueError("⚠️ Variabile d'ambiente FOOTBALL_DATA_API_KEY non trovata.")

    def _get(self, endpoint):
        headers = {"X-Auth-Token": self.api_key}
        url = self.BASE_URL + endpoint
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_matches(self, competition_code="SA"):
        """
        competition_code:
        SA = Serie A
        PL = Premier League
        CL = Champions League
        PD = La Liga
        BL1 = Bundesliga
        """
        data = self._get(f"competitions/{competition_code}/matches?status=SCHEDULED")
        matches = []

        for m in data["matches"]:
            matches.append({
                "home": m["homeTeam"]["name"],
                "away": m["awayTeam"]["name"]
            })

        return matches
