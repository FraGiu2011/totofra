# core/team_mapper_SA.py

class TeamMapperSA:
    def __init__(self):
        self.map = {
            "Inter Milan": "inter",
            "AC Milan": "milan",
            "AS Roma": "roma",
            "SS Lazio": "lazio",
            "Atalanta BC": "atalanta",
            "Napoli": "napoli",
            "Juventus": "juventus",
            "Fiorentina": "fiorentina",
            "Bologna": "bologna",
            "Torino FC": "torino",
            "Genoa CFC": "genoa",
            "US Lecce": "lecce",
            "Udinese Calcio": "udinese",
            "Cagliari Calcio": "cagliari",
            "Hellas Verona": "hellas verona",
            "Frosinone Calcio": "frosinone",
            "US Sassuolo Calcio": "sassuolo",
            "Empoli FC": "empoli",
            "US Salernitana 1919": "salernitana",
            "AC Monza": "monza"
        }

    def normalize(self, name: str) -> str:
        return self.map.get(name, name.lower())
