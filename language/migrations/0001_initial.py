# Generated by Django 4.2.7 on 2023-11-28 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cr_date', models.DateField(auto_now_add=True, verbose_name='Created at')),
                ('name', models.CharField(default='', max_length=50, verbose_name='Model name')),
                ('type', models.CharField(choices=[('GPT4ALL', 'Gpt4All'), ('BARK', 'Bark')], default='', max_length=20, verbose_name='Model type')),
                ('path', models.FileField(default='', upload_to='system/models/', verbose_name='Model path')),
            ],
            options={
                'verbose_name': 'Language model',
                'verbose_name_plural': 'Language models',
                'indexes': [models.Index(fields=['type'], name='language_la_type_b2bb1b_idx')],
            },
        ),
    ]