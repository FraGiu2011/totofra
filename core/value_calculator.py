# value_calculator.py

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class OutcomeProbabilities:
    """
    Probabilità stimate dal modello TotoFra per il mercato 1X2.
    Tutti i valori devono essere compresi tra 0 e 1.
    """
    home_win: float  # P(1)
    draw: float      # P(X)
    away_win: float  # P(2)


@dataclass
class OutcomeOdds:
    """
    Quote del bookmaker per il mercato 1X2.
    Tipicamente provenienti da OddsAPI (es. Bet365).
    """
    home_win: float  # quota 1
    draw: float      # quota X
    away_win: float  # quota 2


@dataclass
class OutcomeValue:
    """
    Risultato del calcolo del value per ogni esito 1X2.
    """
    value_home: float
    value_draw: float
    value_away: float


def _calculate_single_value(probability: float, odds: float) -> float:
    """
    Calcola il value per un singolo esito.
    Formula: value = (probabilità * quota) - 1
    """
    return (probability * odds) - 1.0


def calculate_value_1x2(
    probabilities: OutcomeProbabilities,
    odds: OutcomeOdds
) -> OutcomeValue:
    """
    Calcola il value per il mercato 1X2 dato:
    - probabilità stimate dal modello TotoFra
    - quote del bookmaker (OddsAPI)

    Restituisce un oggetto OutcomeValue con:
    - value_home (1)
    - value_draw (X)
    - value_away (2)
    """
    value_home = _calculate_single_value(probabilities.home_win, odds.home_win)
    value_draw = _calculate_single_value(probabilities.draw, odds.draw)
    value_away = _calculate_single_value(probabilities.away_win, odds.away_win)

    return OutcomeValue(
        value_home=value_home,
        value_draw=value_draw,
        value_away=value_away
    )


def as_dict(value: OutcomeValue) -> Dict[str, float]:
    """
    Converte l'OutcomeValue in un dizionario semplice,
    utile per logging, JSON, stampa in schedina, ecc.
    """
    return {
        "value_1": value.value_home,
        "value_X": value.value_draw,
        "value_2": value.value_away,
    }


def best_value_outcome(value: OutcomeValue) -> Optional[str]:
    """
    Restituisce l'esito con il value più alto tra 1, X, 2.
    Non applica soglie: è solo un confronto.
    Ritorna '1', 'X', '2' oppure None se tutti i value sono uguali.
    """
    values_map = {
        "1": value.value_home,
        "X": value.value_draw,
        "2": value.value_away,
    }

    max_value = max(values_map.values())
    # Se tutti uguali, non ha senso scegliere
    if list(values_map.values()).count(max_value) > 1:
        return None

    for outcome, v in values_map.items():
        if v == max_value:
            return outcome

    return None
