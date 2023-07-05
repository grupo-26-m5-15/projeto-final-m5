# Generated by Django 4.2.2 on 2023-07-05 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('copies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('devolution_date', models.DateTimeField()),
                ('copy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='copies.copy')),
            ],
        ),
    ]
