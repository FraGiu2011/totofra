import json
import unittest

from worldcup.worldcup_loader import (
    load_worldcup_results,
    load_worldcup_standings,
    load_worldcup_team_stats,
    load_worldcup_team_stats_extended,
    load_worldcup_team_ids,
    load_all_worldcup_data
)

from worldcup.worldcup_mapper import (
    normalize_team_name,
    get_team_id,
    get_team_name,
    map_team_names
)

from worldcup.worldcup_predictor import (
    predict_match,
    get_team_parameters
)

from worldcup.worldcup_schedina import (
    generate_schedina
)

from worldcup.worldcup_ranking import (
    generate_worldcup_ranking
)

from worldcup.worldcup_ranking_real import (
    generate_worldcup_ranking_real
)

from worldcup.worldcup_dashboard import (
    generate_worldcup_dashboard_html
)

from worldcup.worldcup_dashboard_real import (
    generate_worldcup_dashboard_real_html
)

from main_worldcup import run_all


# ============================================================
#  MOCK LOADER
# ============================================================

def load_mock():
    with open("tests/mock_worldcup.json", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
#  TEST SU TUTTO IL MODULO MONDIALE
# ============================================================

class TestWorldCupModule(unittest.TestCase):

    def test_loader(self):
        print("\n=== TEST LOADER MONDIALE ===")
        self.assertFalse(load_worldcup_results().empty)
        self.assertFalse(load_worldcup_standings().empty)
        self.assertFalse(load_worldcup_team_stats().empty)
        self.assertFalse(load_worldcup_team_stats_extended().empty)
        self.assertFalse(load_worldcup_team_ids().empty)
        self.assertIn("results", load_all_worldcup_data())

    def test_mapper(self):
        print("\n=== TEST MAPPER MONDIALE ===")
        self.assertEqual(normalize_team_name("USA"), "united states")
        tid = get_team_id("Brazil")
        self.assertIsNotNone(tid)
        self.assertEqual(get_team_name(tid).lower(), "brazil")

    def test_predictor(self):
        print("\n=== TEST PREDICTOR MONDIALE ===")
        params = get_team_parameters("Brazil")
        self.assertIn("attack", params)
        result = predict_match("Brazil", "Argentina")
        self.assertIn("prob_home_win", result)

    def test_schedina(self):
        print("\n=== TEST SCHEDINA MONDIALE ===")
        schedina = generate_schedina()
        self.assertIsInstance(schedina, list)

    def test_ranking_simulated(self):
        print("\n=== TEST RANKING SIMULATO MONDIALE ===")
        ranking = generate_worldcup_ranking()
        self.assertFalse(ranking.empty)

    def test_ranking_real(self):
        print("\n=== TEST RANKING REALE MONDIALE ===")
        ranking = generate_worldcup_ranking_real()
        self.assertFalse(ranking.empty)

    def test_dashboard(self):
        print("\n=== TEST DASHBOARD MONDIALE ===")
        html = generate_worldcup_dashboard_html()
        self.assertIn("<html>", html)

    def test_dashboard_real(self):
        print("\n=== TEST DASHBOARD REALE MONDIALE ===")
        html = generate_worldcup_dashboard_real_html()
        self.assertIn("<html>", html)

    def test_main_worldcup(self):
        print("\n=== TEST MAIN MONDIALE ===")
        run_all()  # deve eseguire tutto senza errori


if __name__ == "__main__":
    unittest.main()
