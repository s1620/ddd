# Generated by Django 2.2.6 on 2019-12-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comcom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(max_length=255, verbose_name='位置'),
        ),
    ]