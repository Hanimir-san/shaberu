# Generated by Django 4.2.7 on 2023-11-29 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0006_languagemodel_is_default_alter_languagemodel_file_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='languagemodel',
            constraint=models.UniqueConstraint(fields=('name', 'type'), name='Unique named model'),
        ),
    ]