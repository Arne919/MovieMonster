# Generated by Django 4.2.16 on 2024-11-18 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='movie',
            name='trailer_url',
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_id',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='movie',
            name='actors',
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(related_name='movies', to='movies.actor'),
        ),
    ]
