class TableFormatter:
    def __init__(self, titles):
        self.titles = titles

        self.sizes = {
                "Rounds Per Minute": 17,
                "Power": 17,
                "Damage Type": 17,
                "Impact": 12,
                "Charge Time": 17,
                "Range": 8,
                "Stability": 10,
                "Handling": 10,
                "Reload Speed": 13,
                "Magazine": 17,
                "Blast Radius": 12,
                "Efficiency": 10,
                "Defense": 10,
                "Ammo Capacity": 13,
                "Velocity": 7,
                "Swing Speed": 17
        }

    def format(self):

        new_titles = []
        for title in self.titles:
            if title in self.sizes:
                new_title = title + (self.sizes[title] - len(title)) * " "
                new_titles.append(new_title)

        return list(new_titles)
