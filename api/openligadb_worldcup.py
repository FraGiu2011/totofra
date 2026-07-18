import requests
import csv
import os


class OpenLigaDBWorldCup:

    BASE_LIST_URL = "https://api.openligadb.de/getavailableleagues"
    BASE_MATCH_URL = "https://api.openligadb.de/getmatchdata/{shortcut}"

    def find_worldcup_shortcut(self):
        print("[INFO] Scansione tornei disponibili su OpenLigaDB…")
        r = requests.get(self.BASE_LIST_URL, timeout=10)
        r.raise_for_status()
        leagues = r.json()

        candidates = []
        for lg in leagues:
            name = lg.get("leagueName", "").lower()
            shortcut = lg.get("leagueShortcut", "").lower()

            if any(k in name for k in ["world", "cup", "wm", "fifa"]):
                candidates.append(shortcut)

        if not candidates:
            print("[WARN] Nessun torneo Mondiale trovato su OpenLigaDB.")
            return None

        shortcut = candidates[-1]
        print(f"[INFO] Trovato torneo Mondiale: shortcut = {shortcut}")
        return shortcut

    def fetch_results(self, shortcut):
        url = self.BASE_MATCH_URL.format(shortcut=shortcut)
        print(f"[INFO] Fetching World Cup results from: {url}")
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()

    def save_results_csv(self, data):
        if not data:
            print("[WARN] Nessun risultato disponibile.")
            return

        path = os.path.join("data", "worldcup_results.csv")

        rows = []
        for match in data:
            home = match["team1"]["teamName"]
            away = match["team2"]["teamName"]

            goals_home = None
            goals_away = None

            if match.get("matchResults"):
                for res in match["matchResults"]:
                    if res["resultTypeID"] == 2:
                        goals_home = res["pointsTeam1"]
                        goals_away = res["pointsTeam2"]

            rows.append({
                "home": home,
                "away": away,
                "goals_home": goals_home,
                "goals_away": goals_away,
                "match_date": match["matchDateTime"]
            })

        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"[OK] worldcup_results.csv aggiornato: {path}")

    def update(self):
        shortcut = self.find_worldcup_shortcut()
        if not shortcut:
            return

        data = self.fetch_results(shortcut)
        self.save_results_csv(data)


# ============================================================
# FUNZIONE PER LA SCHEDINA MONDIALE
# ============================================================

def load_worldcup_matches():
    """
    Restituisce i match del Mondiale in formato:
    [
        {"home": "Team1", "away": "Team2"},
        ...
    ]
    """

    wc = OpenLigaDBWorldCup()   # <--- QUESTA È LA RIGA CORRETTA
    shortcut = wc.find_worldcup_shortcut()

    if not shortcut:
        print("[WARN] Nessun torneo Mondiale trovato.")
        return []

    data = wc.fetch_results(shortcut)

    matches = []

    for match in data:
        home = match.get("team1", {}).get("teamName")
        away = match.get("team2", {}).get("teamName")

        if home and away:
            matches.append({
                "home": home,
                "away": away
            })

    print(f"[DEBUG] Match Mondiale trovati: {len(matches)}")
    if matches:
        print(f"[DEBUG] Esempio: {matches[0]}")

    return matches


if __name__ == "__main__":
    OpenLigaDBWorldCup().update()
