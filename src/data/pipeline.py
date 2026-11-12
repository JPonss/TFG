import pandas as pd
from src.data.yfinance_source import YahooIndexProvider
from src.data.dolt_source import DoltOptionsProcessor

class DataPipeline:
    def __init__(self, options_csv: str, output_path: str):
        self.options_processor = DoltOptionsProcessor(options_csv)
        self.output_path = output_path

    def run(self) -> pd.DataFrame:
        print("1. Procesando cadena de opciones de DoltHub...")
        df_options = self.options_processor.fetch_data()
        
        print("2. Descargando datos del índice SPX y VIX desde Yahoo Finance...")
        start_date = df_options.index.min().strftime("%Y-%m-%d")
        end_date = (df_options.index.max() + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        
        index_provider = YahooIndexProvider(start_date=start_date, end_date=end_date)
        df_index = index_provider.fetch_data()

        print("3. Integrando series temporales por fecha...")
        master_df = df_index.join(df_options, how="inner")
        
        master_df["VRP"] = master_df["IV_ATM_Call"] - master_df["HV_20D"]
        master_df = master_df.dropna()

        print(f"4. Guardando dataset procesado en: {self.output_path}")
        master_df.to_parquet(self.output_path, engine="pyarrow")
        return master_df