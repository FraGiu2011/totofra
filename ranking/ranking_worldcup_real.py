import csv
import os
from collections import defaultdict

# ----------------------------------------------------
# 1) CARICAMENTO RISULTATI REALI (API-FOOTBALL → CSV)
# ----------------------------------------------------

def load_results():
    path = os.path.join("data", "worldcup_results.csv")
    results = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["goals_home"] == "" or row["goals_away"] == "":
                continue

            results.append({
                "home": row["home"],
                "away": row["away"],
                "gh": int(row["goals_home"]),
                "ga": int(row["goals_away"])
            })

    return results


# ----------------------------------------------------
# 2) CALCOLO STATISTICHE DA RISULTATI REALI
# ----------------------------------------------------

def compute_table(results):
    table = defaultdict(lambda: {
        "mp": 0,
        "gf": 0,
        "ga": 0,
        "gd": 0,
        "pts": 0
    })

    for m in results:
        h = m["home"]
        a = m["away"]
        gh = m["gh"]
        ga = m["ga"]

        # partite giocate
        table[h]["mp"] += 1
        table[a]["mp"] += 1

        # gol
        table[h]["gf"] += gh
        table[h]["ga"] += ga
        table[a]["gf"] += ga
        table[a]["ga"] += gh

        # differenza reti
        table[h]["gd"] = table[h]["gf"] - table[h]["ga"]
        table[a]["gd"] = table[a]["gf"] - table[a]["ga"]

        # punti
        if gh > ga:
            table[h]["pts"] += 3
        elif ga > gh:
            table[a]["pts"] += 3
        else:
            table[h]["pts"] += 1
            table[a]["pts"] += 1

    return table


# ----------------------------------------------------
# 3) SALVATAGGIO RANKING
# ----------------------------------------------------

def save_ranking(table):
    rows = sorted(
        table.items(),
        key=lambda x: (x[1]["pts"], x[1]["gd"], x[1]["gf"]),
        reverse=True
    )

    path = os.path.join("output", "ranking_worldcup_real.txt")

    with open(path, "w", encoding="utf-8") as f:
        f.write("=== RANKING MONDIALE (REALE – API-FOOTBALL) ===\n\n")

        pos = 1
        for team, stats in rows:
            f.write(f"{pos}) {team}\n")
            f.write(f"   Punti: {stats['pts']}\n")
            f.write(f"   Partite: {stats['mp']}\n")
            f.write(f"   GF: {stats['gf']}  GA: {stats['ga']}  GD: {stats['gd']}\n\n")
            pos += 1

    print(f"[OK] Ranking Mondiale reale generato: {path}")


# ----------------------------------------------------
# 4) MAIN
# ----------------------------------------------------

def generate_ranking():
    print("[INFO] Generazione ranking Mondiale reale…")
    results = load_results()
    table = compute_table(results)
    save_ranking(table)


if __name__ == "__main__":
    generate_ranking()
