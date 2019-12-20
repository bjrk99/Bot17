from bot17 import Bot17
from secrets import token


def main():
	bot = Bot17("!")
	bot.run(token)

if __name__ == "__main__":
	main()