# Generated by Django 3.0 on 2019-12-26 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('func5api', '0006_auto_20191225_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fix',
            name='status',
            field=models.CharField(choices=[('未處理', '未處理'), ('已處理', '已處理')], default='未處理', max_length=10),
        ),
    ]