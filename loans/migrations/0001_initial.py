# Generated by Django 4.2.2 on 2023-07-10 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('copies', '0001_initial'),
        ('libraries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('devolution_date', models.DateTimeField(null=True)),
                ('copy', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loan', to='copies.copy')),
                ('library', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loan', to='libraries.library')),
            ],
        ),
    ]