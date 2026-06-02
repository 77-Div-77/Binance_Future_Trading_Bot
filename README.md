# Binance Futures Testnet Trading Bot

A Python CLI application that places **Market** and **Limit** orders on the **Binance Futures Testnet (USDT-M)**.
Built with clean layered architecture, comprehensive logging, and a rich terminal UX powered by [argparse](https://docs.python.org/3/library/argparse.html) and [Rich](https://rich.readthedocs.io/).

---

## Requirements

- Python 3.8+
- A [Binance Futures Testnet](https://testnet.binancefuture.com) account with API credentials

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py         # Package marker
│   ├── logging_config.py   # Logging setup (file + console handlers)
│   ├── client.py           # Binance API layer (Testnet client wrapper)
│   ├── validators.py       # Input validation (symbol, side, type, qty, price)
│   ├── orders.py           # Business logic (orchestrates validation + client)
│   └── cli.py              # CLI entry point (argparse + Rich)
├── logs/
│   └── bot_activity.log    # Auto-generated on first run
├── .env                    # API credentials (NOT committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd trading_bot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Create a `.env` file in the project root:

```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_key_here
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## How to Run

All commands are run from the project root.

### Market Order (BUY)

```bash
python -m bot.cli BTCUSDT BUY MARKET 0.01
```

### Limit Order (SELL)

```bash
python -m bot.cli BTCUSDT SELL LIMIT 0.01 --price 90000
```

### View help

```bash
python -m bot.cli --help
```

---

## CLI Reference

```
Usage: python -m bot.cli [SYMBOL] [SIDE] [ORDER_TYPE] [QUANTITY] [OPTIONS]

Arguments:
  SYMBOL      Trading pair, e.g. BTCUSDT        [required]
  SIDE        BUY or SELL                        [required]
  ORDER_TYPE  MARKET or LIMIT                    [required]
  QUANTITY    Quantity to trade (must be > 0)    [required]

Options:
  -p, --price FLOAT   Limit price (required for LIMIT orders)
  --help              Show this message and exit.
```

---

## Output Example

A successful order displays:

1. **Order Request Summary** table (what you submitted)
2. **Order Response Details** table (orderId, status, executedQty, avgPrice, symbol, side, type)
3. A colour-coded success/failure panel

Errors are categorised by type:
- ⚠️ Validation errors (bad input — caught before hitting the API)
- 🔴 API errors (Binance returned an error code)
- 📡 Network errors (connectivity issues)

---

## Logging

All activity is written to `logs/bot_activity.log`:

| Level   | What is logged |
|---------|---------------|
| INFO    | Client init, full API request params, full API response |
| WARNING | Input validation failures |
| ERROR   | Binance API exceptions, unexpected network errors |

Log format:
```
2025-01-15 14:32:01 | INFO     | Initializing Binance Futures Testnet Client.
2025-01-15 14:32:01 | INFO     | Sending API Request: futures_create_order with params: {...}
2025-01-15 14:32:02 | INFO     | API Response Received: {...}
```

---

## Assumptions

- **GTC (Good Till Canceled)** is used as the default `timeInForce` for all LIMIT orders.
- The user has sufficient Testnet USDT balance to cover the order.
- The Testnet API keys are for **Binance Futures Testnet** (`testnet.binancefuture.com`), not the spot testnet.
- Quantity precision follows Binance's contract spec for the chosen symbol; invalid precision will result in a Binance API error.

---

## Bonus Feature

✅ **Enhanced CLI UX** — argparse with Rich formatting:
- Colour-coded BUY/SELL sides (green/red)
- Spinner during API call
- Structured request & response tables with borders
- Icon-prefixed error panels categorised by error type (validation / API / network)
- Exit code `1` on failure (shell-script-friendly)
