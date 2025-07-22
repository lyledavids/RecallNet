import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RECALL_API_KEY")
BASE_URL = "https://api.sandbox.competitions.recall.network"
ENDPOINT = f"{BASE_URL}/api/trade/execute"

# ✅ Reputable ERC-20 Tokens (Ethereum Mainnet)
REPUTABLE_TOKENS = {
    "USDC":  "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "DAI":   "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "USDT":  "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "WETH":  "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "WBTC":  "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
    "LINK":  "0x514910771AF9Ca656af840dff83E8264EcF986CA",
    "UNI":   "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    "AAVE":  "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DdAE9"
}


def execute_trade(from_token: str, to_token: str, amount: str, reason: str = "CLI Trade"):
    payload = {
        "fromToken": from_token,
        "toToken": to_token,
        "amount": amount,
        "reason": reason
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"\n⏳ Submitting trade from {from_token} → {to_token} for {amount} units")
    resp = requests.post(ENDPOINT, json=payload, headers=headers, timeout=30)

    if resp.ok:
        print("✅ Trade executed:", resp.json())
    else:
        print("❌ Error", resp.status_code, resp.text)


def trade_between_tokens(amount: str, from_symbol: str, to_symbol: str):
    if from_symbol not in REPUTABLE_TOKENS or to_symbol not in REPUTABLE_TOKENS:
        print("❌ One or both tokens are not in the reputable list.")
        print("Available tokens:", ", ".join(REPUTABLE_TOKENS.keys()))
        return

    from_token = REPUTABLE_TOKENS[from_symbol]
    to_token = REPUTABLE_TOKENS[to_symbol]

    execute_trade(from_token, to_token, amount, reason=f"{from_symbol} to {to_symbol}")


def trade_to_custom_token(amount: str, from_symbol: str, to_address: str):
    print(f"\n🔍 Preparing custom trade: {amount} {from_symbol} → {to_address}")

    if from_symbol not in REPUTABLE_TOKENS:
        print(f"❌ '{from_symbol}' is not in the reputable token list.")
        print("✔️  Valid options:", ", ".join(REPUTABLE_TOKENS.keys()))
        return

    if not (to_address.startswith("0x") and len(to_address) == 42):
        print(f"❌ Invalid ERC-20 address: {to_address}")
        return

    from_token = REPUTABLE_TOKENS[from_symbol]
    execute_trade(from_token, to_address, amount, reason=f"{from_symbol} to custom ERC20")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python3 recall_trade.py trade-list <amount> <FROM> <TO>")
        print("  python3 recall_trade.py trade-custom <amount> <FROM> <TO_ADDRESS>")
        print("\nExamples:")
        print("  python3 recall_trade.py trade-list 100 USDC WETH")
        print("  python3 recall_trade.py trade-custom 0.01 DAI 0xYourTokenAddressHere")
        sys.exit(1)

    command = sys.argv[1]

    if command == "trade-list":
        if len(sys.argv) != 5:
            print("❌ Usage: python3 recall_trade.py trade-list <amount> <FROM> <TO>")
            sys.exit(1)
        amount = sys.argv[2]
        from_symbol = sys.argv[3].upper()
        to_symbol = sys.argv[4].upper()
        trade_between_tokens(amount, from_symbol, to_symbol)

    elif command == "trade-custom":
        if len(sys.argv) != 5:
            print("❌ Usage: python3 recall_trade.py trade-custom <amount> <FROM> <TO_ADDRESS>")
            sys.exit(1)
        amount = sys.argv[2]
        from_symbol = sys.argv[3].upper()
        to_address = sys.argv[4]
        trade_to_custom_token(amount, from_symbol, to_address)

    else:
        print("❌ Unknown command:", command)
