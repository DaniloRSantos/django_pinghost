# Generated by Django 4.2.1 on 2023-06-25 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ph', '0004_remove_hosts_endereco_enderecobusca_hosts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hosts',
            name='time_host',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]