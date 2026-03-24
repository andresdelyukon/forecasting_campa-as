import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def analizar_campanas(df, fecha_inicio, fecha_fin, metrica="ROAS", ascendente=False):
    """
    Agrega métricas por campaña en un rango de fechas y ordena por la métrica elegida.
    Métricas disponibles: ROAS, CTR, CPC, CPM, CPA.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= fecha_inicio) & (df["date"] <= fecha_fin)]

    if df.empty:
        print(f"Sin datos en el periodo {fecha_inicio} - {fecha_fin}")
        return pd.DataFrame()

    agg = df.groupby("campaign.name").agg(
        clicks=("clicks", "sum"),
        spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        transacciones=("Transacciones", "sum"),
        revenue=("Revenue con IVA", "sum"),
    ).reset_index()

    agg["CTR"] = agg["clicks"] / agg["impressions"]
    agg["CPC"] = agg["spend"] / agg["clicks"]
    agg["CPM"] = (agg["spend"] / agg["impressions"]) * 1000
    agg["CPA"] = agg["spend"] / agg["transacciones"]
    agg["ROAS"] = agg["revenue"] / agg["spend"]

    agg.replace([np.inf, -np.inf], np.nan, inplace=True)

    return agg.sort_values(by=metrica, ascending=ascendente)


def promedio_campana(df, nombre_campana, fecha_inicio, fecha_fin):
    """
    Devuelve el promedio diario de spend, Revenue e IVA y ROAS
    para una campaña en un rango de fechas.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    df_filtrado = df[
        (df["campaign.name"] == nombre_campana)
        & (df["date"] >= fecha_inicio)
        & (df["date"] <= fecha_fin)
    ]

    if df_filtrado.empty:
        print(f"Sin datos para '{nombre_campana}' en el periodo {fecha_inicio} - {fecha_fin}")
        return None

    return df_filtrado[["spend", "Revenue con IVA", "ROAS"]].mean()


def analizar_roas_mensual(df, campaign_name, fecha_inicio, fecha_fin):
    """
    Calcula el ROAS mensual de una campaña y genera un gráfico de línea.
    Devuelve el DataFrame mensual con columnas: mes, Revenue con IVA, spend, ROAS.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    df_camp = df[
        (df["campaign.name"] == campaign_name)
        & (df["date"] >= pd.to_datetime(fecha_inicio))
        & (df["date"] <= pd.to_datetime(fecha_fin))
    ]

    if df_camp.empty:
        print(f"Sin datos para '{campaign_name}'")
        return pd.DataFrame()

    df_camp = df_camp.copy()
    df_camp["mes"] = df_camp["date"].dt.to_period("M")

    df_mes = df_camp.groupby("mes").agg(
        revenue=("Revenue con IVA", "sum"),
        spend=("spend", "sum"),
    ).reset_index()

    df_mes["ROAS"] = np.where(df_mes["spend"] > 0, df_mes["revenue"] / df_mes["spend"], np.nan)
    df_mes["mes"] = df_mes["mes"].dt.to_timestamp()

    plt.figure()
    plt.plot(df_mes["mes"], df_mes["ROAS"], marker="o")
    plt.xlabel("Mes")
    plt.ylabel("ROAS")
    plt.title(f"ROAS mensual - {campaign_name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return df_mes


def boxplot_campana(df, campaign_name, metric):
    """Boxplot de una métrica para detectar outliers en una campaña."""
    df_camp = df[df["campaign.name"] == campaign_name]
    if df_camp.empty:
        print(f"Sin datos para '{campaign_name}'")
        return

    plt.figure(figsize=(6, 4))
    plt.boxplot(df_camp[metric].dropna())
    plt.title(f"Boxplot de {metric} - {campaign_name}")
    plt.ylabel(metric)
    plt.show()


def histograma_campana(df, campaign_name, metric, bins=30):
    """Histograma de una métrica para ver la distribución de una campaña."""
    df_camp = df[df["campaign.name"] == campaign_name]
    if df_camp.empty:
        print(f"Sin datos para '{campaign_name}'")
        return

    plt.figure(figsize=(7, 4))
    plt.hist(df_camp[metric].dropna(), bins=bins)
    plt.title(f"Histograma de {metric} - {campaign_name}")
    plt.xlabel(metric)
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.show()
