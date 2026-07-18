import os
import csv

def load_tennis_elo():
    path = os.path.join("data", "tennis_elo_ratings.csv")
    players = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            player = row["player"].strip()
            elo = float(row["elo"])
            hard = float(row["hard"])
            clay = float(row["clay"])
            grass = float(row["grass"])

            # Elo totale = media pesata
            total = (elo * 0.5) + (hard * 0.2) + (clay * 0.2) + (grass * 0.1)

            players.append({
                "player": player,
                "elo": elo,
                "hard": hard,
                "clay": clay,
                "grass": grass,
                "total": total
            })

    return players


def generate_ranking_tennis():

    print("[INFO] Generazione ranking Tennis…")

    players = load_tennis_elo()

    # Ordina per Elo totale
    players_sorted = sorted(players, key=lambda x: x["total"], reverse=True)

    lines = []
    lines.append("=== RANKING TENNIS (ELO) ===\n")

    pos = 1
    for p in players_sorted:
        lines.append(f"{pos}) {p['player']}")
        lines.append(f"   Elo Base:   {p['elo']}")
        lines.append(f"   Hard:       {p['hard']}")
        lines.append(f"   Clay:       {p['clay']}")
        lines.append(f"   Grass:      {p['grass']}")
        lines.append(f"   Total Elo:  {p['total']:.2f}")
        lines.append("")
        pos += 1

    # Salvataggio
    output_path = os.path.join("output", "ranking_tennis.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Ranking Tennis generato: {output_path}")


if __name__ == "__main__":
    generate_ranking_tennis()
