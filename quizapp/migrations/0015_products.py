# Generated by Django 3.1.3 on 2020-11-18 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0014_auto_20201117_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
    ]
