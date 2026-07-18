import requests

class FootyStatsAPI:
    BASE_URL = "https://footystats.org/api/"

    def __init__(self):
        # API pubblica gratuita (dataset statico)
        self.key = "1.0"

    def get_team_stats(self, team_name):
        """
        Ritorna corner stats, over/under, forma, xG.
        """
        url = f"{self.BASE_URL}v1/teams?key={self.key}&team={team_name}"
        response = requests.get(url)
        if response.status_code != 200:
            return None

        data = response.json()

        if "data" not in data or len(data["data"]) == 0:
            return None

        team = data["data"][0]

        return {
            "team": team_name,
            "corners_avg": team.get("corners_avg", None),
            "corners_for": team.get("corners_for", None),
            "corners_against": team.get("corners_against", None),
            "over_2_5": team.get("over_2_5", None),
            "over_3_5": team.get("over_3_5", None),
            "xG": team.get("xG", None),
            "xGA": team.get("xGA", None),
            "form": team.get("form", None)
        }
