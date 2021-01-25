# Generated by Django 3.1.5 on 2021-01-25 20:18

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movie_cat', '0002_auto_20210126_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=modelcluster.fields.ParentalManyToManyField(related_name='film_actor', to='movie_cat.Actor', verbose_name='актеры'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='directors',
            field=modelcluster.fields.ParentalManyToManyField(related_name='film_director', to='movie_cat.Actor', verbose_name='режиссер'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genres',
            field=modelcluster.fields.ParentalManyToManyField(to='movie_cat.Genre', verbose_name='жанры'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='movie_category',
            field=modelcluster.fields.ParentalManyToManyField(to='movie_cat.Category', verbose_name='Категория'),
        ),
    ]
