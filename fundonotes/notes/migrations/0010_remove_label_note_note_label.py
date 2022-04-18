# Generated by Django 4.0.2 on 2022-04-18 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_alter_label_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='note',
        ),
        migrations.AddField(
            model_name='note',
            name='label',
            field=models.ManyToManyField(related_name='labels', to='notes.Label'),
        ),
    ]