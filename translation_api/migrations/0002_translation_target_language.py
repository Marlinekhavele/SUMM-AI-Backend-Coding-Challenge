# Generated by Django 5.0.4 on 2024-08-15 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("translation_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="translation",
            name="target_language",
            field=models.CharField(default="English", max_length=50),
        ),
    ]
