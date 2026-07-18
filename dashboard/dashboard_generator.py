# dashboard/dashboard_generator.py

import os
import json

OUTPUT_DIR = "dashboard_output"

def _ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def generate_dashboard(matches, competition):
    """
    Dashboard classica per le partite (PL, SA, tennis match, ecc.)
    """
    _ensure_output_dir()
    filename = os.path.join(OUTPUT_DIR, f"dashboard_{competition}.html")

    rows = []
    for m in matches:
        # Adatta questi campi alla tua struttura reale
        match_name = m.get("match", "")
        prob_1 = m.get("prob_1", "")
        prob_2 = m.get("prob_2", "")
        odds_1 = m.get("odds_1", "")
        odds_2 = m.get("odds_2", "")
        value_1 = m.get("value_1", "")
        value_2 = m.get("value_2", "")

        rows.append(f"""
        <tr>
            <td>{match_name}</td>
            <td>{prob_1}</td>
            <td>{prob_2}</td>
            <td>{odds_1}</td>
            <td>{odds_2}</td>
            <td>{value_1}</td>
            <td>{value_2}</td>
        </tr>
        """)

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Dashboard {competition}</title>
    </head>
    <body>
        <h1>Dashboard {competition}</h1>
        <table border="1" cellspacing="0" cellpadding="4">
            <tr>
                <th>Match</th>
                <th>Prob 1</th>
                <th>Prob 2</th>
                <th>Odds 1</th>
                <th>Odds 2</th>
                <th>Value 1</th>
                <th>Value 2</th>
            </tr>
            {''.join(rows)}
        </table>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[INFO] Dashboard generata: {filename}")


def generate_ranking_dashboard(ranking, sport):
    """
    Dashboard per il ranking Elo tennis (o altri sport in futuro).
    """
    _ensure_output_dir()
    filename = os.path.join(OUTPUT_DIR, f"dashboard_ranking_{sport}.html")

    rows = []
    for idx, r in enumerate(ranking, start=1):
        player = r.get("player", "")
        elo = r.get("elo", "")
        rows.append(f"""
        <tr>
            <td>{idx}</td>
            <td>{player}</td>
            <td>{elo}</td>
        </tr>
        """)

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Ranking Elo {sport}</title>
    </head>
    <body>
        <h1>Ranking Elo {sport}</h1>
        <table border="1" cellspacing="0" cellpadding="4">
            <tr>
                <th>#</th>
                <th>Giocatore</th>
                <th>Elo</th>
            </tr>
            {''.join(rows)}
        </table>
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[INFO] Dashboard ranking generata: {filename}")
