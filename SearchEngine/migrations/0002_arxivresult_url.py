# Generated by Django 4.2.4 on 2023-08-09 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SearchEngine", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="arxivresult",
            name="url",
            field=models.URLField(default="https://example.com"),
        ),
    ]
