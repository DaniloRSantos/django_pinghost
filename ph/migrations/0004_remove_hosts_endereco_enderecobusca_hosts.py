# Generated by Django 4.2 on 2023-06-17 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ph', '0003_hosts_ip_host'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hosts',
            name='endereco',
        ),
        migrations.AddField(
            model_name='enderecobusca',
            name='hosts',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ph.hosts'),
            preserve_default=False,
        ),
    ]
