# Generated by Django 4.2.2 on 2023-08-23 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='minimum_pay',
            field=models.PositiveSmallIntegerField(verbose_name='최소 주문 금액'),
        ),
    ]
