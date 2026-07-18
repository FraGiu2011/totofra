class DataCleanerTennis:
    def clean(self, matches):
        cleaned = []
        for m in matches:
            if "odds" not in m:
                continue
            if "1" not in m["odds"] or "2" not in m["odds"]:
                continue
            cleaned.append(m)
        return cleaned
