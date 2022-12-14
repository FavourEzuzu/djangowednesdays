# Generated by Django 4.1 on 2022-08-22 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0002_clubuser_venue_event_attendees_alter_event_venue"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venue",
            name="email_address",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="Email Address"
            ),
        ),
        migrations.AlterField(
            model_name="venue",
            name="phone",
            field=models.CharField(
                blank=True, max_length=15, verbose_name="Phone contact"
            ),
        ),
        migrations.AlterField(
            model_name="venue",
            name="web",
            field=models.URLField(blank=True, verbose_name="Website Address"),
        ),
    ]
