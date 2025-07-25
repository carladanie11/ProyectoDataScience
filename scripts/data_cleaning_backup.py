import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data_efficiently():
    """Cargar datos de manera eficiente para RAM limitada"""
    print("🔄 Cargando dataset NYC Taxi...")
    
    file_path = 'raw_data/yellow_tripdata_2024-01.parquet'
    
    # Definir tipos de datos para optimizar memoria
    dtypes = {
        'VendorID': 'int8',
        'passenger_count': 'int8', 
        'RatecodeID': 'int8',
        'store_and_fwd_flag': 'category',
        'PULocationID': 'int16',
        'DOLocationID': 'int16',
        'payment_type': 'int8',
        'trip_distance': 'float32',
        'fare_amount': 'float32',
        'extra': 'float32',
        'mta_tax': 'float32',
        'tip_amount': 'float32',
        'tolls_amount': 'float32',
        'improvement_surcharge': 'float32',
        'total_amount': 'float32',
        'congestion_surcharge': 'float32',
        'Airport_fee': 'float32'
    }
    
    # Cargar datos
    df = pd.read_parquet(file_path)
    
    # Aplicar optimización de tipos
    for col, dtype in dtypes.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)
    
    print(f"✅ Datos cargados: {df.shape}")
    print(f"💾 Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    return df

def clean_data(df):
    """Limpiar y validar datos"""
    print("\n🧹 Iniciando limpieza de datos...")
    
    initial_rows = len(df)
    
    # 1. Eliminar filas con valores nulos en columnas críticas
    critical_cols = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 
                    'trip_distance', 'total_amount']
    
    print(f"📊 Valores nulos por columna crítica:")
    for col in critical_cols:
        null_count = df[col].isnull().sum()
        print(f"   {col}: {null_count:,}")
    
    df = df.dropna(subset=critical_cols)
    print(f"✅ Filas después de eliminar nulos: {len(df):,}")
    
    # 2. Filtrar valores lógicos
    print(f"\n🎯 Aplicando filtros de calidad...")
    
    # Distancia positiva y realista (< 100 millas)
    df = df[(df['trip_distance'] > 0) & (df['trip_distance'] < 100)]
    
    # Duración de viaje realista (1 min a 3 horas)
    df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    df = df[(df['trip_duration'] >= 1) & (df['trip_duration'] <= 180)]
    
    # Total amount positivo y realista (< $500)
    df = df[(df['total_amount'] > 0) & (df['total_amount'] < 500)]
    
    # Número de pasajeros realista
    df['passenger_count'] = df['passenger_count'].fillna(1)
    df = df[(df['passenger_count'] >= 1) & (df['passenger_count'] <= 6)]
    
    print(f"✅ Filas después de filtros: {len(df):,}")
    print(f"📉 Registros eliminados: {initial_rows - len(df):,} ({((initial_rows - len(df))/initial_rows)*100:.1f}%)")
    
    return df

def create_features(df):
    """Crear variables derivadas para modelado"""
    print("\n⚙️ Creando features para modelado...")
    
    # Variables temporales
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    df['pickup_day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
    df['pickup_day'] = df['tpep_pickup_datetime'].dt.day
    
    # Variables de negocio
    df['revenue_per_mile'] = df['total_amount'] / (df['trip_distance'] + 0.01)
    df['revenue_per_minute'] = df['total_amount'] / (df['trip_duration'] + 0.01)
    df['speed_mph'] = (df['trip_distance'] / (df['trip_duration'] / 60)).round(2)
    
    # Categorías de tiempo
    df['time_category'] = pd.cut(df['pickup_hour'], 
                                bins=[0, 6, 12, 18, 24], 
                                labels=['Night', 'Morning', 'Afternoon', 'Evening'])
    
    # Categorías de distancia
    df['distance_category'] = pd.cut(df['trip_distance'],
                                   bins=[0, 2, 5, 10, float('inf')],
                                   labels=['Short', 'Medium', 'Long', 'Very_Long'])
    
    print(f"✅ Features creadas:")
    new_features = ['pickup_hour', 'pickup_day_of_week', 'trip_duration', 
                   'revenue_per_mile', 'speed_mph', 'time_category', 'distance_category']
    for feature in new_features:
        print(f"   📈 {feature}")
    
    return df

def save_clean_data(df):
    """Guardar datos limpios"""
    print(f"\n💾 Guardando datos limpios...")
    
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Guardar en formato parquet (más eficiente)
    output_path = 'data/cleaned_taxi_data.parquet'
    df.to_parquet(output_path, index=False)
    
    # Guardar muestra en CSV para inspección manual
    sample_path = 'data/data_sample.csv'
    df.sample(1000).to_csv(sample_path, index=False)
    
    file_size = os.path.getsize(output_path) / (1024**2)
    print(f"✅ Datos guardados en: {output_path}")
    print(f"📦 Tamaño final: {file_size:.1f} MB")
    print(f"📊 Registros finales: {len(df):,}")
    
    return output_path

def generate_data_summary(df):
    """Generar resumen de calidad de datos"""
    print(f"\n📋 RESUMEN DE LIMPIEZA DE DATOS")
    print("="*50)
    
    print(f"📊 Dataset final:")
    print(f"   Registros: {len(df):,}")
    print(f"   Columnas: {len(df.columns)}")
    print(f"   Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    print(f"\n🎯 Variables clave - Estadísticas:")
    key_vars = ['trip_distance', 'trip_duration', 'total_amount', 'speed_mph']
    for var in key_vars:
        if var in df.columns:
            print(f"   {var}:")
            print(f"     Media: {df[var].mean():.2f}")
            print(f"     Min: {df[var].min():.2f}")
            print(f"     Max: {df[var].max():.2f}")
    
    print(f"\n📅 Rango temporal:")
    print(f"   Desde: {df['tpep_pickup_datetime'].min()}")
    print(f"   Hasta: {df['tpep_pickup_datetime'].max()}")
    
    return True

if __name__ == "__main__":
    print("🚀 LIMPIEZA DE DATOS - NYC TAXI DATASET")
    print("="*60)
    
    try:
        # 1. Cargar datos
        df = load_data_efficiently()
        
        # 2. Limpiar datos
        df_clean = clean_data(df)
        
        # 3. Crear features
        df_final = create_features(df_clean)
        
        # 4. Guardar datos limpios
        output_path = save_clean_data(df_final)
        
        # 5. Generar resumen
        generate_data_summary(df_final)
        
        print(f"\n🎉 ¡LIMPIEZA COMPLETADA EXITOSAMENTE!")
        print(f"✅ Datos listos para modelado en: {output_path}")
        
    except Exception as e:
        print(f"❌ Error en limpieza: {e}")
        import traceback
        traceback.print_exc()
