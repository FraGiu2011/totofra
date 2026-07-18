# core/team_normalizer.py

from core.team_mapper_PL import TeamMapperPL
from core.team_mapper_SA import TeamMapperSA

class TeamNormalizer:
    def __init__(self, league="PL"):
        self.league = league.upper()
        self.mapper = TeamMapperPL() if self.league == "PL" else TeamMapperSA()

    def normalize(self, name: str) -> str:
        if not isinstance(name, str):
            return name

        name = name.strip()

        # Mappa OddsAPI → CSV
        name = self.mapper.normalize(name)

        # Pulizia generica
        name = name.replace("FC", "").replace("AFC", "").strip()
        name = name.replace("Calcio", "").strip()
        name = name.replace("Football Club", "").strip()

        # Tutto minuscolo (TeamStatsLoader usa minuscolo)
        return name.lower()

    def normalize_match(self, match: dict) -> dict:
        m2 = match.copy()
        if "home" in m2:
            m2["home"] = self.normalize(m2["home"])
        if "away" in m2:
            m2["away"] = self.normalize(m2["away"])
        return m2

    def normalize_all_matches(self, matches: list) -> list:
        return [self.normalize_match(m) for m in matches]
