import os
import csv

def load_worldcup_stats():
    path = os.path.join("data", "worldcup_team_stats.csv")
    stats = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team = row["team"].strip().lower()
            ah = float(row["attack_home"])
            dh = float(row["defense_home"])
            aa = float(row["attack_away"])
            da = float(row["defense_away"])

            # Forza totale (media pesata)
            total_strength = (ah + aa) - (dh + da)

            stats.append({
                "team": team,
                "attack_home": ah,
                "defense_home": dh,
                "attack_away": aa,
                "defense_away": da,
                "strength": total_strength
            })

    return stats


def generate_ranking_worldcup():

    print("[INFO] Generazione ranking Mondiale…")

    stats = load_worldcup_stats()

    # Ordina per forza totale
    stats_sorted = sorted(stats, key=lambda x: x["strength"], reverse=True)

    lines = []
    lines.append("=== RANKING MONDIALE ===\n")

    pos = 1
    for s in stats_sorted:
        lines.append(f"{pos}) {s['team'].title()}")
        lines.append(f"   Attack Home:  {s['attack_home']}")
        lines.append(f"   Defense Home: {s['defense_home']}")
        lines.append(f"   Attack Away:  {s['attack_away']}")
        lines.append(f"   Defense Away: {s['defense_away']}")
        lines.append(f"   Strength:     {s['strength']:.3f}")
        lines.append("")
        pos += 1

    # Salvataggio
    output_path = os.path.join("output", "ranking_worldcup.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Ranking Mondiale generato: {output_path}")


if __name__ == "__main__":
    generate_ranking_worldcup()
