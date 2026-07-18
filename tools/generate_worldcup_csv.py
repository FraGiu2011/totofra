import os
from api.footballdata_worldcup import (
    build_worldcup_results_csv,
    build_worldcup_team_ids_csv,
    build_worldcup_standings_csv,
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    results_path = os.path.join(DATA_DIR, "worldcup_results.csv")
    team_ids_path = os.path.join(DATA_DIR, "worldcup_team_ids.csv")
    standings_path = os.path.join(DATA_DIR, "worldcup_standings.csv")

    print("Rigenero worldcup_results.csv...")
    build_worldcup_results_csv(results_path)

    print("Rigenero worldcup_team_ids.csv...")
    build_worldcup_team_ids_csv(team_ids_path)

    print("Rigenero worldcup_standings.csv...")
    build_worldcup_standings_csv(standings_path)

    print("CSV Mondiale aggiornati con football-data.org.")


if __name__ == "__main__":
    main()
