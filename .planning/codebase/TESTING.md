# TESTING

## Estado actual
**Sin tests automatizados.** No hay archivos `test_*.py`, `pytest.ini`, ni CI configurado.

## Validación existente
- Validación manual en el notebook: `df.head()`, `print(filtered_df)`, inspección visual de gráficos
- Cross-validation de Prophet via `prophet.diagnostics.cross_validation` con métrica MASE
- Early returns con mensajes de error en funciones de `src/` (validación de datos vacíos)

## Recomendaciones para agregar tests
Si se quiere agregar cobertura mínima:
```
tests/
├── test_metrics.py       ← analizar_campanas, promedio_campana con DataFrames sintéticos
├── test_continuity.py    ← analizar_continuidad con gaps artificiales
└── test_prophet_model.py ← get_serie_por_campana con datos mock
```

Framework sugerido: `pytest` + `pandas.testing` para comparar DataFrames.
