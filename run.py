import asyncio
import asyncpg

from bot17 import Bot17
import secrets


async def main():
	pool = await asyncpg.create_pool(**secrets.sql)

	query = """CREATE TABLE IF NOT EXISTS guilds(
					guild_id BIGINT PRIMARY KEY,
					prefix TEXT[] NOT NULL);"""
	await pool.execute(query)

	records = await pool.fetch("SELECT * FROM guilds")
	prefixes = {r["guild_id"]: r["prefix"] for r in records}

	bot = Bot17(pool=pool, prefixes=prefixes)
	await bot.start(secrets.token)

if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())