from pyguardian import PyGuardian
from manifest import InventoryManifest
from operator import itemgetter
from tabulate import tabulate
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    sort_prompt = input("Sort vault items? ")
    if sort_prompt.startswith('y'):
        sorter = input("Sort by name, tier or type? ")

    player = PyGuardian(gamertag, platform)

    item_hashes = await player.fetch_vault()

    player_vault = InventoryManifest(item_hashes)

    if sorter == "name":
        item_info = player_vault.get_items()
        item_info = sorted(item_info, key=itemgetter(0))
    elif sorter == "tier":
        item_info = player_vault.get_items()
        item_info = sorted(item_info, key=itemgetter(2))
    elif sorter == "type":
        item_info = player_vault.get_items()
        item_info = sorted(item_info, key=itemgetter(1))
    else:
        print(tabulate(item_info, ["Name", "Type", "Tier"],
                       tablefmt="psql"))
        sys.exit()

    print(tabulate(item_info, ["Name", "Type", "Tier"],
                   tablefmt="psql"))


asyncio.run(main())
