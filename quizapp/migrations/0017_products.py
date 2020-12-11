# Generated by Django 3.1.3 on 2020-11-18 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0016_delete_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('cleanser', models.CharField(max_length=100)),
                ('moisturizer', models.CharField(max_length=100)),
                ('serum', models.CharField(max_length=100)),
            ],
        ),
    ]
