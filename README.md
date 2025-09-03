# Telegram Trading Bot

This project is a sample implementation of a Telegram controlled trading bot for Binance testnet.
It includes a scalping strategy, Binance integration and a simple SQLite trade log.

## Features
- Telegram bot interface using inline buttons
- Scalping strategy with multiple indicators
- Binance testnet client with safe rounding
- SQLite trade log and example backtest script

## Quick start
1. Copy `.env.example` to `.env` and fill in the variables.
2. Install requirements with `pip install -r requirements.txt`.
3. Initialize the database using `python database/init_db.py`.
4. Start the bot with `python main.py`.
5. Interact with your bot on Telegram using the authorised account.

More details are available in `RUNNING.md`.
