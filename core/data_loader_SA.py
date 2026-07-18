import requests

# Carichiamo TUTTA la stagione Bundesliga 2024
OPENLIGA_SA_URL = "https://api.openligadb.de/getmatchdata/bl1/2024"


def load_matches_SA():
    """
    Carica i match della Bundesliga 2024 da OpenLigaDB.
    Restituisce una lista di dict:
    [
        {"home": "Team1", "away": "Team2"},
        ...
    ]
    """

    try:
        response = requests.get(OPENLIGA_SA_URL)
        data = response.json()
    except Exception as e:
        print(f"Errore OpenLigaDB: {e}")
        return []

    matches = []

    for m in data:
        home = m.get("Team1", {}).get("TeamName")
        away = m.get("Team2", {}).get("TeamName")

        if home and away:
            matches.append({
                "home": home,
                "away": away
            })

    print(f"[DEBUG] Match trovati da OpenLigaDB: {len(matches)}")
    if matches:
        print(f"[DEBUG] Esempio: {matches[0]}")

    return matches
