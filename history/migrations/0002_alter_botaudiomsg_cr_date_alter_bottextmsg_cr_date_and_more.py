# Generated by Django 4.2.7 on 2023-11-28 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botaudiomsg',
            name='cr_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='bottextmsg',
            name='cr_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='useraudiomsg',
            name='cr_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='usertextmsg',
            name='cr_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created at'),
        ),
    ]