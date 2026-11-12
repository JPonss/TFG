import pandas as pd
import numpy as np
import yfinance as yf
from src.data.base import MarketDataProvider

class YahooIndexProvider(MarketDataProvider):
    def __init__(self, index_ticker: str = "^GSPC", vix_ticker: str = "^VIX", 
                 start_date: str = "2019-01-01", end_date: str = "2025-12-31"):
        self.index_ticker = index_ticker
        self.vix_ticker = vix_ticker
        self.start_date = start_date
        self.end_date = end_date

    def fetch_data(self) -> pd.DataFrame:
        tickers = [self.index_ticker, self.vix_ticker]
        data = yf.download(tickers, start=self.start_date, end=self.end_date, progress=False)

        # Tratar multiíndice de Yahoo Finance
        if isinstance(data.columns, pd.MultiIndex):
            close = data["Close"]
        else:
            close = data[["Close"]]

        df = pd.DataFrame(index=close.index)
        df["SPX_Close"] = close[self.index_ticker]
        df["VIX_Close"] = close[self.vix_ticker] / 100.0  # Normalizado a tanto por uno

        # Ratios de precio y volatilidad realizada
        df["SPX_Return"] = df["SPX_Close"].pct_change()
        df["HV_20D"] = df["SPX_Return"].rolling(20).std() * np.sqrt(252)
        df["Price_to_SMA20"] = df["SPX_Close"] / df["SPX_Close"].rolling(20).mean()
        df["Price_to_SMA50"] = df["SPX_Close"] / df["SPX_Close"].rolling(50).mean()

        return df.dropna()