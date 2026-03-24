import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics


def get_serie_por_campana(campana, df, metrica="Revenue con IVA"):
    """
    Extrae la serie temporal diaria de una métrica para una campaña
    y devuelve un DataFrame en formato Prophet (columnas: ds, y).
    """
    resultado = (
        df[df["campaign.name"] == campana]
        .groupby("date", as_index=False)[metrica]
        .sum()
        .sort_values("date")
    )
    resultado.columns = ["ds", "y"]
    resultado["ds"] = pd.to_datetime(resultado["ds"], errors="coerce")
    resultado = resultado.dropna(subset=["ds"])
    return resultado


def get_revenue_por_campana(campana, df):
    return get_serie_por_campana(campana, df, metrica="Revenue con IVA")


def get_spend_por_campana(campana, df):
    return get_serie_por_campana(campana, df, metrica="spend")


def construir_holidays(eventos: dict) -> pd.DataFrame:
    """
    Construye el DataFrame de holidays para Prophet a partir de un dict.

    Ejemplo de entrada (desde config/settings.py):
        {
            "hot_sale": {"ds": ["2025-06-03"], "lower_window": -2, "upper_window": 2},
        }
    """
    frames = []
    for nombre, cfg in eventos.items():
        frames.append(pd.DataFrame({
            "holiday": nombre,
            "ds": pd.to_datetime(cfg["ds"]),
            "lower_window": cfg.get("lower_window", 0),
            "upper_window": cfg.get("upper_window", 0),
        }))
    return pd.concat(frames, ignore_index=True)


def entrenar_prophet(df_prophet, changepoint_prior_scale=0.5, holidays=None, periodos=7):
    """
    Entrena un modelo Prophet y devuelve (modelo, forecast).

    Parámetros:
        df_prophet: DataFrame con columnas ds, y
        changepoint_prior_scale: flexibilidad del trend (0.05 conservador, 0.5 flexible)
        holidays: DataFrame de holidays (usar construir_holidays())
        periodos: días a predecir hacia adelante
    """
    m = Prophet(changepoint_prior_scale=changepoint_prior_scale, holidays=holidays)
    m.fit(df_prophet)
    future = m.make_future_dataframe(periods=periodos)
    forecast = m.predict(future)
    return m, forecast


def evaluar_modelo(modelo, initial="200 days", period="7 days", horizon="7 days"):
    """
    Corre validación cruzada y devuelve las métricas de rendimiento.
    """
    df_cv = cross_validation(modelo, initial=initial, period=period, horizon=horizon)
    df_perf = performance_metrics(df_cv)
    return df_cv, df_perf
