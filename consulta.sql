
-- KPI OPERATIVO PRINCIPAL: Eficiencia Operacional por Zona y Tiempo
-- Desafío Técnico Data Scientist - Sector Logístico
-- Fecha: 2025-07-24 21:18

-- KPI 1: EFICIENCIA REVENUE POR HORA

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
        

-- KPI 2: PERFORMANCE POR DÍA DE SEMANA  

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
        

-- KPI 3: ANÁLISIS DE VELOCIDAD OPERATIVA

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
        

-- KPI 4: RESUMEN EJECUTIVO
SELECT 
    'RESUMEN OPERACIONAL' as metric_name,
    ROUND(AVG(total_amount), 2) as avg_revenue_total,
    ROUND(AVG(trip_distance), 2) as avg_distance_total,
    ROUND(AVG(trip_duration_minutes), 2) as avg_duration_total,
    COUNT(*) as total_operations
FROM taxi_operations;
        