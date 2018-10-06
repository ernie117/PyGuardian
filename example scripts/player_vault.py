from pyguardian import PyGuardian
from manifest import InventoryManifest
from operator import itemgetter
from tabulate import tabulate
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    item_hashes = await player.fetch_vault()

    player_vault = InventoryManifest(item_hashes)

    item_info = player_vault.get_items()

    sort_prompt = input("Sort vault items? ")

    if sort_prompt.startswith('y'):
        try:
            sorter = input("Sort by name=0, type=1 or tier=2? ")
            sorter = int(sorter)

            item_info = sorted(item_info, key=itemgetter(sorter))

            print(tabulate(item_info, ["Name", "Type", "Tier"],
                           tablefmt="psql"))

        except ValueError:
            print("Must enter an integer!")
    else:
        print(tabulate(item_info, ["Name", "Type", "Tier"],
                       tablefmt="psql"))


if __name__ == "__main__":
    asyncio.run(main())
