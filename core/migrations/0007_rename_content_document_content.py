# Generated by Django 3.2.9 on 2021-11-04 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_article_type_document_doc_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='Content',
            new_name='content',
        ),
    ]