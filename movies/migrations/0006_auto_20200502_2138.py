# Generated by Django 3.0.4 on 2020-05-02 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0005_movieperson_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='star',
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='value',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=1),
        ),
        migrations.DeleteModel(
            name='RatingStar',
        ),
    ]
