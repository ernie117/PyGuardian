from pyguardian import PyGuardian
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    time_data = await player.fetch_last_time_played()

    for entry in time_data:
        print(entry)


asyncio.run(main())
