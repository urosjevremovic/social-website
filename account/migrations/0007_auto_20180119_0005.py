# Generated by Django 2.0.1 on 2018-01-19 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20180118_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='activation_key',
            field=models.CharField(max_length=35),
        ),
    ]