# Generated by Django 4.2.2 on 2023-08-23 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_feature_minimum_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='feature',
            name='minimum_order',
            field=models.TextField(blank=True, max_length=150, verbose_name='최소 주문 기준'),
        ),
    ]