def _prob_from_odds(odds):
    if odds is None or odds == 0:
        return None
    return 1 / odds


def totofra_score(match):
    """
    Versione AGGRESSIVA del TotoFra Score.
    Amplifica differenze, penalizza match equilibrati,
    boosta match con favorito chiaro.
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

    base = (
        (p1 * 100 * 0.60) +
        (px * 100 * 0.05) +
        (p2 * 100 * 0.60)
    )

    if imbalance < 0.15:
        base *= 0.55
    elif imbalance < 0.25:
        base *= 0.75

    if imbalance > 0.40:
        base *= 1.20

    base = max(0, min(base, 100))
    return round(base, 1)
