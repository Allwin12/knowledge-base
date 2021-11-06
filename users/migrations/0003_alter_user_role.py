# Generated by Django 3.2.9 on 2021-11-03 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211103_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('AUTHOR', 'Author'), ('REVIEWER', 'Reviewer'), ('ANALYST', 'Analyst'), ('CUSTOMER', 'Customer')], max_length=20),
        ),
    ]
