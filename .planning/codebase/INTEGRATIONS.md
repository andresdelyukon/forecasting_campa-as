# INTEGRATIONS

## Google Sheets API

### Sheet 1 — All Media
- **ID**: `SHEET_ID_ALL_MEDIA` (en `config/settings.py`)
- Datos crudos de campañas: date, campaign.name, Clicks, Impresiones, Spend, Transacciones, Revenue con IVA, ROAS, CPC, CPM, CTR, CPA, Objetivo por medio
- Actualizado diariamente con performance de plataformas de ads

### Sheet 2 — Presupuesto Optimizado
- **ID**: `SHEET_ID_PRESUPUESTO_OPTIMIZADO` (en `config/settings.py`)
- Output del modelo MMM: columnas Objetivo + presupuesto recomendado por modelo
- Se compara contra distribución actual de spend

### Implementación
```python
from google.colab import auth
auth.authenticate_user()
import gspread
from google.auth import default
creds, _ = default()
gc = gspread.authorize(creds)
worksheet = gc.open_by_key(SHEET_ID_ALL_MEDIA).sheet1
rows = worksheet.get_all_values()
df = pd.DataFrame.from_records(rows[1:], columns=rows[0])
```

### Autenticación
- **Colab**: `google.colab.auth.authenticate_user()` → OAuth consent → credenciales temporales de sesión
- **Local**: `google.auth.default()` con credenciales de entorno
- Sesión ligada al kernel de Colab (se pierde al reiniciar)

## Campañas monitoreadas
- **INNOVA** (~28 campañas): prefijos `aw_innova_*` y `fb_innova_*` — SEM, Shopping, PMAX, DPA, DABA
- **FESA** (~90 campañas): prefijos `aw_fesa_*` y `fb_fesa_*` — eComm, Calls, App installs, Brand, WhatsApp

## Sin otras integraciones externas
- No hay llamadas directas a Google Ads API, Meta Graph API, ni GA4
- Los datos llegan pre-exportados desde las plataformas → Google Sheets → este pipeline
- Prophet corre localmente (sin servicios externos de ML)

## Puntos de extensión futuros
- **Escribir forecasts de vuelta a Sheets**: `worksheet.update()` con scope read-write
- **Ejecución programada**: Cloud Functions + Cloud Scheduler
- **Volúmenes grandes**: BigQuery en lugar de Google Sheets
