# Generated by Django 4.0.4 on 2022-06-24 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellHouse', '0009_alter_apartment_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='category',
            field=models.CharField(choices=[('Rent', 'Rent'), ('Sale', 'Sale')], max_length=5),
        ),
    ]
