# Generated by Django 3.2.9 on 2021-11-06 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_document_documentfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knowledgebase',
            old_name='languages',
            new_name='language',
        ),
    ]