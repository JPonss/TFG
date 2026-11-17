import os
import pandas as pd
from src.data.pipeline import DataPipeline
from src.genetic.motor_evolutivo import run_genetic_pipeline

def main():
    raw_path = "data/raw/spy_options.csv"
    output_path = "data/processed/spx_options_master.parquet"

    os.makedirs("data/processed", exist_ok=True)
    
    # 1. Pipeline de Ingesta y Procesamiento de Datos
    if not os.path.exists(output_path):
        print("Ejecutando pipeline de datos...")
        pipeline = DataPipeline(options_csv=raw_path, output_path=output_path)
        df_master = pipeline.run()
    else:
        print(f"Cargando dataset maestro procesado desde: {output_path}")
        df_master = pd.read_parquet(output_path)

    print(f"Dataset listo. Filas: {len(df_master)} | Columnas: {list(df_master.columns)}")

    # 2. Ejecutar el Motor Evolutivo de Programación Genética
    print("\nIniciando el motor de Programación Genética...")
    best_tree = run_genetic_pipeline(df_master, n_generations=5, pop_size=30)

if __name__ == "__main__":
    main()