import os

from django.conf import settings
from django.contrib import admin, messages

from language.models import LanguageModel

from gpt4all import GPT4All

# Register your models here.

# TODO: Research Django constants best practices
MODELS_DIR = os.path.join(settings.MEDIA_ROOT, 'system', 'models')

@admin.action(description="Download selected models")
def get_model(modeladmin, request, queryset):
    # TODO: Move to asynch task
    if not queryset:
        msg = "Please select one or more models to install!"
        messages.add_message(request, messages.ERROR, msg)
        return None
    msg = ["The following models have been installed:"]
    modelsInstalled = 0
    for record in queryset.iterator():
        model_type = record.type
        model_name = record.name
        if not os.path.exists(MODELS_DIR):
            os.makedirs(MODELS_DIR)
        if model_type == LanguageModel.CHOICE_GPT4ALL:
            model_path = GPT4All.retrieve_model(model_name, MODELS_DIR).get('path')
            record.file = model_path
            record.save()
            msg += f"{model_name},"
        if model_type == LanguageModel.CHOICE_BARK:
            pass
        else:
            pass
    if modelsInstalled:
        msg = ' '.join(msg)
        messages.add_message(request, messages.SUCCESS, msg)
    else:
        msg = 'The selected models have not been installed!'
        messages.add_message(request, messages.WARNING, msg)

@admin.register(LanguageModel)
class LanguageModelAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "file", "cr_date"]

    ordering = ["type", "name"]
    date_hierarchy = 'cr_date'

    actions = [get_model]
