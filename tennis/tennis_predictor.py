# ============================================================
# TENNIS PREDICTOR — Elo + Forma → Probabilità Vittoria
# ============================================================

from tennis.tennis_loader import load_atp_ranking, load_player_form
from tennis.tennis_mapper import normalize_player

def get_player_stats(player):
    df = load_atp_ranking()
    row = df[df["player"] == player]

    if row.empty:
        return {"elo": 1800, "form": 0.50}

    elo = row.iloc[0]["elo"]
    form = load_player_form(player)

    return {"elo": elo, "form": form}


def predict_match(player1, player2):
    p1 = normalize_player(player1)
    p2 = normalize_player(player2)

    stats1 = get_player_stats(p1)
    stats2 = get_player_stats(p2)

    score1 = stats1["elo"] * stats1["form"]
    score2 = stats2["elo"] * stats2["form"]

    prob1 = score1 / (score1 + score2)
    prob2 = 1 - prob1

    return {
        "player1": p1,
        "player2": p2,
        "prob1": round(prob1 * 100, 2),
        "prob2": round(prob2 * 100, 2)
    }
