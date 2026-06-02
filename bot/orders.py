from bot.client import BinanceFuturesClient
from binance.exceptions import BinanceAPIException
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_limit_order,
    validate_quantity,
    validate_symbol,
)
from bot.logging_config import logger


def execute_trade(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
) -> dict:
    """
    Validate inputs, connect to Binance Futures Testnet, and place an order.

    Returns a dict with keys:
        status  : "success" | "error"
        data    : API response dict  (only on success)
        message : human-readable error string (only on error)
    """
    try:
        # ── 1. Validate all inputs before touching the network ──────────────
        validate_symbol(symbol)
        validate_side(side)
        validate_order_type(order_type)
        validate_quantity(quantity)
        validate_limit_order(order_type, price)

        # ── 2. Initialise the Binance client ─────────────────────────────────
        client = BinanceFuturesClient()

        # ── 3. Place the order ────────────────────────────────────────────────
        response = client.place_order(
            symbol=symbol.upper(),
            side=side.upper(),
            order_type=order_type.upper(),
            quantity=quantity,
            price=price,
        )
        return {"status": "success", "data": response}

    except ValueError as ve:
        # Input validation failures
        logger.warning(f"Validation failed: {ve}")
        return {"status": "error", "error_type": "validation", "message": str(ve)}

    except BinanceAPIException as ae:
        # Already logged inside client.py; surface a clean message
        return {
            "status": "error",
            "error_type": "api",
            "message": f"Binance API error (code {ae.code}): {ae.message}",
        }

    except Exception as e:
        # Network / unexpected failures — already logged in client.py
        return {"status": "error", "error_type": "network", "message": str(e)}
