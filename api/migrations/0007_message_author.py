# Generated by Django 3.1.1 on 2020-10-04 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20201001_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.CharField(default='', max_length=255),
        ),
    ]
