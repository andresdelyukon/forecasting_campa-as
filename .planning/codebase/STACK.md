# STACK

## Language & Runtime
- **Language**: Python 3.x
- **Execution Environment**: Google Colab (Jupyter-based), compatible con VS Code + Jupyter
- **Package Manager**: pip

## Core Frameworks & Libraries

| Librería | Uso |
|----------|-----|
| `pandas` | Manipulación de datos, agregaciones, groupby |
| `numpy` | Cálculos numéricos, manejo de inf/nan |
| `prophet` | Forecasting de series temporales (Meta) |
| `matplotlib` | Visualizaciones (línea, boxplot, histograma) |
| `gspread` | Cliente de Google Sheets API |
| `google-auth` | Autenticación OAuth con Google |

## Configuración centralizada
`config/settings.py` — única fuente de verdad:
- IDs de Google Sheets
- Rango de fechas por defecto (`FECHA_INICIO`, `FECHA_FIN`)
- Parámetros de Prophet (`CHANGEPOINT_PRIOR_SCALE=0.5`, `FORECAST_HORIZON_DAYS=7`)
- Eventos especiales/holidays (Hot Sale, Hot Fashion)
- Columnas numéricas del sheet

## Flujo de datos
```
Google Sheets (gspread)
  ↓
pandas DataFrame (df_all_media)
  ↓ astype(float) + filtro por campaña
src/metrics.py → métricas (ROAS, CTR, CPC, CPM, CPA)
src/prophet_model.py → serie temporal → Prophet → forecast 7 días
  ↓
matplotlib (visualizaciones)
```

## Entornos soportados
- **Google Colab** (primario) — `google.colab.auth` maneja OAuth
- **Local / VS Code** — `sys.path.insert(0, '.')` para imports desde raíz
