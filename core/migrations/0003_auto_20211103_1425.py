# Generated by Django 3.2.9 on 2021-11-03 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_knowledgebase'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='knowledgebase',
            name='customers',
            field=models.ManyToManyField(limit_choices_to={'role': 'CUSTOMER'}, related_name='customers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='knowledgebase',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
    ]
