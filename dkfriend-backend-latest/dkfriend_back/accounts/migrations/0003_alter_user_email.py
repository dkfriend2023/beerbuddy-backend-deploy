# Generated by Django 4.2.2 on 2023-09-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_kakao_id_user_like_restaurant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=40, unique=True),
        ),
    ]
