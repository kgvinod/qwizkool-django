# Generated by Django 3.1.4 on 2021-01-04 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20210103_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='attempted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='passed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
    ]
