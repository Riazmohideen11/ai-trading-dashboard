import yfinance as yf
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from agents.news_sentiment import NewsSentiment
class MarketAnalyst:
    def analyze(self, symbol):
        import yfinance as yf
        import pandas as pd

        data = yf.download(symbol, period="3mo", interval="1d")

        if data.empty:
            print("⚠️ No data fetched")
            return {"price": None, "signal": "HOLD"}

    # 🔥 FIX: Flatten columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

    # Indicators
        data['SMA_5'] = data['Close'].rolling(5).mean()
        data['SMA_20'] = data['Close'].rolling(20).mean()

        sma5 = data['SMA_5'].iloc[-1]
        sma20 = data['SMA_20'].iloc[-1]
        price = data['Close'].iloc[-1]

     # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        latest = data.iloc[-1]

        price = latest['Close']
        sma5 = latest['SMA_5']
        sma20 = latest['SMA_20']
        rsi = latest['RSI']

    # AI News Sentiment
        from agents.news_sentiment import NewsSentiment
        sentiment_agent = NewsSentiment()
        news = sentiment_agent.analyze(symbol.replace(".NS",""))

    # Handle NaN
        if pd.isna(sma5) or pd.isna(sma20):
           return {"price": float(price), "signal": "HOLD"}

    # Signal logic
        if sma5 > sma20 and rsi < 70:
            signal = "BUY"

        elif sma5 < sma20 and rsi > 30:
            signal = "SELL"

        else:
            signal = "HOLD"

        return {
          "price": float(price),
          "signal": signal,
          "news": news,
          "data": data
          
}