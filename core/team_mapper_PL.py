# core/team_mapper_PL.py

class TeamMapperPL:
    def __init__(self):
        self.map = {
            "Arsenal": "arsenal",
            "Manchester City": "manchester city",
            "Liverpool": "liverpool",
            "Chelsea": "chelsea",
            "Tottenham Hotspur": "tottenham",
            "Aston Villa": "aston villa",
            "Newcastle United": "newcastle",
            "Brighton and Hove Albion": "brighton hove albion",
            "West Ham United": "west ham",
            "Fulham": "fulham",
            "Wolverhampton Wanderers": "wolves",
            "Bournemouth": "bournemouth",
            "Brentford": "brentford",
            "Crystal Palace": "crystal palace",
            "Nottingham Forest": "nottingham forest",
            "Burnley": "burnley",
            "Luton Town": "luton",
            "Sheffield United": "sheffield united",
            "Everton": "everton",
            "Manchester United": "manchester united"
        }

    def normalize(self, name: str) -> str:
        return self.map.get(name, name.lower())
