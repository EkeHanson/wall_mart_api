# Generated by Django 5.0.2 on 2024-08-16 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recharge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recharge',
            name='user_firstName',
            field=models.CharField(default='Hanson', max_length=100),
        ),
    ]