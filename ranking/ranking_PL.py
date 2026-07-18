import os
import csv

def load_premier_league_stats():
    path = os.path.join("data", "premier_league_team_stats.csv")
    stats = []

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            team = row["team"].strip().lower()

            # Colonne moderne
            cf = float(row["corners_for"])
            ca = float(row["corners_against"])
            xgf = float(row["xg_for"])
            xga = float(row["xg_against"])
            sf = float(row["shots_for"])
            sa = float(row["shots_against"])

            # Forza totale (stessa formula del Mondiale)
            strength = (
                xgf * 0.6 +
                sf * 0.3 +
                cf * 0.1
            ) - (
                xga * 0.6 +
                sa * 0.3 +
                ca * 0.1
            )

            stats.append({
                "team": team,
                "corners_for": cf,
                "corners_against": ca,
                "xg_for": xgf,
                "xg_against": xga,
                "shots_for": sf,
                "shots_against": sa,
                "strength": strength
            })

    return stats


def generate_ranking_PL():

    print("[INFO] Generazione ranking Premier League…")

    stats = load_premier_league_stats()

    # Ordina per forza totale
    stats_sorted = sorted(stats, key=lambda x: x["strength"], reverse=True)

    lines = []
    lines.append("=== RANKING PREMIER LEAGUE ===\n")

    pos = 1
    for s in stats_sorted:
        lines.append(f"{pos}) {s['team'].title()}")
        lines.append(f"   xG For:        {s['xg_for']}")
        lines.append(f"   xG Against:    {s['xg_against']}")
        lines.append(f"   Shots For:     {s['shots_for']}")
        lines.append(f"   Shots Against: {s['shots_against']}")
        lines.append(f"   Corners For:   {s['corners_for']}")
        lines.append(f"   Corners Ag.:   {s['corners_against']}")
        lines.append(f"   Strength:      {s['strength']:.3f}")
        lines.append("")
        pos += 1

    # Salvataggio
    output_path = os.path.join("output", "ranking_PL.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] Ranking Premier League generato: {output_path}")


if __name__ == "__main__":
    generate_ranking_PL()
