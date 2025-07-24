import pandas as pd
import sys
import os

def explore_nyc_taxi():
    try:
        print("Explorando NYC Taxi Dataset desde ProyectoDataScience...")
        
        current_dir = os.getcwd()
        print(f"Directorio actual: {current_dir}")
        
        file_path = 'raw_data/yellow_tripdata_2024-01.parquet'
        if not os.path.exists(file_path):
            print(f"Archivo no encontrado: {file_path}")
            return False
        
        print(f"Archivo encontrado: {file_path}")
        file_size = os.path.getsize(file_path) / (1024*1024)
        print(f"Tamaño del archivo: {file_size:.1f} MB")
        
        print("Leyendo dataset completo...")
        df = pd.read_parquet(file_path)
        
        print(f"Dataset cargado exitosamente!")
        print(f"Forma del dataset: {df.shape}")
        print(f"Columnas disponibles:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\nTipos de datos:")
        for col, dtype in df.dtypes.items():
            print(f"   {col}: {dtype}")
        
        print(f"\nPrimeros 3 registros:")
        print(df.head(3))
        
        key_vars = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance', 'total_amount']
        
        print(f"\nVariables clave para logística:")
        for var in key_vars:
            if var in df.columns:
                print(f"   SI: {var}")
            else:
                print(f"   NO: {var}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("EXPLORACION DE DATASET")
    print("=" * 50)
    
    if explore_nyc_taxi():
        print("\nEXITO: Dataset listo para el desafío!")
    else:
        print("\nPROBLEMA: Verificar dependencias")
