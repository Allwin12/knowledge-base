# Generated by Django 3.2.9 on 2021-11-04 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20211103_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='article_type',
            new_name='doc_type',
        ),
    ]
