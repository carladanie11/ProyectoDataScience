# Paso 4: KPI Operativo SQL - Versión Corregida
import pandas as pd
import sqlite3
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def main():
    print('🎯 PASO 4: KPI OPERATIVO CON SQL')
    print('='*60)

    try:
        # Cargar datos
        print('📊 Cargando datos limpios...')
        df = pd.read_parquet('data/processed/taxi_data_cleaned.parquet')
        print(f'✅ Datos cargados: {len(df):,} registros')
        
        # Crear conexión SQLite
        print('��️ Creando base de datos SQLite...')
        conn = sqlite3.connect('data/taxi_operations.db')
        
        # Cargar datos a SQLite
        df.to_sql('taxi_operations', conn, if_exists='replace', index=False)
        print('✅ Datos cargados en SQLite')
        
        # KPI 1: Eficiencia por Hora
        print('\n📊 KPI 1: Eficiencia Revenue por Hora')
        kpi1_query = """
        SELECT 
            pickup_hour,
            ROUND(AVG(total_amount), 2) as avg_revenue,
            ROUND(AVG(trip_distance), 2) as avg_distance,
            ROUND(AVG(total_amount/trip_distance), 2) as revenue_per_mile,
            COUNT(*) as total_trips
        FROM taxi_operations 
        WHERE trip_distance > 0
        GROUP BY pickup_hour
        ORDER BY revenue_per_mile DESC
        LIMIT 10;
        """
        
        kpi1_result = pd.read_sql_query(kpi1_query, conn)
        print(kpi1_result)
        
        # KPI 2: Performance por Día de Semana
        print('\n📊 KPI 2: Performance por Día de Semana')
        kpi2_query = """
        SELECT 
            pickup_weekday,
            CASE 
                WHEN pickup_weekday = 0 THEN 'Lunes'
                WHEN pickup_weekday = 1 THEN 'Martes'
                WHEN pickup_weekday = 2 THEN 'Miércoles'
                WHEN pickup_weekday = 3 THEN 'Jueves'
                WHEN pickup_weekday = 4 THEN 'Viernes'
                WHEN pickup_weekday = 5 THEN 'Sábado'
                WHEN pickup_weekday = 6 THEN 'Domingo'
            END as dia_nombre,
            ROUND(AVG(total_amount), 2) as avg_revenue,
            ROUND(AVG(trip_duration_minutes), 2) as avg_duration,
            COUNT(*) as total_trips
        FROM taxi_operations 
        GROUP BY pickup_weekday
        ORDER BY avg_revenue DESC;
        """
        
        kpi2_result = pd.read_sql_query(kpi2_query, conn)
        print(kpi2_result)
        
        # KPI 3: Análisis de Velocidad Operativa
        print('\n📊 KPI 3: Análisis de Velocidad Operativa')
        kpi3_query = """
        SELECT 
            CASE 
                WHEN (trip_distance/trip_duration_minutes) < 0.5 THEN 'Lento'
                WHEN (trip_distance/trip_duration_minutes) BETWEEN 0.5 AND 1.0 THEN 'Normal'
                ELSE 'Rápido'
            END as categoria_velocidad,
            ROUND(AVG(trip_distance/trip_duration_minutes), 3) as velocidad_promedio,
            ROUND(AVG(total_amount), 2) as revenue_promedio,
            COUNT(*) as cantidad_viajes,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM taxi_operations), 2) as porcentaje
        FROM taxi_operations 
        WHERE trip_duration_minutes > 0 AND trip_distance > 0
        GROUP BY categoria_velocidad
        ORDER BY velocidad_promedio DESC;
        """
        
        kpi3_result = pd.read_sql_query(kpi3_query, conn)
        print(kpi3_result)
        
        # Guardar consulta SQL final
        print('\n💾 Guardando consulta.sql...')
        final_query = f"""
-- KPI OPERATIVO PRINCIPAL: Eficiencia Operacional por Zona y Tiempo
-- Desafío Técnico Data Scientist - Sector Logístico
-- Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M")}

-- KPI 1: EFICIENCIA REVENUE POR HORA
{kpi1_query}

-- KPI 2: PERFORMANCE POR DÍA DE SEMANA  
{kpi2_query}

-- KPI 3: ANÁLISIS DE VELOCIDAD OPERATIVA
{kpi3_query}

-- KPI 4: RESUMEN EJECUTIVO
SELECT 
    'RESUMEN OPERACIONAL' as metric_name,
    ROUND(AVG(total_amount), 2) as avg_revenue_total,
    ROUND(AVG(trip_distance), 2) as avg_distance_total,
    ROUND(AVG(trip_duration_minutes), 2) as avg_duration_total,
    COUNT(*) as total_operations
FROM taxi_operations;
        """
        
        with open('consulta.sql', 'w') as f:
            f.write(final_query)
        
        print('✅ consulta.sql creado exitosamente')
        
        # Exportar KPIs a CSV para visualización
        print('\n📊 Exportando KPIs para visualización...')
        kpi1_result.to_csv('data/kpi1_eficiencia_hora.csv', index=False)
        kpi2_result.to_csv('data/kpi2_performance_dia.csv', index=False)
        kpi3_result.to_csv('data/kpi3_velocidad_operativa.csv', index=False)
        
        conn.close()
        
        print('\n🎉 PASO 4 COMPLETADO EXITOSAMENTE!')
        print('✅ Base de datos SQLite creada')
        print('✅ KPIs operativos calculados') 
        print('✅ consulta.sql generado')
        print('✅ CSVs para visualización exportados')
        print('\n🔄 Listo para Paso 5: Visualización y Dashboard')
        
    except Exception as e:
        print(f'❌ Error en KPI SQL: {str(e)}')

if __name__ == "__main__":
    main()
