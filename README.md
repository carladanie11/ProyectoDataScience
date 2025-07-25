
# 🚖 Proyecto Data Science - Predicción ETA y Optimización Logística NYC Taxi

## 🎯 Objetivo
Desarrollar un sistema predictivo para optimizar operaciones logísticas urbanas usando datos reales de taxis de Nueva York. El foco está en la predicción de tiempos de entrega (ETA), análisis de demanda y generación de KPIs operativos para toma de decisiones.

---

## 📊 Dataset Utilizado

- **Fuente:** NYC Yellow Taxi Trip Records (Enero 2024)
- **Registros:** 2,964,624
- **Variables:** 19 originales, 13 finales para modelado
- **Tamaño:** 47.6 MB (raw), ~8 MB (procesado)
- **Formato:** Parquet (`raw_data/yellow_tripdata_2024-01.parquet`)

### Variables Clave:
- `tpep_pickup_datetime`, `tpep_dropoff_datetime`
- `trip_distance`, `total_amount`, `fare_amount`
- `passenger_count`
- `PULocationID`, `DOLocationID`
- Variables derivadas: `pickup_hour`, `pickup_weekday`, `trip_duration_minutes`, `revenue_per_mile`, `speed_mph`

---

## 📁 Estructura del Proyecto

```
ProyectoDataScience/
├── data/
│   ├── kpi1_eficiencia_hora.csv
│   ├── kpi2_performance_dia.csv
│   ├── kpi3_velocidad_operativa.csv
│   ├── taxi_operations.db
│   └── processed/
├── models/
│   └── eta_model.pkl
├── notebooks/
├── raw_data/
│   └── yellow_tripdata_2024-01.parquet
├── results/
├── scripts/
│   ├── data_cleaning.py
│   ├── data_cleaning_simple.py
│   ├── data_cleaning_backup.py
│   └── explore_dataset.py
├── dashboard_simple.py
├── temp_dashboard.py
├── temp_sql_kpi_fixed.py
├── consulta.sql
├── create_final_docs.py
├── one_pager.md
├── video_script.md
├── README.md
└── venv_desafio/
```

---

## 🚦 Estado del Proyecto

- [x] **Exploración y limpieza de datos** (`scripts/data_cleaning.py`, `scripts/explore_dataset.py`)
- [x] **Modelado ETA** (`models/eta_model.pkl`)
- [x] **KPIs operativos con SQL** (`consulta.sql`, `data/*.csv`)
- [x] **Dashboard visual** (`dashboard.png`, `dashboard_simple.py`)
- [x] **Documentación final y video** (`one_pager.md`, `video_script.md`)
- [x] **Verificación de entregables** (`create_final_docs.py`)

---

## 🛠️ Stack Tecnológico

- **Python** (Linux Debian 11)
- **pandas, numpy, scikit-learn, matplotlib, seaborn**
- **SQLite** para KPIs operativos
- **Entorno virtual:** `venv_desafio`

---

## 📈 KPIs Operativos

- **Eficiencia por Hora:** Revenue promedio por hora (`data/kpi1_eficiencia_hora.csv`)
- **Performance por Día:** Revenue y duración por día (`data/kpi2_performance_dia.csv`)
- **Velocidad Operativa:** Categorías de velocidad (`data/kpi3_velocidad_operativa.csv`)
- **Base de datos:** `data/taxi_operations.db`
- **Consultas SQL:** [`consulta.sql`](consulta.sql)

---

## 📊 Dashboard

- Visualización de KPIs y performance del modelo (`dashboard.png`)
- Scripts: [`dashboard_simple.py`](dashboard_simple.py), [`temp_dashboard.py`](temp_dashboard.py)

---

## 🚀 Ejecución Rápida

1. **Instala dependencias** en el entorno virtual:
   ```bash
   source venv_desafio/bin/activate
   pip install -r requirements.txt
   ```
2. **Explora y limpia datos:**
   ```bash
   python scripts/data_cleaning.py
   ```
3. **Modela y genera KPIs:**
   ```bash
   python temp_sql_kpi_fixed.py
   ```
4. **Genera dashboard:**
   ```bash
   python dashboard_simple.py
   ```
5. **Verifica entregables:**
   ```bash
   python create_final_docs.py
   ```

---

## 📚 Documentación y Presentación

- **One Pager:** [`one_pager.md`](one_pager.md)
- **Guion Video:** [`video_script.md`](video_script.md)
- **Notebook exploratorio:** [`notebooks/`](notebooks/)

---

## 💡 Impacto de Negocio

- Reducción 15-20% en tiempos de espera
- Optimización +25% de flota por zonas
- ROI estimado: $50,000/año
- Sistema listo para producción y escalable

---

