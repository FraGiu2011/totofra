def _prob_from_odds(odds):
    if odds is None or odds == 0:
        return None
    return 1 / odds


def radar_rischio(match):
    """
    Versione AGGRESSIVA del Radar Rischio.
    Più il match è incerto → rischio altissimo.
    Favorito chiaro → rischio molto basso.
    """
    p1 = _prob_from_odds(match.get("odds_home"))
    px = _prob_from_odds(match.get("odds_draw"))
    p2 = _prob_from_odds(match.get("odds_away"))

    if not all([p1, px, p2]):
        return 50

    total = p1 + px + p2
    p1 /= total
    px /= total
    p2 /= total

    imbalance = abs(p1 - p2)

    rischio = (1 - imbalance) * 0.75 + px * 0.25

    if imbalance < 0.10:
        rischio *= 1.30

    if imbalance > 0.45:
        rischio *= 0.70

    rischio = max(0, min(rischio * 100, 100))
    return round(rischio, 1)
