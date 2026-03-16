from django.db import models


class PresentationCard(models.Model):
    title = models.CharField(max_length=200, default="Staff & Hours")
    product_group = models.CharField(max_length=50, default="SW")
    site = models.CharField(max_length=50, default="AMJK")
    report_date = models.DateField()
    generated_time = models.TimeField()

    supervisors = models.PositiveIntegerField(default=1)
    assistant_supervisors = models.PositiveIntegerField(default=1)
    office_staff = models.PositiveIntegerField(default=2)
    warehouse_leads = models.PositiveIntegerField(default=1)
    forklift_drivers = models.PositiveIntegerField(default=6)

    warehouse_workdays = models.CharField(max_length=100, default="Monday - Friday")
    warehouse_day_shift = models.CharField(max_length=100, default="7:00AM - 3:30PM")
    warehouse_night_shift = models.CharField(max_length=100, default="3:30PM - 12:00AM")

    shipping_workdays = models.CharField(max_length=100, default="Monday - Friday")
    shipping_day_shift = models.CharField(max_length=100, default="7:30AM - 4:30PM")
    shipping_night_shift = models.CharField(max_length=100, default="4:30PM - 1:00AM")
    shipping_note = models.TextField(
        default="Last two Saturdays of each month are designated as 8-hour workdays."
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]

    def __str__(self) -> str:
        return f"{self.site} - {self.title}"


class SafetyCard(models.Model):
    title = models.CharField(max_length=200, default="Safety")
    since_year = models.PositiveIntegerField(default=2021)
    organization_name = models.CharField(max_length=200, default="CFP Warehouse & Shipping")
    headline = models.CharField(max_length=200, default="ZERO Recordable Accidents")
    body = models.TextField(
        default=(
            "Our team's commitment to safety has kept every associate healthy and productive "
            "- day after day, year after year."
        )
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]

    def __str__(self) -> str:
        return self.title


class FreightAnalytics(models.Model):
    """Cache freight cost and weight analytics from Warship"""
    site = models.CharField(max_length=50, default="AMJK")
    product_group = models.CharField(max_length=50, default="SW")

    # Historic averages (2018-2025 avg)
    hist_avg_frt_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hist_avg_ttl_lbs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    hist_avg_cost_per_lb = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    # YTD (current year) values
    ytd_frt_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ytd_ttl_lbs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ytd_cost_per_lb = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    # Calculated deltas
    frt_amt_delta_pct = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # positive = better
    lbs_delta_pct = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cost_per_lb_delta_pct = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    last_synced = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_synced"]

    def __str__(self) -> str:
        return f"{self.site} {self.product_group} Freight Analytics"


class CarrierUsage(models.Model):
    """Cache carrier load distribution data from Warship"""
    site = models.CharField(max_length=50, default="AMJK")
    product_group = models.CharField(max_length=50, default="SW")

    # JSON dict: {"GILTNER-AM": 35.5, "AAL-AM": 23.2, ...}
    carrier_percentages = models.JSONField(default=dict)

    last_synced = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_synced"]

    def __str__(self) -> str:
        return f"{self.site} {self.product_group} Carrier Usage"
