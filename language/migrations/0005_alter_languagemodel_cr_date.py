# Generated by Django 4.2.7 on 2023-11-28 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0004_alter_languagemodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='languagemodel',
            name='cr_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
    ]