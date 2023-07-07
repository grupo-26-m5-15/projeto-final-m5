# Generated by Django 4.2.2 on 2023-07-06 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('libraries', '0001_initial'),
        ('books', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userlibraryblock',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libraries_blocked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='libraryemployee',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libraries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='libraryemployee',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='libraries.library'),
        ),
        migrations.AddField(
            model_name='librarybooks',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libraries', to='books.book'),
        ),
        migrations.AddField(
            model_name='librarybooks',
            name='library',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='libraries.library'),
        ),
    ]
