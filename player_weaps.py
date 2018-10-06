from pyguardian import PyGuardian
from instance_data import InstanceData
from manifest import InventoryManifest
import tabulate
import asyncio
import json


tabulate.PRESERVE_WHITESPACE = True


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    weapon_hashes = await player.fetch_eq(length=3)

    weapon_names = InventoryManifest(weapon_hashes)
    weapon_names = weapon_names.get_partial_items()

    data = await player.fetch_instance_data()

    weapons = InstanceData(data)

    titles, stats = weapons.get_stats()

    titles = [["Damage Type", "Power"] + title for title in titles]

    final_stats = [name + stat for name, stat in zip(weapon_names, stats)]

    for i, element in enumerate(final_stats):
        table = [element]
        print(tabulate.tabulate(table, titles[i], tablefmt="fancy_grid"))


if __name__ == "__main__":
    asyncio.run(main())
