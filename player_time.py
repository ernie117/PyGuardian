from pyguardian import PyGuardian
from tabulate import tabulate
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    times, total = await player.fetch_play_time()

    if len(times) == 1:
        table = [[times[0], total]]
        print(tabulate(table, ["Char. 1", "Total"], tablefmt="psql"))
    elif len(times) == 2:
        table = [[times[0], times[1], total]]
        print(tabulate(table, ["Char. 1", "Char. 2", "Total"], tablefmt="psql"))
    else:
        table = [[times[0], times[1], times[2], total]]
        print(tabulate(table, ["Char. 1", "Char. 2", "Char. 3", "Total"], tablefmt="psql"))


asyncio.run(main())

