# Generated by Django 4.2.7 on 2023-11-28 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0003_alter_languagemodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagemodel',
            name='file',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Model path'),
        ),
    ]
