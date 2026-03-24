# ARCHITECTURE

## Patrón general
**Layered notebook architecture** — el notebook orquesta, los módulos ejecutan.

```
Config Layer     → config/settings.py
Business Logic   → src/{metrics, continuity, prophet_model, campaigns}.py
Execution Layer  → notebooks/Forecasting_campañas.ipynb
Data Layer       → Google Sheets (2 sheets via gspread)
```

## Flujo de datos
```
Google Sheets
    ↓ gspread
df_all_media (DataFrame crudo)
    ↓ astype(float) + filtro por campaña
filtered_df
    ↓ src/metrics.py
Análisis de métricas (ROAS, CTR, CPC, CPM, CPA)
    ↓ src/prophet_model.py
Serie temporal (ds, y) → Prophet → forecast 7 días
    ↓
Visualización (matplotlib)
```

## Módulos
- `config/settings.py` — única fuente de verdad para parámetros configurables
- `src/campaigns.py` — listas estáticas `CAMPANAS_INNOVA`, `CAMPANAS_FESA`
- `src/metrics.py` — funciones de análisis y visualización de métricas
- `src/continuity.py` — validación de continuidad temporal de campañas
- `src/prophet_model.py` — wrappers de Prophet (get_serie, entrenar, evaluar)

## Entry point
`notebooks/Forecasting_campañas.ipynb` — celda 0 clona repo e instala dependencias en Colab
