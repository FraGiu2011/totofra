class PlayerMapperTennis:
    def __init__(self):
        self.map = {
            "N. Djokovic": "novak djokovic",
            "Novak Djokovic": "novak djokovic",
            "R. Nadal": "rafael nadal",
            "Rafael Nadal": "rafael nadal",
            "C. Alcaraz": "carlos alcaraz",
            "Carlos Alcaraz": "carlos alcaraz",
            "J. Sinner": "jannik sinner",
            "Jannik Sinner": "jannik sinner",
        }

    def normalize(self, name: str) -> str:
        return self.map.get(name, name.lower().strip())
