import os
from core.modello_poisson import PoissonModel
from core.team_normalizer import TeamNormalizer
from core.data_cleaner import DataCleaner
from core.comparator import Comparator
import json

def load_mock_or_api():
    """
    Per ora usiamo il mock del test.
    In seguito collegheremo l'API Mondiale.
    """
    mock_path = os.path.join("tests", "mock_worldcup.json")
    with open(mock_path, encoding="utf-8") as f:
        raw = json.load(f)

    matches = []
    for m in raw:
        matches.append({
            "home": m["home_team"],
            "away": m["away_team"],
            "odds": {
                "1": m["odds_1"],
                "X": m["odds_X"],
                "2": m["odds_2"]
            }
        })

    return matches


def generate_dashboard_worldcup():

    print("[INFO] Generazione dashboard Mondiale…")

    # 1) Carica match
    matches = load_mock_or_api()

    # 2) Normalizzazione
    normalizer = TeamNormalizer()
    normalized = normalizer.normalize_all_matches(matches)

    # 3) Pulizia
    cleaner = DataCleaner()
    cleaned = cleaner.clean(normalized)

    # 4) Modello Poisson
    model = PoissonModel("worldcup")
    model.normalizer = normalizer
    predictions = model.predict(cleaned)

    # 5) Comparator (mock tipster + real odds)
    comparator = Comparator()

    tipster_predictions = {}
    real_odds = {}

    for m in cleaned:
        key = f"{m['home']}-{m['away']}"
        tipster_predictions[key] = {
            "prob_1": 0.33,
            "prob_x": 0.33,
            "prob_2": 0.33
        }
        real_odds[key] = {
            "odds_1": m["odds"]["1"],
            "odds_X": m["odds"]["X"],
            "odds_2": m["odds"]["2"]
        }

    final = comparator.compare(predictions, tipster_predictions, real_odds)

    # 6) HTML
    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>TotoFra – Dashboard Mondiale</title>
        <style>
            body { font-family: Arial; background: #f4f4f4; padding: 20px; }
            table { width: 100%; border-collapse: collapse; background: white; }
            th, td { padding: 10px; border-bottom: 1px solid #ddd; text-align: center; }
            th { background: #222; color: white; }
            tr:hover { background: #f1f1f1; }
            .good { background: #d4edda; }
            .bad { background: #f8d7da; }
        </style>
    </head>
    <body>
        <h1>TotoFra – Dashboard Mondiale</h1>
        <h3>Probabilità Poisson + Value Betting</h3>

        <table>
            <tr>
                <th>Casa</th>
                <th>Trasferta</th>
                <th>Prob 1</th>
                <th>Prob X</th>
                <th>Prob 2</th>
                <th>Quota 1</th>
                <th>Quota X</th>
                <th>Quota 2</th>
                <th>Value 1</th>
                <th>Value X</th>
                <th>Value 2</th>
            </tr>
    """

    for m in final:
        html += f"""
        <tr>
            <td>{m['home'].title()}</td>
            <td>{m['away'].title()}</td>
            <td>{m['prob_1']:.3f}</td>
            <td>{m['prob_x']:.3f}</td>
            <td>{m['prob_2']:.3f}</td>
            <td>{real_odds[f"{m['home']}-{m['away']}"]['odds_1']}</td>
            <td>{real_odds[f"{m['home']}-{m['away']}"]['odds_X']}</td>
            <td>{real_odds[f"{m['home']}-{m['away']}"]['odds_2']}</td>
            <td>{m['value_1']}</td>
            <td>{m['value_x']}</td>
            <td>{m['value_2']}</td>
        </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    # 7) Salvataggio
    output_path = os.path.join("output", "dashboard_worldcup.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Dashboard Mondiale generata: {output_path}")

if __name__ == "__main__":
    generate_dashboard_worldcup()

