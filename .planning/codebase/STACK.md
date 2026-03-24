# STACK

## Language & Runtime
- **Python 3** (notebook requiere >=3.8 por Prophet)
- **Jupyter Notebook** — entorno de ejecución principal

## Frameworks & Libraries
| Librería | Uso |
|----------|-----|
| `prophet` | Forecasting de series temporales |
| `pandas` | Manipulación de datos y agregaciones |
| `numpy` | Cálculos numéricos y manejo de infinitos |
| `matplotlib` | Visualizaciones (boxplot, histograma, línea) |
| `gspread` | Cliente de Google Sheets API |
| `google-auth` | Autenticación OAuth con Google |

## Configuración
- `config/settings.py` — parámetros globales: IDs de sheets, fechas, `CHANGEPOINT_PRIOR_SCALE`, `FORECAST_HORIZON_DAYS`, holidays
- `requirements.txt` — dependencias del proyecto

## Entorno de ejecución soportado
- **Google Colab** (primario) — autenticación via `google.colab.auth`
- **Local / VS Code** — via `sys.path` apuntando a raíz del proyecto
