# Generated by Django 3.1.3 on 2020-11-16 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='participant_list',
            new_name='participants',
        ),
    ]