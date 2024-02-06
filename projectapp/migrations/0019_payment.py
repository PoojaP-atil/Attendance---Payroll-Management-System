# Generated by Django 4.2.7 on 2024-02-05 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0018_leaverequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentstatus', models.CharField(default='pending', max_length=100)),
                ('transactionid', models.CharField(max_length=200)),
                ('paymentmode', models.CharField(default='paypal', max_length=100)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectapp.employee')),
            ],
            options={
                'db_table': 'payment',
            },
        ),
    ]
