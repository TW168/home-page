from collections import defaultdict
from datetime import datetime

import mysql.connector
from django.shortcuts import render


WARSHIP_DB_CONFIG = {
    "user": "root",
    "password": "n1cenclean",
    "host": "172.17.15.228",
    "port": 3306,
    "database": "warship",
}


def _build_gas_chart_data(limit: int = 120):
    labels = []
    datasets = []
    status_note = "Live from Warship MySQL"

    try:
        conn = mysql.connector.connect(**WARSHIP_DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT fuel_type, price, scraped_at
            FROM warship.gas_prices
            ORDER BY scraped_at DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        rows.reverse()
        label_set = []
        fuel_by_label = defaultdict(dict)
        for row in rows:
            scraped_at = row.get("scraped_at")
            if isinstance(scraped_at, datetime):
                label = scraped_at.strftime("%Y-%m-%d %H:%M")
            else:
                label = str(scraped_at)
            if label not in fuel_by_label:
                label_set.append(label)
            fuel_by_label[label][row["fuel_type"]] = float(row["price"])

        labels = label_set
        fuel_types = sorted({r["fuel_type"] for r in rows})
        line_colors = [
            "#0072B2",
            "#D55E00",
            "#009E73",
            "#CC79A7",
            "#E69F00",
            "#56B4E9",
            "#F0E442",
            "#000000",
        ]
        dash_patterns = [
            [],
            [8, 4],
            [3, 4],
            [10, 5, 2, 5],
            [2, 3],
            [12, 6],
            [5, 2, 1, 2],
            [1, 3],
        ]

        for idx, fuel_type in enumerate(fuel_types):
            color = line_colors[idx % len(line_colors)]
            values = []
            for label in labels:
                values.append(fuel_by_label[label].get(fuel_type))
            datasets.append(
                {
                    "label": fuel_type,
                    "data": values,
                    "borderColor": color,
                    "backgroundColor": color,
                    "borderDash": dash_patterns[idx % len(dash_patterns)],
                    "borderWidth": 3,
                    "tension": 0.25,
                    "pointRadius": 2,
                    "pointHoverRadius": 5,
                    "spanGaps": True,
                }
            )

        if not labels:
            status_note = "No records found in warship.gas_prices"
    except Exception as exc:  # pragma: no cover - keeps dashboard available even if DB is offline
        status_note = f"Gas chart unavailable: {exc}"

    return labels, datasets, status_note


def home(request):
    nav_items = [
        {
            "title": "Presentation",
            "href": "/presentation/",
        },
        {
            "title": "Meeting Report",
            "href": "#",
        },
        {
            "title": "TSR Prep",
            "href": "#",
        },
        {
            "title": "Shipping",
            "href": "#",
        },
        {
            "title": "Warehouse",
            "href": "#",
        },
        {
            "title": "ISO Docs",
            "href": "#",
        },
        {
            "title": "About",
            "href": "#",
        },
    ]

    weather_panels = [
        {
            "title": "NOAA Maximum Temperature (CONUS)",
            "note": "Refreshed daily at 06:00.",
            "image_url": "/static/assets/weather/MaxT1_conus.png",
            "source_label": "NOAA Graphical Forecast",
            "source_url": "https://graphical.weather.gov/images/conus/MaxT1_conus.png",
        },
        {
            "title": "NOAA National Forecast",
            "note": "Refreshed daily at 06:00.",
            "image_url": "/static/assets/weather/national_forecast.jpg",
            "source_label": "NOAA WPC National Forecast",
            "source_url": "https://www.wpc.ncep.noaa.gov/noaa/national_forecast.jpg",
        },
    ]

    gas_chart_labels, gas_chart_datasets, _ = _build_gas_chart_data()

    gas_scrape = {
        "title": "AAA Gas Prices",
        "status": "Daily Scrape",
        "note": "Refresh daily at 07:30.",
    }

    context = {
        "nav_items": nav_items,
        "weather_panels": weather_panels,
        "gas_scrape": gas_scrape,
        "gas_chart_labels": gas_chart_labels,
        "gas_chart_datasets": gas_chart_datasets,
    }
    return render(request, "dashboard/home.html", context)
