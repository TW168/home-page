from django.contrib import admin

from .models import PresentationCard, SafetyCard, FreightAnalytics, CarrierUsage


@admin.register(PresentationCard)
class PresentationCardAdmin(admin.ModelAdmin):
    list_display = ("title", "site", "product_group", "report_date", "generated_time", "updated_at")
    search_fields = ("title", "site", "product_group")
    ordering = ("-updated_at",)


@admin.register(SafetyCard)
class SafetyCardAdmin(admin.ModelAdmin):
    list_display = ("title", "since_year", "organization_name", "headline", "updated_at")
    search_fields = ("title", "organization_name", "headline")
    ordering = ("-updated_at",)


@admin.register(FreightAnalytics)
class FreightAnalyticsAdmin(admin.ModelAdmin):
    list_display = ("site", "product_group", "ytd_frt_amt", "ytd_ttl_lbs", "frt_amt_delta_pct", "last_synced")
    search_fields = ("site", "product_group")
    ordering = ("-last_synced",)
    readonly_fields = ("last_synced",)


@admin.register(CarrierUsage)
class CarrierUsageAdmin(admin.ModelAdmin):
    list_display = ("site", "product_group", "last_synced")
    search_fields = ("site", "product_group")
    ordering = ("-last_synced",)
    readonly_fields = ("last_synced",)
