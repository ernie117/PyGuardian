class GuardianProcessor:

    PLATFORMS = {"xbox": "1", "playstation": "2", "pc": "4"}

    @staticmethod
    def process(guardian, platform) -> tuple:

        # '#' in BattleID's on pc must be replaced in URLs
        return (guardian.strip().replace("#", "%23"),
                GuardianProcessor.PLATFORMS[platform.strip().lower()])

