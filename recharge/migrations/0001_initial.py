# Generated by Django 5.0.2 on 2024-08-15 19:43

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
            name='Recharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_name', models.CharField(max_length=255)),
                ('recharge_method', models.CharField(choices=[('bank_transfer', 'Bank Transfer'), ('credit_card', 'Credit Card'), ('mobile_payment', 'Mobile Payment'), ('crypto', 'Cryptocurrency')], max_length=20)),
                ('payment_id', models.CharField(editable=False, max_length=100, unique=True)),
                ('user_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('amount_top_up', models.DecimalField(decimal_places=2, max_digits=10)),
                ('receipt_image', models.ImageField(blank=True, null=True, upload_to='receipts/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recharges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
