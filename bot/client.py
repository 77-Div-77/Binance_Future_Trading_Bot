import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import logger
from dotenv import load_dotenv

load_dotenv()

# Binance Futures Testnet API base
FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"


class BinanceFuturesClient:
    def __init__(self):
        # .strip() removes any accidental whitespace or CRLF from the .env file
        api_key    = (os.getenv("BINANCE_API_KEY")    or "").strip()
        api_secret = (os.getenv("BINANCE_API_SECRET") or "").strip()

        if not api_key or not api_secret:
            logger.error("API credentials missing in .env file.")
            raise ValueError("Missing API keys. Please check your .env file.")

        logger.info("Initializing Binance Futures Testnet Client.")

        # testnet=False → python-binance will NEVER call testnet.binance.vision
        # We then manually point FUTURES_URL at the Futures Testnet ourselves.
        # This gives us python-binance's proven HMAC signing without any
        # unwanted connections to the unreliable Spot Testnet host.
        self.client = Client(api_key, api_secret, testnet=False)
        self.client.FUTURES_URL = FUTURES_TESTNET_URL

        logger.info("Futures URL set to: %s", self.client.FUTURES_URL)

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None,
    ) -> dict:
        """Place a USDT-M Futures order on the Binance Futures Testnet."""
        try:
            params = {
                "symbol":   symbol,
                "side":     side,
                "type":     order_type,
                "quantity": quantity,
            }

            if order_type == "LIMIT":
                params["timeInForce"] = "GTC"
                params["price"]       = price

            logger.info("Sending API Request: futures_create_order | params: %s", params)
            response = self.client.futures_create_order(**params)
            logger.info("API Response Received: %s", response)
            return response

        except BinanceAPIException as e:
            logger.error("Binance API Error: %s (Code: %s)", e.message, e.code)
            raise e
        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            raise e
