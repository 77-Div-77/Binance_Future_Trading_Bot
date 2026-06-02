import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.rule import Rule
from bot.orders import execute_trade

console = Console()

# ── Helpers ────────────────────────────────────────────────────────────────────

def _print_header() -> None:
    console.print()
    console.print(Rule("[bold cyan]Binance Futures Testnet Trading Bot[/bold cyan]", style="cyan"))
    console.print()


def _print_request_summary(symbol, side, order_type, quantity, price) -> None:
    table = Table(
        title="[bold cyan]📋  Order Request Summary[/bold cyan]",
        show_header=True,
        header_style="bold white on blue",
        border_style="cyan",
        show_lines=True,
    )
    table.add_column("Symbol",   style="bold yellow",  justify="center")
    table.add_column("Side",     style="bold",         justify="center")
    table.add_column("Type",     style="bold magenta", justify="center")
    table.add_column("Quantity", style="cyan",         justify="right")
    table.add_column("Price",    style="green",        justify="right")

    side_styled = f"[bold green]{side}[/bold green]" if side == "BUY" else f"[bold red]{side}[/bold red]"
    price_str   = f"[green]{price:,.2f}[/green]" if price else "[dim]N/A[/dim]"

    table.add_row(symbol, side_styled, order_type, f"{quantity:g}", price_str)
    console.print(table)
    console.print()


def _print_success(data: dict) -> None:
    console.print(Panel("[bold green]✅  Order Placed Successfully![/bold green]",
                        border_style="green", expand=False))
    console.print()

    table = Table(
        title="[bold green]📊  Order Response Details[/bold green]",
        show_header=True,
        header_style="bold white on dark_green",
        border_style="green",
        show_lines=True,
    )
    table.add_column("Order ID",     style="bold yellow", justify="center")
    table.add_column("Status",       style="bold green",  justify="center")
    table.add_column("Executed Qty", style="cyan",        justify="right")
    table.add_column("Avg Price",    style="green",       justify="right")
    table.add_column("Symbol",       style="yellow",      justify="center")
    table.add_column("Side",         style="bold",        justify="center")
    table.add_column("Type",         style="magenta",     justify="center")

    side_val  = data.get("side", "N/A")
    side_col  = (f"[bold green]{side_val}[/bold green]" if side_val == "BUY"
                 else f"[bold red]{side_val}[/bold red]")
    avg_price = data.get("avgPrice", "0")
    avg_price_str = (f"{float(avg_price):,.4f}"
                     if avg_price and avg_price not in ("0", "0.00", "0.0000")
                     else "[dim]Pending[/dim]")

    table.add_row(
        str(data.get("orderId",     "N/A")),
        str(data.get("status",      "N/A")),
        str(data.get("executedQty", "N/A")),
        avg_price_str,
        str(data.get("symbol",      "N/A")),
        side_col,
        str(data.get("type",        "N/A")),
    )
    console.print(table)
    console.print()


def _print_error(message: str, error_type: str = "error") -> None:
    icons = {"validation": "⚠️ ", "api": "🔴", "network": "📡", "error": "❌"}
    icon  = icons.get(error_type, "❌")
    console.print(Panel(
        f"{icon}  [bold red]Order Failed[/bold red]\n\n[white]{message}[/white]",
        border_style="red", expand=False,
    ))
    console.print()


# ── Argument parser ────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m bot.cli",
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  Market order:  python3 -m bot.cli BTCUSDT BUY  MARKET 0.01\n"
            "  Limit  order:  python3 -m bot.cli BTCUSDT SELL LIMIT  0.01 --price 90000\n"
        ),
    )
    parser.add_argument("symbol",     help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("side",       help="BUY or SELL")
    parser.add_argument("order_type", help="MARKET or LIMIT")
    parser.add_argument("quantity",   type=float, help="Quantity to trade (must be > 0)")
    parser.add_argument("--price", "-p", type=float, default=None,
                        help="Limit price (required for LIMIT orders)")
    return parser


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = build_parser()
    args   = parser.parse_args()

    symbol     = args.symbol.upper()
    side       = args.side.upper()
    order_type = args.order_type.upper()
    quantity   = args.quantity
    price      = args.price

    _print_header()
    _print_request_summary(symbol, side, order_type, quantity, price)

    with console.status("[bold yellow]⏳  Sending order to Binance Testnet…[/bold yellow]",
                        spinner="dots"):
        result = execute_trade(symbol, side, order_type, quantity, price)

    if result["status"] == "success":
        _print_success(result["data"])
    else:
        _print_error(result["message"], result.get("error_type", "error"))
        sys.exit(1)


if __name__ == "__main__":
    main()
