# Generated by Django 3.0 on 2019-12-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('func5api', '0007_auto_20191226_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aid', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20)),
                ('student_number', models.CharField(max_length=10)),
            ],
        ),
    ]