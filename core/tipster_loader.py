class TipsterLoader:
    def load_tipsters(self):
        """
        Tipster avanzati (simulati).
        Ogni tipster fornisce probabilità 1X2.
        """

        tipsters = {
            "TipsterA": {"1": 0.45, "X": 0.30, "2": 0.25},
            "TipsterB": {"1": 0.40, "X": 0.32, "2": 0.28},
            "TipsterC": {"1": 0.38, "X": 0.35, "2": 0.27},
        }

        return tipsters
