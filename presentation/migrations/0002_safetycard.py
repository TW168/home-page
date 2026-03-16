from django.db import migrations, models


def seed_safety_card(apps, schema_editor):
    SafetyCard = apps.get_model("presentation", "SafetyCard")
    if SafetyCard.objects.exists():
        return

    SafetyCard.objects.create(
        title="Safety",
        since_year=2021,
        organization_name="CFP Warehouse & Shipping",
        headline="ZERO Recordable Accidents",
        body=(
            "Our team's commitment to safety has kept every associate healthy and productive "
            "- day after day, year after year."
        ),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("presentation", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SafetyCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Safety", max_length=200)),
                ("since_year", models.PositiveIntegerField(default=2021)),
                (
                    "organization_name",
                    models.CharField(default="CFP Warehouse & Shipping", max_length=200),
                ),
                (
                    "headline",
                    models.CharField(default="ZERO Recordable Accidents", max_length=200),
                ),
                (
                    "body",
                    models.TextField(
                        default=(
                            "Our team's commitment to safety has kept every associate healthy and productive "
                            "- day after day, year after year."
                        )
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-updated_at", "id"]},
        ),
        migrations.RunPython(seed_safety_card, migrations.RunPython.noop),
    ]