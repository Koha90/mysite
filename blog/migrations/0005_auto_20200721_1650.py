# Generated by Django 3.0.8 on 2020-07-21 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='update',
            new_name='updated',
        ),
    ]
