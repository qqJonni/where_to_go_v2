# Generated by Django 4.2.5 on 2023-09-24 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("places", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="placename",
            name="point_lat",
        ),
        migrations.RemoveField(
            model_name="placename",
            name="point_lon",
        ),
    ]
