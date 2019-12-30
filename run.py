import asyncio
import asyncpg

from bot17 import Bot17
import secrets


async def main():
	pool = await asyncpg.create_pool(**secrets.sql)
	bot = Bot17(pool=pool)

	await bot.start(secrets.token)

if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())