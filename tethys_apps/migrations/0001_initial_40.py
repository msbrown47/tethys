# Generated by Django 3.2.12 on 2022-08-12 16:39
# flake8: noqa

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import tethys_apps.base.mixins
import tethys_services.models


class Migration(migrations.Migration):

    replaces = [
        ("tethys_apps", "0001_initial_30"),
        ("tethys_apps", "0002_auto_20200326_1657"),
        ("tethys_apps", "0003_auto_20201209_0432"),
        ("tethys_apps", "0004_auto_20211221_2300"),
        ("tethys_apps", "0005_schedulersetting"),
        ("tethys_apps", "0006_app_order"),
    ]

    initial = True

    dependencies = [
        ("tethys_services", "0001_initial_40"),
        ("tethys_compute", "0001_initial_40"),
    ]

    operations = [
        migrations.CreateModel(
            name="TethysApp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("package", models.CharField(default="", max_length=200, unique=True)),
                ("name", models.CharField(default="", max_length=200)),
                (
                    "description",
                    models.TextField(blank=True, default="", max_length=1000),
                ),
                ("enable_feedback", models.BooleanField(default=False)),
                (
                    "feedback_emails",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True, max_length=200, null=True
                        ),
                        default=list,
                        size=None,
                    ),
                ),
                ("tags", models.CharField(blank=True, default="", max_length=200)),
                ("index", models.CharField(default="", max_length=200)),
                ("icon", models.CharField(default="", max_length=200)),
                ("root_url", models.CharField(default="", max_length=200)),
                ("color", models.CharField(default="", max_length=10)),
                ("enabled", models.BooleanField(default=True)),
                ("show_in_apps_library", models.BooleanField(default=True)),
                ("order", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Tethys App",
                "verbose_name_plural": "Installed Apps",
            },
            bases=(models.Model, tethys_apps.base.mixins.TethysBaseMixin),
        ),
        migrations.CreateModel(
            name="TethysAppSetting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=200)),
                (
                    "description",
                    models.TextField(blank=True, default="", max_length=1000),
                ),
                ("required", models.BooleanField(default=True)),
                ("initializer", models.CharField(default="", max_length=1000)),
                ("initialized", models.BooleanField(default=False)),
                (
                    "tethys_app",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="settings_set",
                        to="tethys_apps.tethysapp",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WebProcessingServiceSetting",
            fields=[
                (
                    "tethysappsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tethys_apps.tethysappsetting",
                    ),
                ),
                (
                    "web_processing_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tethys_services.webprocessingservice",
                    ),
                ),
            ],
            bases=("tethys_apps.tethysappsetting",),
        ),
        migrations.CreateModel(
            name="SpatialDatasetServiceSetting",
            fields=[
                (
                    "tethysappsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tethys_apps.tethysappsetting",
                    ),
                ),
                (
                    "engine",
                    models.CharField(
                        choices=[
                            (
                                "tethys_dataset_services.engines.GeoServerSpatialDatasetEngine",
                                "GeoServer",
                            ),
                            ("thredds-engine", "THREDDS"),
                        ],
                        default="tethys_dataset_services.engines.GeoServerSpatialDatasetEngine",
                        max_length=200,
                    ),
                ),
                (
                    "spatial_dataset_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tethys_services.spatialdatasetservice",
                    ),
                ),
            ],
            bases=("tethys_apps.tethysappsetting",),
        ),
        migrations.CreateModel(
            name="PersistentStoreDatabaseSetting",
            fields=[
                (
                    "tethysappsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tethys_apps.tethysappsetting",
                    ),
                ),
                ("spatial", models.BooleanField(default=False)),
                ("dynamic", models.BooleanField(default=False)),
                (
                    "persistent_store_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tethys_services.persistentstoreservice",
                    ),
                ),
            ],
            bases=("tethys_apps.tethysappsetting",),
        ),
        migrations.CreateModel(
            name="PersistentStoreConnectionSetting",
            fields=[
                (
                    "tethysappsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tethys_apps.tethysappsetting",
                    ),
                ),
                (
                    "persistent_store_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tethys_services.persistentstoreservice",
                    ),
                ),
            ],
            bases=("tethys_apps.tethysappsetting",),
        ),
        migrations.CreateModel(
            name="DatasetServiceSetting",
            fields=[
                (
                    "tethysappsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tethys_apps.tethysappsetting",
                    ),
                ),
                (
                    "engine",
                    models.CharField(
                        choices=[
                            (
                                "tethys_dataset_services.engines.CkanDatasetEngine",
                                "CKAN",
                            ),
                            (
                                "tethys_dataset_services.engines.HydroShareDatasetEngine",
                                "HydroShare",
                            ),
                        ],
                        default="tethys_dataset_services.engines.CkanDatasetEngine",
                        max_length=200,
                    ),
                ),
                (
                    "dataset_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tethys_services.datasetservice",
                    ),
                ),
            ],
            bases=("tethys_apps.tethysappsetting",),
        ),
        migrations.CreateModel(
            name="CustomSetting",
            fields=[
                (
                    "tethysappsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tethys_apps.tethysappsetting",
                    ),
                ),
                ("value", models.CharField(blank=True, default="", max_length=1024)),
                ("default", models.CharField(blank=True, default="", max_length=1024)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("STRING", "String"),
                            ("INTEGER", "Integer"),
                            ("FLOAT", "Float"),
                            ("BOOLEAN", "Boolean"),
                            ("UUID", "UUID"),
                        ],
                        default="STRING",
                        max_length=200,
                    ),
                ),
            ],
            bases=("tethys_apps.tethysappsetting",),
        ),
        migrations.CreateModel(
            name="TethysExtension",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("package", models.CharField(default="", max_length=200, unique=True)),
                ("name", models.CharField(default="", max_length=200)),
                (
                    "description",
                    models.TextField(blank=True, default="", max_length=1000),
                ),
                ("root_url", models.CharField(default="", max_length=200)),
                ("enabled", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Tethys Extension",
                "verbose_name_plural": "Installed Extensions",
            },
            bases=(models.Model, tethys_apps.base.mixins.TethysBaseMixin),
        ),
        migrations.CreateModel(
            name="SchedulerSetting",
            fields=[
                (
                    "tethysappsetting_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tethys_apps.tethysappsetting",
                    ),
                ),
                (
                    "engine",
                    models.CharField(
                        choices=[("htcondor", "HTCondor"), ("dask", "Dask")],
                        default="htcondor",
                        max_length=200,
                    ),
                ),
                (
                    "scheduler_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tethys_compute.scheduler",
                    ),
                ),
            ],
            bases=("tethys_apps.tethysappsetting",),
        ),
        migrations.CreateModel(
            name="ProxyApp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "endpoint",
                    models.CharField(
                        max_length=1024,
                        validators=[tethys_services.models.validate_url],
                    ),
                ),
                (
                    "logo_url",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        validators=[tethys_services.models.validate_url],
                    ),
                ),
                ("description", models.TextField(blank=True, max_length=2048)),
                ("tags", models.CharField(blank=True, default="", max_length=200)),
                ("enabled", models.BooleanField(default=True)),
                ("show_in_apps_library", models.BooleanField(default=True)),
                ("order", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Proxy App",
                "verbose_name_plural": "Proxy Apps",
            },
        ),
    ]
