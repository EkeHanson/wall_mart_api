# Generated by Django 5.0.2 on 2024-08-19 20:11

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
                ('bank_name', models.CharField(default='Banco Prepago Tenpo', max_length=100)),
                ('account_number', models.CharField(default='111119469406', max_length=20)),
                ('recipient_name', models.CharField(default='Gonsalo Osvaldo Cornejo Rivero', max_length=100)),
                ('ruth', models.CharField(default=1946399, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='CryptoWalletDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_type', models.CharField(choices=[('USDT', 'USDT'), ('BINANCE', 'Binance'), ('TON', 'TON'), ('BTC', 'Bitcoin'), ('TRX', 'TRON'), ('TRC20', 'TRC20')], max_length=20, unique=True)),
                ('wallet_address', models.CharField(max_length=255)),
            ],
        ),
    ]
