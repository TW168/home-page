import datetime
import json
from collections import Counter, defaultdict
from statistics import median
from urllib.error import URLError
from urllib.request import urlopen

import mysql.connector
from django.http import JsonResponse
from django.shortcuts import render

from .models import PresentationCard, SafetyCard, FreightAnalytics, CarrierUsage

_WARSHIP_DB = {
    "user": "root",
    "password": "n1cenclean",
    "host": "172.17.15.228",
    "port": 3306,
    "database": "warship",
}

_WARSHIP_FASTAPI_BASE = "http://127.0.0.1:8088"


def _nav_items():
    return [
        {"title": "Home", "href": "/"},
        {"title": "Presentation", "href": "/presentation/"},
        {"title": "Meeting Report", "href": "#"},
        {"title": "TSR Prep", "href": "#"},
        {"title": "Shipping", "href": "#"},
        {"title": "Warehouse", "href": "#"},
        {"title": "ISO Docs", "href": "#"},
        {"title": "About", "href": "#"},
    ]


def presentation_home(request):
    card = PresentationCard.objects.order_by("-updated_at", "id").first()
    safety_card = SafetyCard.objects.order_by("-updated_at", "id").first()
    freight_analytics = FreightAnalytics.objects.filter(site="AMJK", product_group="SW").order_by("-last_synced").first()
    carrier_usage = CarrierUsage.objects.filter(site="AMJK", product_group="SW").order_by("-last_synced").first()
    
    context = {
        "nav_items": _nav_items(),
        "card": card,
        "safety_card": safety_card,
        "freight_analytics": freight_analytics,
        "carrier_usage": carrier_usage,
    }
    return render(request, "presentation/home.html", context)


def freight_cpb_boxplot_api(request):
    """Return top-50 product-code distributions for AMJK SW YTD box plot.

    Source: FastAPI /api/shipping/shipped-products endpoint in extra/shipping.py.
    """
    current_year = datetime.date.today().year
    start_date = f"{current_year}-01-01"
    end_date = f"{current_year}-12-31"
    endpoint = (
        f"{_WARSHIP_FASTAPI_BASE}/api/shipping/shipped-products"
        f"?site=AMJK&product_group=SW&start_date={start_date}&end_date={end_date}"
    )

    try:
        with urlopen(endpoint, timeout=20) as response:
            rows = json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return JsonResponse({"error": str(exc)}, status=500)

    by_code = defaultdict(list)
    weight_by_code = Counter()
    for row in rows:
        product_code = row.get("product_code")
        unit_freight = row.get("unit_freight")
        pick_weight = row.get("pick_weight") or 0
        if not product_code or unit_freight is None:
            continue
        by_code[product_code].append(float(unit_freight))
        weight_by_code[product_code] += int(pick_weight)

    top_codes = [code for code, _ in weight_by_code.most_common(50)]
    top_codes.sort(key=lambda code: median(by_code[code]) if by_code[code] else 0)

    traces = []
    for code in top_codes:
        values = by_code[code]
        if not values:
            continue
        traces.append(
            {
                "name": code,
                "y": values,
                "type": "box",
                "boxpoints": "outliers",
                "jitter": 0.3,
                "pointpos": 0,
                "marker": {"size": 4},
                "line": {"width": 1.5},
                "fillcolor": "rgba(0,0,0,0)",
            }
        )

    return JsonResponse(
        {
            "year": current_year,
            "site": "AMJK",
            "product_group": "SW",
            "source": "Warship database via FastAPI shipped-products endpoint",
            "subtitle": f"AMJK · SW · YTD {current_year}",
            "note": "Top 50 products by shipped weight. Each box = product code. Sorted by median ¢/lb (low to high).",
            "traces": traces,
        }
    )
