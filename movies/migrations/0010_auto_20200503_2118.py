# Generated by Django 3.0.4 on 2020-05-03 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_auto_20200503_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.PositiveSmallIntegerField(choices=[(5, 'Excellent'), (4, 'Very Good'), (3, 'Good'), (2, 'Average'), (1, 'Poor')], default=1),
        ),
    ]