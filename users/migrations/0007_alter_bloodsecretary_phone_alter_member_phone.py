# Generated by Django 4.2.17 on 2025-02-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_bloodsecretary_phone_member_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodsecretary',
            name='phone',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
