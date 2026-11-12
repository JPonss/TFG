import pandas as pd
import numpy as np
from src.data.base import MarketDataProvider

class DoltOptionsProcessor(MarketDataProvider):
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def fetch_data(self) -> pd.DataFrame:
        use_cols = ["date", "call_put", "bid", "ask", "vol", "delta", "gamma", "vega", "theta"]
        df_opt = pd.read_csv(self.csv_path, usecols=use_cols)

        # Conversión de tipos y limpieza de nulos
        numeric_cols = ["bid", "ask", "vol", "delta", "gamma", "vega", "theta"]
        for col in numeric_cols:
            df_opt[col] = pd.to_numeric(df_opt[col], errors="coerce")
        df_opt = df_opt.dropna(subset=["date", "vol", "delta"])

        # Segmentación por moneyness usando Delta
        atm_calls = df_opt[(df_opt["call_put"] == "Call") & (df_opt["delta"].between(0.40, 0.60))]
        atm_puts  = df_opt[(df_opt["call_put"] == "Put")  & (df_opt["delta"].between(-0.60, -0.40))]
        otm_puts  = df_opt[(df_opt["call_put"] == "Put")  & (df_opt["delta"].between(-0.30, -0.10))]
        otm_calls = df_opt[(df_opt["call_put"] == "Call") & (df_opt["delta"].between(0.10, 0.30))]

        # Agregación por fecha
        daily_atm_c = atm_calls.groupby("date")["vol"].mean().rename("IV_ATM_Call")
        daily_atm_p = atm_puts.groupby("date")["vol"].mean().rename("IV_ATM_Put")
        daily_otm_p = otm_puts.groupby("date")["vol"].mean().rename("IV_OTM_Put")
        daily_otm_c = otm_calls.groupby("date")["vol"].mean().rename("IV_OTM_Call")

        daily_greeks = df_opt.groupby("date").agg(
            IV_Mean=("vol", "mean"),
            Gamma_Mean=("gamma", "mean"),
            Vega_Mean=("vega", "mean"),
            Theta_Mean=("theta", "mean")
        )

        res = pd.concat([daily_atm_c, daily_atm_p, daily_otm_p, daily_otm_c, daily_greeks], axis=1)
        res["IV_Skew_Put_Call"] = res["IV_OTM_Put"] - res["IV_ATM_Call"]
        res.index = pd.to_datetime(res.index)
        return res.sort_index()


        