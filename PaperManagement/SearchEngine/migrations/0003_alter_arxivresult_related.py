# Generated by Django 4.2.4 on 2023-08-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SearchEngine', '0002_arxivresult_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arxivresult',
            name='related',
            field=models.TextField(default=''),
        ),
    ]
