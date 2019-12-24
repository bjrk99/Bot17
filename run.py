import asyncio

from bot17 import Bot17
from secrets import token


async def main():
	bot = Bot17("!")

	try:
		await bot.start(token)
	except KeyboardInterrupt:
		await bot.logout()

if __name__ == "__main__":
	asyncio.get_event_loop().run_until_complete(main())