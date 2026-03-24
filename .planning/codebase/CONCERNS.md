# CONCERNS

## Deuda técnica

### Alta prioridad
- **Sin tests** — no hay cobertura automática; errores en `src/` solo se detectan corriendo el notebook
- **IDs de Google Sheets hardcodeados en `config/settings.py`** — deberían ir en variables de entorno (`.env`) para no exponerlos en el repo
- **Listas de campañas estáticas** (`src/campaigns.py`) — si se agrega una campaña nueva en Sheets, hay que actualizar el código manualmente

### Media prioridad
- **Inconsistencia de columnas** — el sheet usa `Clicks`/`Impresiones`/`Spend` (mayúsculas) y el código analítico usa `clicks`/`impressions`/`spend` (minúsculas); depende de qué sheet se cargue
- **Funciones de métricas y visualización acopladas** — `analizar_roas_mensual`, `analizar_continuidad_campana` calculan y grafican en la misma función, difícil de reutilizar solo el cálculo
- **Sin logs** — no hay forma de saber qué pasó en ejecuciones anteriores

### Baja prioridad
- **`changepoint_prior_scale=0.5` global** — un solo valor para todas las campañas; campañas con comportamiento muy distinto podrían necesitar valores diferentes
- **Notebook con 78 celdas** — flujo largo y difícil de seguir; candidato a dividirse en notebooks más pequeños por fase (análisis, forecasting, reportes)

## Seguridad
- Los IDs de Google Sheets están en `config/settings.py` dentro del repo — no son credenciales pero identifican los sheets
- El `.gitignore` excluye `*.json` (credenciales de servicio de Google), correcto
- Los outputs del notebook deben limpiarse antes de cada commit (`jupyter nbconvert --clear-output`) para no exponer datos de clientes
