import pandas as pd
import numpy as np


# ── Helpers internos ──────────────────────────────────────────────────────────

def _filtrar_por_keyword(campanas: list, keyword: str) -> list:
    """Devuelve campañas cuyo nombre contiene el keyword (case-insensitive)."""
    return [c for c in campanas if keyword.lower() in c.lower()]


def _roas_por_campana(df: pd.DataFrame, campanas: list, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
    """
    Calcula Revenue, Spend y ROAS por campaña en un rango de fechas.
    Devuelve DataFrame indexado por campaign.name.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    mask = (
        df["campaign.name"].isin(campanas)
        & (df["date"] >= fecha_inicio)
        & (df["date"] <= fecha_fin)
    )
    agg = (
        df[mask]
        .groupby("campaign.name")
        .agg(revenue=("Revenue con IVA", "sum"), spend=("spend", "sum"))
    )
    agg["ROAS"] = np.where(agg["spend"] > 0, agg["revenue"] / agg["spend"], np.nan)
    return agg


def _spend_diario(spend_total: float, fecha_inicio: str, fecha_fin: str) -> float:
    """Calcula el gasto diario promedio en base al total del periodo."""
    dias = (pd.to_datetime(fecha_fin) - pd.to_datetime(fecha_inicio)).days + 1
    return spend_total / dias if dias > 0 else 0


# ── Motor de reglas ───────────────────────────────────────────────────────────

def generar_recomendaciones(
    df: pd.DataFrame,
    campanas: list,
    movimientos: list,
    fecha_hist_inicio: str,
    fecha_hist_fin: str,
    fecha_reciente_inicio: str,
    fecha_reciente_fin: str,
    umbral_mejora: float = 0.10,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Genera recomendaciones de reasignación de presupuesto entre objetivos.

    Parámetros
    ----------
    df : DataFrame con datos de campañas (columnas: date, campaign.name, spend, Revenue con IVA)
    campanas : lista de campañas a considerar (ej: CAMPANAS_INNOVA)
    movimientos : lista de dicts con la estructura:
        [
            {
                'origen': 'pla',       # keyword del objetivo a recortar
                'destino': 'daba',     # keyword del objetivo receptor
                'porcentaje': 0.05,    # % a mover (0.05 = 5%)
            },
            ...
        ]
    fecha_hist_inicio / fecha_hist_fin : ventana larga para rankear por ROAS histórico
    fecha_reciente_inicio / fecha_reciente_fin : ventana corta para detectar tendencia y calcular montos
    umbral_mejora : si el ROAS reciente supera al histórico en este % → skip esta campaña y baja a la siguiente

    Devuelve
    --------
    df_detalle : tabla fila por fila con cada decisión de subir/bajar
    df_resumen : totales por movimiento (cuánto se libera y dónde va)
    """
    filas_detalle = []
    filas_resumen = []

    for mov in movimientos:
        keyword_origen = mov["origen"]
        keyword_destino = mov["destino"]
        pct = mov["porcentaje"]

        # ── LADO BAJAR (origen) ───────────────────────────────────────────────
        camps_origen = _filtrar_por_keyword(campanas, keyword_origen)

        if not camps_origen:
            print(f"[AVISO] No se encontraron campañas con keyword '{keyword_origen}'")
            continue

        roas_hist_origen = _roas_por_campana(df, camps_origen, fecha_hist_inicio, fecha_hist_fin)
        roas_rec_origen = _roas_por_campana(df, camps_origen, fecha_reciente_inicio, fecha_reciente_fin)

        # Rankear ascendente: peor ROAS histórico primero (candidato a recortar)
        ranking_origen = (
            roas_hist_origen.dropna(subset=["ROAS"])
            .sort_values("ROAS", ascending=True)
            .reset_index()
        )

        campana_recortada = None
        delta_diario = 0.0

        for rank_idx, row in ranking_origen.iterrows():
            camp = row["campaign.name"]
            roas_h = row["ROAS"]

            # Tendencia reciente
            if camp in roas_rec_origen.index:
                roas_r = roas_rec_origen.loc[camp, "ROAS"]
                spend_rec = roas_rec_origen.loc[camp, "spend"]
            else:
                roas_r = np.nan
                spend_rec = row["spend"]

            mejora = ((roas_r - roas_h) / roas_h) if (pd.notna(roas_r) and roas_h > 0) else 0
            tendencia_str = f"+{mejora*100:.1f}%" if mejora > 0 else f"{mejora*100:.1f}%"

            spend_dia = _spend_diario(spend_rec, fecha_reciente_inicio, fecha_reciente_fin)
            delta = spend_dia * pct

            # Si está mejorando por encima del umbral → skip
            if mejora > umbral_mejora:
                filas_detalle.append({
                    "movimiento": f"{keyword_origen.upper()} → {keyword_destino.upper()}",
                    "accion": "SKIP (mejorando)",
                    "objetivo": keyword_origen.upper(),
                    "campaña": camp,
                    "rank_ROAS_hist": rank_idx + 1,
                    "ROAS_historico": round(roas_h, 2),
                    "ROAS_reciente": round(roas_r, 2) if pd.notna(roas_r) else "-",
                    "tendencia": tendencia_str,
                    "spend_diario_actual": round(spend_dia, 2),
                    "delta_diario": 0,
                    "spend_diario_recomendado": round(spend_dia, 2),
                })
                continue  # Pasa a la siguiente rankeada

            # Esta campaña recibe el recorte
            campana_recortada = camp
            delta_diario = delta

            filas_detalle.append({
                "movimiento": f"{keyword_origen.upper()} → {keyword_destino.upper()}",
                "accion": "BAJAR",
                "objetivo": keyword_origen.upper(),
                "campaña": camp,
                "rank_ROAS_hist": rank_idx + 1,
                "ROAS_historico": round(roas_h, 2),
                "ROAS_reciente": round(roas_r, 2) if pd.notna(roas_r) else "-",
                "tendencia": tendencia_str,
                "spend_diario_actual": round(spend_dia, 2),
                "delta_diario": round(-delta, 2),
                "spend_diario_recomendado": round(spend_dia - delta, 2),
            })
            break  # Solo recortar una campaña por movimiento

        if campana_recortada is None:
            print(f"[AVISO] Todas las campañas de '{keyword_origen}' están mejorando — no se recortó ninguna.")
            continue

        # ── LADO SUBIR (destino) ──────────────────────────────────────────────
        camps_destino = _filtrar_por_keyword(campanas, keyword_destino)

        if not camps_destino:
            print(f"[AVISO] No se encontraron campañas con keyword '{keyword_destino}'")
            continue

        roas_hist_destino = _roas_por_campana(df, camps_destino, fecha_hist_inicio, fecha_hist_fin)
        roas_rec_destino = _roas_por_campana(df, camps_destino, fecha_reciente_inicio, fecha_reciente_fin)

        # Rankear descendente: mejor ROAS histórico primero (recibe el presupuesto)
        ranking_destino = (
            roas_hist_destino.dropna(subset=["ROAS"])
            .sort_values("ROAS", ascending=False)
            .reset_index()
        )

        if ranking_destino.empty:
            print(f"[AVISO] Sin datos de ROAS para campañas de '{keyword_destino}'")
            continue

        top = ranking_destino.iloc[0]
        camp_dest = top["campaign.name"]
        roas_h_dest = top["ROAS"]

        if camp_dest in roas_rec_destino.index:
            roas_r_dest = roas_rec_destino.loc[camp_dest, "ROAS"]
            spend_rec_dest = roas_rec_destino.loc[camp_dest, "spend"]
        else:
            roas_r_dest = np.nan
            spend_rec_dest = top["spend"]

        spend_dia_dest = _spend_diario(spend_rec_dest, fecha_reciente_inicio, fecha_reciente_fin)
        mejora_dest = (
            (roas_r_dest - roas_h_dest) / roas_h_dest
            if (pd.notna(roas_r_dest) and roas_h_dest > 0)
            else 0
        )
        tendencia_dest = f"+{mejora_dest*100:.1f}%" if mejora_dest > 0 else f"{mejora_dest*100:.1f}%"

        filas_detalle.append({
            "movimiento": f"{keyword_origen.upper()} → {keyword_destino.upper()}",
            "accion": "SUBIR",
            "objetivo": keyword_destino.upper(),
            "campaña": camp_dest,
            "rank_ROAS_hist": 1,
            "ROAS_historico": round(roas_h_dest, 2),
            "ROAS_reciente": round(roas_r_dest, 2) if pd.notna(roas_r_dest) else "-",
            "tendencia": tendencia_dest,
            "spend_diario_actual": round(spend_dia_dest, 2),
            "delta_diario": round(delta_diario, 2),
            "spend_diario_recomendado": round(spend_dia_dest + delta_diario, 2),
        })

        filas_resumen.append({
            "movimiento": f"{keyword_origen.upper()} → {keyword_destino.upper()}",
            "% reasignado": f"{pct*100:.0f}%",
            "campaña origen (BAJAR)": campana_recortada,
            "delta diario origen": round(-delta_diario, 2),
            "campaña destino (SUBIR)": camp_dest,
            "delta diario destino": round(delta_diario, 2),
            "impacto mensual estimado": round(delta_diario * 30, 2),
        })

    df_detalle = pd.DataFrame(filas_detalle)
    df_resumen = pd.DataFrame(filas_resumen)
    return df_detalle, df_resumen
