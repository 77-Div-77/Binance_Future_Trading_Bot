VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_side(side: str) -> bool:
    """Validate that side is BUY or SELL."""
    if side.upper() not in VALID_SIDES:
        raise ValueError(f"Invalid side '{side}'. Must be one of: {', '.join(VALID_SIDES)}")
    return True


def validate_order_type(order_type: str) -> bool:
    """Validate that order_type is MARKET or LIMIT."""
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type '{order_type}'. Must be one of: {', '.join(VALID_ORDER_TYPES)}")
    return True


def validate_limit_order(order_type: str, price: float) -> bool:
    """Validate that LIMIT orders include a valid positive price."""
    if order_type.upper() == "LIMIT" and (price is None or price <= 0):
        raise ValueError("LIMIT orders require a valid, positive --price value.")
    return True


def validate_quantity(quantity: float) -> bool:
    """Validate that quantity is a positive number."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return True


def validate_symbol(symbol: str) -> bool:
    """Validate that symbol is a non-empty alphanumeric string."""
    if not symbol or not symbol.isalnum():
        raise ValueError(f"Invalid symbol '{symbol}'. Must be alphanumeric (e.g., BTCUSDT).")
    return True
