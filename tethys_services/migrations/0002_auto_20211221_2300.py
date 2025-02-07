# Generated by Django 3.2.10 on 2021-12-21 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tethys_services", "0001_initial_30"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datasetservice",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="persistentstoreservice",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="spatialdatasetservice",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="webprocessingservice",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
