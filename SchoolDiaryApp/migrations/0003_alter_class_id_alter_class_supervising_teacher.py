# Generated by Django 5.1.4 on 2025-01-03 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolDiaryApp', '0002_alter_school_id_alter_student_class_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='class',
            name='supervising_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supervising_teacher', to='SchoolDiaryApp.teacher'),
        ),
    ]