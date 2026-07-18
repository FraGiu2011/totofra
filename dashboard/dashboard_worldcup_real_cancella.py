import pandas as pd
import matplotlib.pyplot as plt
import os
import math

# ----------------------------------------------------
# 1) CARICAMENTO CSV REALI
# ----------------------------------------------------

def load_data():
    results = pd.read_csv("data/worldcup_results.csv")
    standings = pd.read_csv("data/worldcup_standings.csv")
    stats = pd.read_csv("data/worldcup_team_stats.csv")
    return results, standings, stats


# ----------------------------------------------------
# 2) GRAFICO GF / GA
# ----------------------------------------------------

def plot_goals(stats, ax):
    stats_sorted = stats.sort_values("gf", ascending=False)

    ax.bar(stats_sorted["team"], stats_sorted["gf"], label="GF", color="green")
    ax.bar(stats_sorted["team"], stats_sorted["ga"], label="GA", color="red", alpha=0.6)

    ax.set_title("Gol Fatti / Subiti (Reali)")
    ax.set_xticklabels(stats_sorted["team"], rotation=90)
    ax.legend()


# ----------------------------------------------------
# 3) GRAFICO RADAR PER UNA SQUADRA
# ----------------------------------------------------

def plot_radar(stats, team, ax):
    row = stats[stats["team"] == team].iloc[0]

    labels = ["GF", "GA", "Shots For", "Shots Against", "Corners For", "Corners Against", "xG For", "xG Against"]
    values = [
        row["gf"], row["ga"],
        row["shots_for"], row["shots_against"],
        row["corners_for"], row["corners_against"],
        row["xg_for"], row["xg_against"]
    ]

    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    values += values[:1]
    angles += angles[:1]

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title(f"Radar Stats – {team}")


# ----------------------------------------------------
# 4) DASHBOARD COMPLETA
# ----------------------------------------------------

def generate_dashboard():
    results, standings, stats = load_data()

    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("Dashboard Mondiale Reale – API-FOOTBALL", fontsize=18)

    # grafico GF/GA
    ax1 = fig.add_subplot(2, 2, 1)
    plot_goals(stats, ax1)

    # radar team top
    top_team = standings.sort_values("pts", ascending=False).iloc[0]["team"]
    ax2 = fig.add_subplot(2, 2, 2, polar=True)
    plot_radar(stats, top_team, ax2)

    # classifica
    ax3 = fig.add_subplot(2, 2, 3)
    standings_sorted = standings.sort_values("pts", ascending=False)
    ax3.barh(standings_sorted["team"], standings_sorted["pts"], color="blue")
    ax3.set_title("Classifica Reale (Punti)")
    ax3.invert_yaxis()

    # xG confronto
    ax4 = fig.add_subplot(2, 2, 4)
    stats_sorted = stats.sort_values("xg_for", ascending=False)
    ax4.bar(stats_sorted["team"], stats_sorted["xg_for"], label="xG For", color="purple")
    ax4.bar(stats_sorted["team"], stats_sorted["xg_against"], label="xG Against", color="orange", alpha=0.6)
    ax4.set_title("Expected Goals (xG)")
    ax4.set_xticklabels(stats_sorted["team"], rotation=90)
    ax4.legend()

    os.makedirs("output", exist_ok=True)
    plt.tight_layout()
    plt.savefig("output/dashboard_worldcup_real.png", dpi=200)

    print("[OK] Dashboard Mondiale reale generata: output/dashboard_worldcup_real.png")


if __name__ == "__main__":
    generate_dashboard()
