# Generated by Django 2.2.6 on 2019-11-01 23:16

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20191027_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='is_processed',
            field=models.BooleanField(default=0),
        ),
    ]
