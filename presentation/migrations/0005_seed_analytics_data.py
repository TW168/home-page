from django.db import migrations
from decimal import Decimal


def seed_analytics(apps, schema_editor):
    FreightAnalytics = apps.get_model('presentation', 'FreightAnalytics')
    CarrierUsage = apps.get_model('presentation', 'CarrierUsage')
    
    # Seed FreightAnalytics with data matching the screenshot
    if not FreightAnalytics.objects.filter(site="AMJK", product_group="SW").exists():
        FreightAnalytics.objects.create(
            site="AMJK",
            product_group="SW",
            # Historic averages (2018-2025)
            hist_avg_frt_amt=Decimal("0.95"),  # $0.95M monthly avg
            hist_avg_ttl_lbs=Decimal("13.87"),  # 13.87M lbs monthly avg
            hist_avg_cost_per_lb=Decimal("7.66"),  # 7.66¢/lb
            # YTD 2026 values
            ytd_frt_amt=Decimal("0.84"),  # $0.84M
            ytd_ttl_lbs=Decimal("10.94"),  # 10.94M lbs
            ytd_cost_per_lb=Decimal("7.68"),  # 7.68¢/lb
            # Deltas (positive = better/lower cost)
            frt_amt_delta_pct=Decimal("11.8"),  # 11.8% better (lower cost)
            lbs_delta_pct=Decimal("-10.9"),  # 10.9% worse (less volume)
            cost_per_lb_delta_pct=Decimal("-1.0"),  # 1% worse (higher per-lb cost)
        )
    
    # Seed CarrierUsage with data matching the screenshot pie chart
    if not CarrierUsage.objects.filter(site="AMJK", product_group="SW").exists():
        carrier_data = {
            "GILTNER-AM": 35.5,
            "AAL-AM": 23.2,
            "CAL-AM": 12.8,
            "DRAKE-AM": 11.6,
            "PDI-AM": 9.23,
            "CHARGER-AM": 5.54,
            "TRAFFIX-AM": 0.0593,
            "CPU": 0.0593,
            "IP-TRUCK": 0.0593,
            "GEODIS": 0.356,
            "LAUBACH-T": 0.623,
            "SAIA-IP": 0.772,
        }
        CarrierUsage.objects.create(
            site="AMJK",
            product_group="SW",
            carrier_percentages=carrier_data,
        )


def reverse_analytics(apps, schema_editor):
    FreightAnalytics = apps.get_model('presentation', 'FreightAnalytics')
    CarrierUsage = apps.get_model('presentation', 'CarrierUsage')
    FreightAnalytics.objects.filter(site="AMJK", product_group="SW").delete()
    CarrierUsage.objects.filter(site="AMJK", product_group="SW").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('presentation', '0004_carrierusage_freightanalytics'),
    ]

    operations = [
        migrations.RunPython(seed_analytics, reverse_analytics),
    ]
