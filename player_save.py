from pyguardian import PyGuardian
import asyncio


async def main():
    gamertag = input("Enter gamertag: ")
    platform = input("Enter platform: ")

    player = PyGuardian(gamertag, platform)

    await player.write_data()

    print("Player data written to JSON \u2713")


if __name__ == "__main__":
    asyncio.run(main())
