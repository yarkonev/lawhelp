# Generated by Django 4.1.7 on 2023-04-12 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_case_number_case_number_case_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='gp_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='case',
            name='overall_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='court',
            name='zip_code',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='case',
            name='number',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
