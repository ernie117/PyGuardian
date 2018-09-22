from pyguardian import PyGuardian
from manifest import InventoryManifest
from tabulate import tabulate
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    char_stats = await player.fetch_char_info()

    for idx, char in enumerate(char_stats):
        char.insert(0, "Char " + str(idx + 1))

    print(tabulate(char_stats, ["", "Light",
                                "Mobility",
                                "Resilience",
                                "Recovery",
                                "Level"],
                   tablefmt="psql"))


asyncio.run(main())
