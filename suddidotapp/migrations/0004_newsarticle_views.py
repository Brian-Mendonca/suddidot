# Generated by Django 5.1.6 on 2025-02-20 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suddidotapp', '0003_alter_newsarticle_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='views',
            field=models.IntegerField(default=1),
        ),
    ]
