# STRUCTURE

## Árbol de directorios
```
forecasting campañas/
├── .planning/
│   └── codebase/           ← documentos de mapeo (este directorio)
├── config/
│   ├── __init__.py
│   └── settings.py         ← IDs sheets, fechas, Prophet params, holidays
├── src/
│   ├── __init__.py
│   ├── campaigns.py        ← CAMPANAS_INNOVA, CAMPANAS_FESA (~90 líneas cada lista)
│   ├── metrics.py          ← analizar_campanas, promedio_campana, ROAS, boxplot, histograma
│   ├── continuity.py       ← analizar_continuidad_campana (revenue y gasto)
│   └── prophet_model.py    ← get_serie, construir_holidays, entrenar_prophet, evaluar_modelo
├── notebooks/
│   └── Forecasting_campañas.ipynb   ← 78 celdas, flujo principal
├── .gitignore
├── README.md
└── requirements.txt
```

## Convenciones de nombres
- Módulos: `snake_case`
- Funciones: `snake_case` con verbo descriptivo (`analizar_`, `get_`, `construir_`, `entrenar_`)
- Constantes: `UPPER_SNAKE_CASE` (ej: `CAMPANAS_INNOVA`, `CHANGEPOINT_PRIOR_SCALE`)
- Variables en notebook: `snake_case` descriptivo (ej: `df_all_media`, `df_prophet`)

## Ubicaciones clave
- Parámetros a ajustar: `config/settings.py`
- Agregar campañas: `src/campaigns.py`
- Nuevas métricas: `src/metrics.py`
- Lógica de Prophet: `src/prophet_model.py`
