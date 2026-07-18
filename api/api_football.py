import os
import csv
import requests


class APIFootball:

    BASE_URL = "https://v3.football.api-sports.io"

    # Mondiale 2026 (ID ufficiale API-FOOTBALL)
    WC_ID = 1
    SEASON = 2026

    # Fallback Mondiale 2022
    WC_FALLBACK_ID = 1
    WC_FALLBACK_SEASON = 2022

    def __init__(self):
        self.api_key = os.getenv("api_football_key")
        if not self.api_key:
            raise ValueError("API key non trovata. Usa: setx api_football_key \"LA_TUA_API_KEY\"")

        self.headers = {
            "x-apisports-key": self.api_key
        }

    # -----------------------------
    # FIXTURES (con fallback)
    # -----------------------------
    def get_worldcup_fixtures(self):
        url = f"{self.BASE_URL}/fixtures?league={self.WC_ID}&season={self.SEASON}"
        r = requests.get(url, headers=self.headers)
        data = r.json()["response"]

        if len(data) == 0:
            print("[WARN] Nessun dato Mondiale 2026. Uso fallback Mondiale 2022.")
            url = f"{self.BASE_URL}/fixtures?league={self.WC_FALLBACK_ID}&season={self.WC_FALLBACK_SEASON}"
            r = requests.get(url, headers=self.headers)
            data = r.json()["response"]

        return data

    # -----------------------------
    # RISULTATI REALI
    # -----------------------------
    def save_results_csv(self):
        data = self.get_worldcup_fixtures()
        rows = []

        for m in data:
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]

            gh = m["goals"]["home"]
            ga = m["goals"]["away"]

            rows.append({
                "home": home,
                "away": away,
                "goals_home": gh if gh is not None else "",
                "goals_away": ga if ga is not None else "",
                "match_date": m["fixture"]["date"]
            })

        if not rows:
            print("[WARN] Nessun risultato trovato.")
            return

        path = os.path.join("data", "worldcup_results.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"[OK] Risultati Mondiale aggiornati: {path}")

    # -----------------------------
    # CLASSIFICHE REALI (con fallback)
    # -----------------------------
    def get_worldcup_standings(self):
        url = f"{self.BASE_URL}/standings?league={self.WC_ID}&season={self.SEASON}"
        r = requests.get(url, headers=self.headers)
        data = r.json()["response"]

        if len(data) == 0:
            print("[WARN] Nessuna classifica Mondiale 2026. Uso fallback Mondiale 2022.")
            url = f"{self.BASE_URL}/standings?league={self.WC_FALLBACK_ID}&season={self.WC_FALLBACK_SEASON}"
            r = requests.get(url, headers=self.headers)
            data = r.json()["response"]

        return data[0]["league"]["standings"]

    def save_standings_csv(self):
        standings = self.get_worldcup_standings()
        rows = []

        for group in standings:
            for team in group:
                rows.append({
                    "group": team["group"],
                    "team": team["team"]["name"],
                    "pts": team["points"],
                    "gf": team["all"]["goals"]["for"],
                    "ga": team["all"]["goals"]["against"],
                    "gd": team["goalsDiff"],
                    "mp": team["all"]["played"]
                })

        path = os.path.join("data", "worldcup_standings.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"[OK] Standings Mondiale aggiornate: {path}")

    # -----------------------------
    # STATISTICHE SQUADRE (con fallback)
    # -----------------------------
    def get_team_stats(self, team_id):
        url = f"{self.BASE_URL}/teams/statistics?team={team_id}&league={self.WC_ID}&season={self.SEASON}"
        r = requests.get(url, headers=self.headers)
        data = r.json()["response"]

        if not data:
            url = f"{self.BASE_URL}/teams/statistics?team={team_id}&league={self.WC_FALLBACK_ID}&season={self.WC_FALLBACK_SEASON}"
            r = requests.get(url, headers=self.headers)
            data = r.json()["response"]

        return data

    def save_team_stats_csv(self):
        fixtures = self.get_worldcup_fixtures()
        team_ids = set()

        for m in fixtures:
            team_ids.add(m["teams"]["home"]["id"])
            team_ids.add(m["teams"]["away"]["id"])

        rows = []

        for tid in team_ids:
            try:
                stats = self.get_team_stats(tid)
            except:
                continue

            def safe(path, default=0):
                ref = stats
                for p in path:
                    if p not in ref or ref[p] is None:
                        return default
                    ref = ref[p]
                return ref

            rows.append({
                "team": safe(["team", "name"], ""),
                "mp": safe(["fixtures", "played", "total"]),
                "gf": safe(["goals", "for", "total", "total"]),
                "ga": safe(["goals", "against", "total", "total"]),
                "shots_for": safe(["shots", "total", "total"]),
                "shots_against": safe(["shots", "against", "total"]),
                "corners_for": safe(["corners", "total"]),
                "corners_against": safe(["corners", "against"]),
                "xg_for": safe(["expected", "goals", "for"]),
                "xg_against": safe(["expected", "goals", "against"])
            })

        path = os.path.join("data", "worldcup_team_stats_extended.csv")
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"[OK] Statistiche squadre aggiornate: {path}")

    # -----------------------------
    # AGGIORNAMENTO COMPLETO
    # -----------------------------
    def update_all(self):
        self.save_results_csv()
        self.save_standings_csv()
        self.save_team_stats_csv()


if __name__ == "__main__":
    APIFootball().update_all()
