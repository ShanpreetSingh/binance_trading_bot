# Binance Futures Trading Bot

## Features
- Place Market & Limit Orders (Buy/Sell)
- Binance Futures Testnet Integration
- Command-Line Interface (CLI)
- Input Validation
- Error Handling
- Logging (API requests, responses, errors)
- Advanced Order Types (Stop-Limit, OCO)
- Order Management (Cancel, Check Status)
- Account Information (Balances, Positions)

## Prerequisites
- Python 3.8+
- Binance Testnet Account
- API Key & Secret

## Installation

git clone https://github.com/yourusername/binance-trading-bot.git
cd binance-trading-bot
pip install -r requirements.txt


## Configuration
Create `.env` file:

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret


## Usage

python main.py


### CLI Menu Options
1. Place New Order
2. Check Order Status
3. Cancel Order
4. View Account Info
5. Exit

## Order Types
| Type        | Description                      | Parameters                     |
|-------------|----------------------------------|--------------------------------|
| Market      | Instant execution                | symbol, side, quantity         |
| Limit       | Execute at specific price        | symbol, side, quantity, price  |
| Stop-Limit  | Trigger at stop price            | symbol, side, quantity, price, stop_price |
| OCO         | One-Cancels-Other order          | symbol, side, quantity, price, stop_price, stop_limit_price |

## Project Structure

binance-trading-bot/
├── bot/
│   ├── core.py
│   ├── order_types.py
│   ├── utils.py
│   └── exceptions.py
├── cli/
│   ├── interface.py
│   └── prompts.py
├── logs/
├── tests/
├── main.py
├── config.json
└── requirements.txt


