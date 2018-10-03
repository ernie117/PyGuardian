from pyguardian import PyGuardian
from manifest import InventoryManifest
from tabulate import tabulate
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    item_hashes = await player.fetch_eq()

    player_items = InventoryManifest(item_hashes)

    item_info = player_items.get_items()

    print(tabulate(item_info, ["Name", "Type", "Tier"],
                   tablefmt="psql"))


if __name__ == "__main__":
    asyncio.run(main())
