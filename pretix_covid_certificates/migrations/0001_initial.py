# Generated by Django 3.2.2 on 2021-06-14 12:24

import django.db.models.deletion
import pretix.base.models.base
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pretixbase", "0193_auto_20210611_1355"),
    ]

    operations = [
        migrations.CreateModel(
            name="CovidCertificateExpiry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("expiry", models.DateTimeField(db_index=True)),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="CovidCertificateExpiry",
                        to="pretixbase.questionanswer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, pretix.base.models.base.LoggingMixin),
        ),
    ]
