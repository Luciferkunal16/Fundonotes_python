# Generated by Django 4.0.2 on 2022-04-18 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0010_remove_label_note_note_label'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='label',
            new_name='label_name',
        ),
    ]