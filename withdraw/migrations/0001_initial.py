# Generated by Django 5.0.2 on 2024-08-15 15:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankAccountNumber', models.CharField(max_length=255)),
                ('bankName', models.CharField(max_length=50)),
                ('phoneNumber', models.CharField(max_length=15)),
                ('selectedMethod', models.CharField(choices=[('bank', 'Bank Transfer'), ('crypto', 'Cryptocurrency')], max_length=20)),
                ('user_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraws', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
