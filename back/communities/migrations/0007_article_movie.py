# Generated by Django 4.2.16 on 2024-11-23 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
        ('communities', '0006_alter_article_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='movies.movie'),
        ),
    ]
