# Generated by Django 2.1.7 on 2019-04-25 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='video_game',
            field=models.CharField(choices=[('PES', 'Pro-Soccer 2019'), ('LoL', 'League of Legends'), ('CS', 'Counter Strike'), ('SF5', 'Street Fighter V')], max_length=3),
        ),
    ]
