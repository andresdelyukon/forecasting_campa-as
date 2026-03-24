# CONCERNS

## Crítico

- **División por cero en métricas** — CTR, CPC, CPM, CPA se calculan sin validar denominadores en `src/metrics.py`; se mitiga con `replace([np.inf, -np.inf], np.nan)` pero puede silenciar errores reales
- **IDs de Google Sheets en el repo** — `SHEET_ID_ALL_MEDIA` y `SHEET_ID_PRESUPUESTO_OPTIMIZADO` están en `config/settings.py` versionado; deberían ir en variables de entorno (`.env` + `.gitignore`)
- **Sin validación de datos externos** — el DataFrame de Google Sheets se consume directamente sin verificar columnas esperadas, tipos, ni rangos de valores; errores de tipo fallan silenciosamente
- **122 nombres de campaña hardcodeados** en `src/campaigns.py` sin verificación contra los datos reales; si una campaña se renombra en Sheets, filtra vacío sin advertencia

## Alta prioridad

- **Sin tests** — cero cobertura automática; errores en `src/` solo se detectan corriendo el notebook completo
- **`changepoint_prior_scale` único para todas las campañas** — un solo valor en `config/settings.py` para +100 campañas con comportamientos muy distintos
- **Inconsistencia de columnas** — el sheet usa `Clicks`/`Impresiones`/`Spend` (mayúsculas) y el código analítico usa `clicks`/`impressions`/`spend` (minúsculas); el comportamiento depende de qué sheet se cargue
- **Sin logging estructurado** — solo `print()` statements; no hay forma de auditar ejecuciones pasadas o detectar regresiones

## Media prioridad

- **Funciones de cálculo y visualización acopladas** — `analizar_roas_mensual`, `analizar_continuidad_campana` calculan y grafican juntas; los `plt.show()` rompen ejecución en modo headless/batch
- **Fechas hardcodeadas en celdas de análisis del notebook** — aunque los parámetros globales están en `config/settings.py`, varias celdas de ejemplo usan fechas literales
- **Celdas del notebook con código muerto** — algunas celdas reemplazadas por comentarios de importación dejaron flujo redundante
- **Sin type hints** en funciones de `src/`

## Seguridad

- Los outputs del notebook pueden contener datos de clientes — limpiar con `jupyter nbconvert --clear-output` antes de cada commit (el `.gitignore` no lo hace automáticamente)
- `.gitignore` excluye `*.json` correctamente (credenciales de servicio de Google)

## Áreas frágiles

- Dependencia total de Google Sheets en runtime — sin fallback local
- Listas de campañas en `src/campaigns.py` — acopladas al naming actual de Sheets
- Interdependencia de celdas en el notebook — el orden de ejecución importa y no está documentado
