# CFP v2 Django Site

Phase 1 Django shell for coexistence with Warship FastAPI.

## Implemented
- Dashboard-style home page
- Two NOAA weather map placeholders (links pending)
- Module placeholders: Warehouse, Shipping, TSR_Prep, ISO Documents, About, Presentation
- Additional placeholder: Meeting Report

## Run
1. Install dependencies:

```bash
uv sync
```

2. Run migrations:

```bash
uv run python manage.py migrate
```

3. Start server:

```bash
uv run python manage.py runserver
```

Open http://127.0.0.1:8000/

## Next
- Configure local NOAA map scraping cron job for Django static assets.
- Wire Warship staff links for Warehouse, Shipping, and TSR_Prep.
- Implement ISO internal module with change-log model.

## NOAA Scrape Cron Job
The dashboard reads NOAA map images from local static files:
- `/static/assets/weather/MaxT1_conus.png`
- `/static/assets/weather/national_forecast.jpg`

To enable daily scraping into this Django project:

1. Make script executable:

```bash
chmod +x /home/tony/cfp-v2/scripts/scrape_noaa_maps.sh
```

2. Add cron entry (see full template in `ops/cronjobs.txt`):

```bash
0 6 * * * /home/tony/cfp-v2/scripts/scrape_noaa_maps.sh >> /tmp/cfp_noaa_scrape.log 2>&1
```
