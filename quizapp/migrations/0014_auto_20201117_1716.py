# Generated by Django 3.1.3 on 2020-11-17 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0013_auto_20201117_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concerns',
            name='is_primary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_primary', to='quizapp.category'),
        ),
    ]
