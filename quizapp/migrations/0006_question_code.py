# Generated by Django 3.1.3 on 2020-11-11 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0005_auto_20201111_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]