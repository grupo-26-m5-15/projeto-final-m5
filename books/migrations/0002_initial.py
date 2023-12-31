# Generated by Django 4.2.2 on 2023-07-10 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_ratings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='following',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='books.book'),
        ),
        migrations.AddField(
            model_name='following',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ManyToManyField(related_name='books', through='books.Following', to=settings.AUTH_USER_MODEL),
        ),
    ]
