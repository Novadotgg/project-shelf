# Generated by Django 5.2.2 on 2025-06-07 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pshelf', '0002_creatorproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorproject',
            name='case_study',
            field=models.TextField(blank=True, null=True),
        ),
    ]
