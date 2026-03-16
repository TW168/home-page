from datetime import date, time

from django.db import migrations, models


def seed_presentation_card(apps, schema_editor):
    PresentationCard = apps.get_model("presentation", "PresentationCard")
    if PresentationCard.objects.exists():
        return

    PresentationCard.objects.create(
        title="Staff & Hours",
        product_group="SW",
        site="AMJK",
        report_date=date(2026, 3, 16),
        generated_time=time(13, 8),
        supervisors=1,
        assistant_supervisors=1,
        office_staff=2,
        warehouse_leads=1,
        forklift_drivers=6,
        warehouse_workdays="Monday - Friday",
        warehouse_day_shift="7:00AM - 3:30PM",
        warehouse_night_shift="3:30PM - 12:00AM",
        shipping_workdays="Monday - Friday",
        shipping_day_shift="7:30AM - 4:30PM",
        shipping_note="Last two Saturdays of each month are designated as 8-hour workdays.",
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PresentationCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Staff & Hours", max_length=200)),
                ("product_group", models.CharField(default="SW", max_length=50)),
                ("site", models.CharField(default="AMJK", max_length=50)),
                ("report_date", models.DateField()),
                ("generated_time", models.TimeField()),
                ("supervisors", models.PositiveIntegerField(default=1)),
                ("assistant_supervisors", models.PositiveIntegerField(default=1)),
                ("office_staff", models.PositiveIntegerField(default=2)),
                ("warehouse_leads", models.PositiveIntegerField(default=1)),
                ("forklift_drivers", models.PositiveIntegerField(default=6)),
                ("warehouse_workdays", models.CharField(default="Monday - Friday", max_length=100)),
                ("warehouse_day_shift", models.CharField(default="7:00AM - 3:30PM", max_length=100)),
                ("warehouse_night_shift", models.CharField(default="3:30PM - 12:00AM", max_length=100)),
                ("shipping_workdays", models.CharField(default="Monday - Friday", max_length=100)),
                ("shipping_day_shift", models.CharField(default="7:30AM - 4:30PM", max_length=100)),
                (
                    "shipping_note",
                    models.TextField(default="Last two Saturdays of each month are designated as 8-hour workdays."),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-updated_at", "id"]},
        ),
        migrations.RunPython(seed_presentation_card, migrations.RunPython.noop),
    ]