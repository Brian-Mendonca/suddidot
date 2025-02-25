# Generated by Django 5.1.6 on 2025-02-24 20:21

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suddidotapp', '0004_newsarticle_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('upvotes', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('news_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='suddidotapp.newsarticle')),
            ],
        ),
    ]
