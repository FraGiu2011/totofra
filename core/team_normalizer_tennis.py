from core.player_mapper_tennis import PlayerMapperTennis

class TeamNormalizerTennis:
    def __init__(self):
        self.mapper = PlayerMapperTennis()

    def normalize(self, name: str) -> str:
        if not isinstance(name, str):
            return name
        name = name.strip()
        name = self.mapper.normalize(name)
        return name.lower()

    def normalize_match(self, match: dict) -> dict:
        m2 = match.copy()
        m2["player1"] = self.normalize(m2["player1"])
        m2["player2"] = self.normalize(m2["player2"])
        return m2

    def normalize_all_matches(self, matches: list) -> list:
        return [self.normalize_match(m) for m in matches]
