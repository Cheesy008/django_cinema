# Generated by Django 3.0.4 on 2020-05-04 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20200503_2118'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='review',
            name='object_id',
        ),
        migrations.AddField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.Movie'),
        ),
    ]