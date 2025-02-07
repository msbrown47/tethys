# Generated by Django 2.2.14 on 2021-12-20 23:07

from django.db import migrations
from django.utils import timezone
from ..models import SettingsCategory, Setting


NEW_SETTINGS = (
    (
        "Custom Templates",
        [
            "Login Page Template",
            "Register Page Template",
            "User Page Template",
            "User Settings Page Template",
        ],
    ),
    (
        "Custom Styles",
        [
            "Accounts Base CSS",
            "Login CSS",
            "Register CSS",
            "User Base CSS",
        ],
    ),
)


def add_new_settings(apps, schema_editor):
    """
    Add new settings for Tethys 4.0
    """

    # Add New settings
    now = timezone.now()
    for category_name, settings in NEW_SETTINGS:
        category = SettingsCategory.objects.get(name=category_name)
        for setting_name in settings:
            try:
                category.setting_set.get(name=setting_name)
            except Setting.DoesNotExist:
                category.setting_set.create(
                    name=setting_name, content="", date_modified=now
                )

        category.save()


def remove_new_settings(apps, schema_editor):
    for category_name, settings in NEW_SETTINGS:
        category = SettingsCategory.objects.get(name=category_name)
        for setting_name in settings:
            try:
                setting = category.setting_set.get(name=setting_name)
                setting.delete()
            except Setting.DoesNotExist:
                pass

        category.save()


class Migration(migrations.Migration):

    dependencies = [
        ("tethys_config", "0004_auto_20211221_2300"),
    ]

    operations = [migrations.RunPython(add_new_settings, remove_new_settings)]
