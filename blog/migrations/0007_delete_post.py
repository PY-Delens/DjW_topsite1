# Generated by Django 3.0.5 on 2020-04-11 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
