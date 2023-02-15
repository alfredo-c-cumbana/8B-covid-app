# Generated by Django 4.0 on 2023-02-13 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='CovidCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=60)),
                ('country_code', models.CharField(max_length=3)),
                ('confirmed', models.CharField(max_length=5)),
                ('deaths', models.CharField(max_length=5)),
                ('recovered', models.CharField(max_length=5)),
                ('date', models.CharField(max_length=30)),
            ],
        ),
    ]
