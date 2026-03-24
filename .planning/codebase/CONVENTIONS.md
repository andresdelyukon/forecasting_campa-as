# CONVENTIONS

## Estilo de código
- Python estándar, sin linter configurado
- Español para nombres de variables de dominio (campañas, métricas de negocio)
- Inglés para nombres técnicos internos de funciones y módulos
- Imports al tope de cada módulo en `src/`; imports inline en funciones heredadas del notebook

## Patrones de funciones
- Todas las funciones de análisis reciben `df` como primer argumento y hacen `df = df.copy()` para no mutar el original
- Validación de datos vacíos con early return y mensaje descriptivo:
  ```python
  if df.empty:
      print(f"Sin datos para '{nombre}' en {fecha_inicio} - {fecha_fin}")
      return None
  ```
- Conversión de fechas siempre con `pd.to_datetime()` dentro de la función
- `np.inf` / `-np.inf` reemplazados por `np.nan` tras cálculos de ratios

## Manejo de errores
- No hay excepciones explícitas (`try/except`) — se usa early return con print
- Datos corruptos en Prophet: `pd.to_datetime(..., errors='coerce')` + `dropna(subset=['ds'])`

## Visualizaciones
- `matplotlib` directo (sin seaborn ni plotly)
- Patrón: `plt.figure()` → plot → labels → `plt.tight_layout()` → `plt.show()`
- Las funciones de visualización combinan cálculo + gráfico en una sola función
