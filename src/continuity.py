import pandas as pd
import matplotlib.pyplot as plt


def analizar_continuidad_campana(df, campaign_name, fecha_inicio, fecha_fin, metrica="Revenue con IVA"):
    """
    Verifica si una campaña tiene datos continuos en el rango de fechas
    y grafica la métrica diaria (revenue o spend).

    Devuelve dict con: continua, dias_faltantes, dias_con_data, dias_esperados.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    df_camp = df[
        (df["campaign.name"] == campaign_name)
        & (df["date"] >= fecha_inicio)
        & (df["date"] <= fecha_fin)
    ]

    rango_completo = pd.date_range(start=fecha_inicio, end=fecha_fin, freq="D")
    fechas_existentes = df_camp["date"].dt.normalize().unique()
    fechas_faltantes = sorted(set(rango_completo) - set(fechas_existentes))

    df_plot = df_camp.groupby("date")[metrica].sum().reset_index()

    etiqueta = "Revenue" if metrica == "Revenue con IVA" else "Spend"
    plt.figure()
    plt.plot(df_plot["date"], df_plot[metrica])
    plt.xlabel("Fecha")
    plt.ylabel(etiqueta)
    plt.title(f"{etiqueta} diario - {campaign_name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return {
        "continua": len(fechas_faltantes) == 0,
        "dias_faltantes": fechas_faltantes,
        "dias_con_data": len(fechas_existentes),
        "dias_esperados": len(rango_completo),
    }


def analizar_continuidad_campana_revenue(df, campaign_name, fecha_inicio, fecha_fin):
    return analizar_continuidad_campana(df, campaign_name, fecha_inicio, fecha_fin, metrica="Revenue con IVA")


def analizar_continuidad_campana_gasto(df, campaign_name, fecha_inicio, fecha_fin):
    return analizar_continuidad_campana(df, campaign_name, fecha_inicio, fecha_fin, metrica="spend")
