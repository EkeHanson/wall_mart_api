# Generated by Django 5.0.2 on 2024-08-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdraw',
            name='user_firstName',
            field=models.CharField(default='Hanson', max_length=100),
        ),
    ]
