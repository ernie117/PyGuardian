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

    weapon_hashes = await player.fetch_eq(length=7)

    weapon_names = InventoryManifest(weapon_hashes)
    weapon_names = weapon_names.get_partial_items()

    data = await player.fetch_instance_data(length=7)

    weapons = InstanceData(data)

    titles, stats = weapons.get_stats()

    final_titles = []
    for title in titles:
        if len(title) >= 6:
            new_title = ["Damage Type", "Power"] + title
            final_titles.append(new_title)
        else:
            new_title = ["Power"] + title
            final_titles.append(new_title)

    final_stats = [name + stat for name, stat in zip(weapon_names, stats)]

    for i, element in enumerate(final_stats):
        table = [element]
        print(tabulate.tabulate(table, final_titles[i], tablefmt="psql"))


if __name__ == "__main__":
    asyncio.run(main())
