# Generated by Django 5.1.4 on 2025-01-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolDiaryApp', '0004_alter_announcements_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
