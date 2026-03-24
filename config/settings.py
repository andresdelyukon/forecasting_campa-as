# ── Parámetros globales del proyecto ─────────────────────────────────────────
# Ajusta estos valores antes de correr el notebook

# IDs de Google Sheets
SHEET_ID_ALL_MEDIA = "114qrqgEosT7FSLDpA210ksnuBHVjUUlpdfKArm-6Nq8"
SHEET_ID_PRESUPUESTO_OPTIMIZADO = "1WvlbVZJWePjZQZ5g3eszzLiqmUAfrJmu-b3ayu8n1vo"

# Rango de análisis por defecto
FECHA_INICIO = "2025-01-01"
FECHA_FIN = "2026-03-10"

# Columnas numéricas del sheet all_media
COLUMNAS_NUMERICAS = [
    "Clicks", "Impresiones", "Spend",
    "clicks", "spend", "impressions",
    "CPC", "CPM", "CTR",
    "Transacciones", "CPA", "Revenue con IVA", "ROAS",
]

# Prophet
CHANGEPOINT_PRIOR_SCALE = 0.5   # 0.05 conservador → 0.5 flexible
FORECAST_HORIZON_DAYS = 7

# Eventos especiales para Prophet
HOLIDAYS = {
    "hot_sale":    {"ds": ["2025-06-03"], "lower_window": -2, "upper_window": 2},
    "hot_fashion": {"ds": ["2025-04-02"], "lower_window": -2, "upper_window": 2},
}
