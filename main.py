from dotenv import load_dotenv

import scraper
import bot
import os
import asyncio
import os.path

if os.path.isfile(".env"):
    load_dotenv()

if not os.path.isdir("./config"):
    os.mkdir("./config")

async def main():
    asyncio.create_task(bot.init())

    await asyncio.sleep(10)

    while True:
        if not bot.client.is_ready():
            raise SystemExit("the bot was not ready in time.")
        await scraper.parse_jobs()
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
