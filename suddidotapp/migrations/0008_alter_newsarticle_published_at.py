# Generated by Django 5.1.6 on 2025-02-25 13:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suddidotapp', '0007_alter_newsarticle_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsarticle',
            name='published_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
