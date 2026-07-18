from core.modello_poisson import PoissonModel

# Creiamo un'istanza globale del modello Poisson per la Serie A
poisson_SA = PoissonModel(league="SA")


def calculate_probabilities_1x2(home_team, away_team):
    """
    Restituisce un dict con:
    - P1
    - PX
    - P2

    Usa il modello Poisson già presente nel progetto.
    """

    result = poisson_SA.predict_match(home_team, away_team)

    return {
        "P1": result["home_win"],
        "PX": result["draw"],
        "P2": result["away_win"]
    }
