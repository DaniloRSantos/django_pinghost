# Generated by Django 4.2.1 on 2023-05-27 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ph', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enderecobusca',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='enderecobusca',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]