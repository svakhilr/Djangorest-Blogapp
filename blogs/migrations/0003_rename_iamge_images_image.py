# Generated by Django 4.1.7 on 2023-03-04 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='iamge',
            new_name='image',
        ),
    ]