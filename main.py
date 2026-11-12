import os
from src.data.pipeline import DataPipeline

def main():
    raw_path = "data/raw/spy_options.csv"
    output_path = "data/processed/spx_options_master.parquet"

    os.makedirs("data/processed", exist_ok=True)
    
    pipeline = DataPipeline(options_csv=raw_path, output_path=output_path)
    df_result = pipeline.run()

    print(f"Dataset maestro generado exitosamente:")
    print(f"  - Filas (días de mercado): {len(df_result)}")
    print(f"  - Columnas: {list(df_result.columns)}")
    print(f"  - Rango temporal: {df_result.index.min().date()} -> {df_result.index.max().date()}")

if __name__ == "__main__":
    main()