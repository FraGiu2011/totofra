import requests
import os

class OddsMatchFetcherTennis:
    def __init__(self):
        self.api_key = os.getenv("ODDS_API_KEY")
        self.url = "https://api.the-odds-api.com/v4/sports/tennis/odds/"

    def get_matches(self):
        params = {
            "apiKey": self.api_key,
            "regions": "eu",
            "markets": "h2h",
            "oddsFormat": "decimal"
        }
        try:
            r = requests.get(self.url, params=params, timeout=10)
            if r.status_code != 200:
                print("[ERROR] OddsAPI Tennis:", r.text)
                return []
            return r.json()
        except Exception as e:
            print("[ERROR] Tennis fetch exception:", e)
            return []

    def parse_matches(self, raw):
        matches = []
        for m in raw:
            if "bookmakers" not in m or len(m["bookmakers"]) == 0:
                continue

            bm = m["bookmakers"][0]
            if "markets" not in bm or len(bm["markets"]) == 0:
                continue

            outcomes = bm["markets"][0]["outcomes"]
            if len(outcomes) != 2:
                continue

            p1 = outcomes[0]["name"]
            p2 = outcomes[1]["name"]
            o1 = outcomes[0]["price"]
            o2 = outcomes[1]["price"]

            matches.append({
                "player1": p1,
                "player2": p2,
                "odds": {"1": o1, "2": o2}
            })

        return matches
