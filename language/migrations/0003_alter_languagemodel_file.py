# Generated by Django 4.2.7 on 2023-11-28 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0002_rename_path_languagemodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagemodel',
            name='file',
            field=models.FileField(blank=True, default='', upload_to='system/models/', verbose_name='Model path'),
        ),
    ]
