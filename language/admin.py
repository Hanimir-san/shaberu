import os

from django.conf import settings
from django.contrib import admin

from language.models import LanguageModel

from gpt4all import GPT4All

# Register your models here.

# TODO: Research Django constants best practices
MODELS_DIR = os.path.join(settings.MEDIA_ROOT, 'system', 'models')

@admin.action(description="Download selected models")
def get_model(modeladmin, request, queryset):
    # TODO: Move to asynch task
    for record in queryset.iterator():
        model_type = record.type
        model_name = record.name
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR)
        if model_type == LanguageModel.CHOICE_GPT4ALL:
            model_path = GPT4All.retrieve_model(model_name, MODELS_DIR).get('path')
            record.file = model_path
            record.save()
        if model_type == LanguageModel.CHOICE_BARK:
            pass
        else:
            pass
    # TODO: Show Django message upon finish

@admin.register(LanguageModel)
class LanguageModelAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "file", "cr_date"]

    ordering = ["type", "name"]
    date_hierarchy = 'cr_date'

    actions = [get_model]
