# Generated by Django 4.2.1 on 2023-06-25 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ph', '0007_alter_enderecobusca_host_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enderecobusca',
            old_name='host_id',
            new_name='host',
        ),
    ]
