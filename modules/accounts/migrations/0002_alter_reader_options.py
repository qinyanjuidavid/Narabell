# Generated by Django 4.1.1 on 2022-10-24 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reader",
            options={"ordering": ["-created_at"], "verbose_name_plural": "Readers"},
        ),
    ]
