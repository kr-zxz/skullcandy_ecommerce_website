# Generated by Django 5.0.4 on 2024-05-19 14:15

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('date_of_order', models.DateField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateField()),
                ('date_of_delivery', models.DateField(null=True)),
                ('status', models.CharField(choices=[('can be satisfied', 'Out for Delivery'), ('stock not available', 'Out of stock')], default='no response', max_length=20)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.supplier')),
            ],
        ),
    ]
