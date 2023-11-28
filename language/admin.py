import os

from django.conf import settings
from django.contrib import admin

from language.models import LanguageModel

from gpt4all import GPT4All

# Register your models here.

@admin.action(description="Download selected models")
def get_model(modeladmin, request, queryset):
    # TODO: fix
    for record in queryset.iterator():
        model_type = record.type
        model_name = record.name
        model_dir = os.path.join(settings.MEDIA_ROOT, record._meta.get_field('file').upload_to)
        model_path = os.path.join(model_dir, model_name)
        if model_type == LanguageModel.CHOICE_GPT4ALL:
            GPT4All.download_model(model_name, model_path)
        if model_type == LanguageModel.CHOICE_BARK:
            pass
        else:
            pass

@admin.register(LanguageModel)
class LanguageModelAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "file", "cr_date"]

    ordering = ["type", "name"]
    date_hierarchy = 'cr_date'

    actions = [get_model]
