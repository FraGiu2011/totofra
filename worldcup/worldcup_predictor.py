import numpy as np
import math
from worldcup.worldcup_loader import load_worldcup_results
from worldcup.worldcup_mapper import normalize_team_name

def compute_team_strengths():
    df = load_worldcup_results()

    teams = {}
    for _, row in df.iterrows():
        h = normalize_team_name(row["team_home"])
        a = normalize_team_name(row["team_away"])
        gh = row["goals_home"]
        ga = row["goals_away"]

        teams.setdefault(h, {"gf": 0, "ga": 0, "mp": 0})
        teams.setdefault(a, {"gf": 0, "ga": 0, "mp": 0})

        teams[h]["gf"] += gh
        teams[h]["ga"] += ga
        teams[h]["mp"] += 1

        teams[a]["gf"] += ga
        teams[a]["ga"] += gh
        teams[a]["mp"] += 1

    strengths = {}
    for t, stats in teams.items():
        mp = max(stats["mp"], 1)
        attack = stats["gf"] / mp
        defense = stats["ga"] / mp
        strengths[t] = {
            "attack_home": attack,
            "defense_home": defense,
            "attack_away": attack,
            "defense_away": defense,
            "attack": attack,
        }

    return strengths

TEAM_STRENGTHS = compute_team_strengths()

def get_team_parameters(team_name):
    norm = normalize_team_name(team_name)
    return TEAM_STRENGTHS.get(norm, {
        "attack_home": 1.0,
        "defense_home": 1.0,
        "attack_away": 1.0,
        "defense_away": 1.0,
        "attack": 1.0,
    })

def poisson_prob(lambda_home, lambda_away):
    max_goals = 10
    matrix = np.zeros((max_goals, max_goals))
    for i in range(max_goals):
        for j in range(max_goals):
            matrix[i][j] = (
                math.exp(-lambda_home) * lambda_home**i / math.factorial(i)
                *
                math.exp(-lambda_away) * lambda_away**j / math.factorial(j)
            )
    prob_home = matrix[np.triu_indices(max_goals, k=1)].sum()
    prob_draw = matrix[np.diag_indices(max_goals)].sum()
    prob_away = matrix[np.tril_indices(max_goals, k=-1)].sum()
    return prob_home, prob_draw, prob_away

def predict_match(team_home, team_away):
    p_home = get_team_parameters(team_home)
    p_away = get_team_parameters(team_away)

    lambda_home = p_home["attack_home"] * p_away["defense_away"]
    lambda_away = p_away["attack_away"] * p_home["defense_home"]

    prob_home, prob_draw, prob_away = poisson_prob(lambda_home, lambda_away)

    return {
        "prob_home_win": prob_home,
        "prob_draw": prob_draw,
        "prob_away_win": prob_away,
        "lambda_home": lambda_home,
        "lambda_away": lambda_away
    }
