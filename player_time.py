from pyguardian import PyGuardian
from tabulate import tabulate
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    times, total = await player.fetch_play_time()

    table = [[*times, total]]

    table_title = ["Char. " + str(i + 1)
                   for char, i in zip(player.chars, range(len(player.chars)))]

    table_title.append("Total")

    print(tabulate(table, table_title, tablefmt="psql"))


asyncio.run(main())

