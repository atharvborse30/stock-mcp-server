from fastmcp import FastMCP
import yfinance as yf
import pandas as pd

# Create MCP server
mcp = FastMCP(name="Stock Analysis Server")


# 📈 Tool 1: Get stock price
@mcp.tool
def get_stock_price(symbol: str) -> float:
    """Get latest stock price"""
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    return float(data["Close"].iloc[-1])


# 📊 Tool 2: Moving Average
@mcp.tool
def moving_average(symbol: str, window: int = 5) -> float:
    """Calculate moving average"""
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")
    ma = data["Close"].rolling(window=window).mean()
    return float(ma.iloc[-1])


# 🤖 Tool 3: Simple trading signal
@mcp.tool
def trading_signal(symbol: str) -> str:
    """Basic buy/sell signal using MA"""
    stock = yf.Ticker(symbol)
    data = stock.history(period="1mo")

    short_ma = data["Close"].rolling(window=5).mean().iloc[-1]
    long_ma = data["Close"].rolling(window=20).mean().iloc[-1]

    if short_ma > long_ma:
        return "BUY"
    else:
        return "SELL"


# 🚀 Run as remote server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)