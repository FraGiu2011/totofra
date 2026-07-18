import unittest
import os

from worldcup.worldcup_quarterfinals import filter_quarterfinal_matches
from worldcup.worldcup_schedina_quarters import generate_schedina_quarters
from worldcup.worldcup_ranking_quarters import generate_ranking_quarters
from worldcup.worldcup_dashboard_quarters import generate_dashboard_quarters_html
from worldcup.worldcup_predictor import predict_match


class TestWorldCupQuarters(unittest.TestCase):

    def test_quarters_filter(self):
        """Verifica che il filtro dei quarti produca solo match tra le 8 squadre selezionate."""
        df = filter_quarterfinal_matches()
        self.assertGreater(len(df), 0, "Nessuna partita trovata per i quarti.")

        valid_teams = {
            "argentina", "brazil", "france", "portugal",
            "germany", "spain", "england", "netherlands"
        }

        for _, row in df.iterrows():
            self.assertIn(row["team_home"].lower(), valid_teams)
            self.assertIn(row["team_away"].lower(), valid_teams)

    def test_schedina_quarters(self):
        """Verifica che la schedina dei quarti venga generata correttamente."""
        df = generate_schedina_quarters()
        self.assertGreater(len(df), 0, "Schedina quarti vuota.")
        required_cols = ["home", "away", "prob_1", "prob_x", "prob_2", "value_1", "value_x", "value_2"]
        for col in required_cols:
            self.assertIn(col, df.columns)

    def test_ranking_quarters(self):
        """Verifica che il ranking dei quarti venga generato correttamente."""
        df = generate_ranking_quarters()
        self.assertGreater(len(df), 0, "Ranking quarti vuoto.")
        required_cols = ["team_home", "team_away", "prob_home_win", "prob_draw", "prob_away_win"]
        for col in required_cols:
            self.assertIn(col, df.columns)

    def test_predictor_quarters(self):
        """Verifica che il predictor funzioni per una partita dei quarti."""
        df = filter_quarterfinal_matches()
        home = df.iloc[0]["team_home"]
        away = df.iloc[0]["team_away"]

        pred = predict_match(home, away)

        self.assertIn("prob_home_win", pred)
        self.assertIn("prob_draw", pred)
        self.assertIn("prob_away_win", pred)

        self.assertGreaterEqual(pred["prob_home_win"], 0)
        self.assertGreaterEqual(pred["prob_draw"], 0)
        self.assertGreaterEqual(pred["prob_away_win"], 0)

    def test_dashboard_quarters(self):
        """Verifica che la dashboard quarti venga generata correttamente."""
        html = generate_dashboard_quarters_html()
        self.assertIsInstance(html, str)
        self.assertIn("<html>", html)
        self.assertIn("Dashboard Quarti", html)


if __name__ == "__main__":
    unittest.main()
