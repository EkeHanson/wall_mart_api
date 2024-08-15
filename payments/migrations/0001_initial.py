# Generated by Django 5.0.2 on 2024-08-15 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=20)),
                ('recipient_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoWalletDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_type', models.CharField(choices=[('USDT', 'USDT'), ('BINANCE', 'Binance'), ('TON', 'TON'), ('BTC', 'Bitcoin'), ('TRX', 'TRON'), ('TRC20', 'TRC20')], max_length=20)),
                ('wallet_address', models.CharField(max_length=255)),
            ],
        ),
    ]
