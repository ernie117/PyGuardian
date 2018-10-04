from pyguardian import PyGuardian
from instance import InstanceData
from manifest import InventoryManifest
from tabulate import tabulate
import asyncio
import json


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    data = await player.fetch_instance_data()

    player = InstanceData(data)

    stats = player.get_stats()

if __name__ == "__main__":
    asyncio.run(main())
