# Generated by Django 2.2 on 2020-11-09 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote_dash_app', '0003_quotepost_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]