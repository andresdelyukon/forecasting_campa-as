# INTEGRATIONS

## Google Sheets API
- **Cliente:** `gspread` + `google-auth`
- **Autenticación:** OAuth via `google.colab.auth.authenticate_user()` (Colab) o credenciales default
- **Sheet 1 — All Media** (`SHEET_ID_ALL_MEDIA`): datos crudos de campañas (clicks, spend, impressions, ROAS, Revenue con IVA, etc.)
- **Sheet 2 — Presupuesto Optimizado** (`SHEET_ID_PRESUPUESTO_OPTIMIZADO`): output del modelo MMM con recomendaciones de presupuesto por canal

## Prophet (Meta)
- Librería open-source de forecasting de series temporales
- Configurada con holidays personalizados (Hot Sale, Hot Fashion) definidos en `config/settings.py`
- Cross-validation con `prophet.diagnostics`

## GitHub
- Repositorio: `https://github.com/andresdelyukon/forecasting_campa-as`
- El notebook clona el repo al inicio cuando corre en Colab

## Sin base de datos
- No hay persistencia local — todos los datos vienen de Google Sheets en runtime
