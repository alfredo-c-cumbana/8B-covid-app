# Generated by Django 4.0 on 2023-02-13 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('restapi', '0002_country_user_alter_covidcase_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='covidcase',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country', to='restapi.country'),
        ),
    ]
