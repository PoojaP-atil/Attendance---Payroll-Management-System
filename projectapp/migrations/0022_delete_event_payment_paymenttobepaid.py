# Generated by Django 4.2.7 on 2024-02-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0021_payment_month'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.AddField(
            model_name='payment',
            name='paymenttobepaid',
            field=models.FloatField(default=0),
        ),
    ]