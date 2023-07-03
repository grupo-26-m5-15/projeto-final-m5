# Generated by Django 4.2.2 on 2023-07-03 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copy',
            name='quantity',
        ),
        migrations.AddField(
            model_name='copy',
            name='availability',
            field=models.BooleanField(default=True),
        ),
    ]
