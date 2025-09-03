"""Entry point for the Telegram trading bot."""
from utils.logging_config import setup_logging
from database.init_db import init_db
from bot.telegram_bot import run_bot


def main() -> None:
    """Initialize logging, database and start the telegram bot."""
    setup_logging()
    init_db()
    run_bot()


if __name__ == "__main__":
    main()
