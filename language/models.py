import os

from django.db import models
from django.urls import reverse

from home.models import Timestamp


# Create your models here.
class LanguageModel(Timestamp):

    CHOICE_BLANK = ''
    CHOICE_GPT4ALL = "GPT4ALL"
    CHOICE_BARK = "BARK"
    CHOICES_TYPE = (
        (CHOICE_GPT4ALL, "Gpt4All"),
        (CHOICE_BARK, "Bark")
      )

    name = models.CharField(max_length=50, verbose_name="Model name", blank=False, default='')
    type = models.CharField(max_length=20, choices=CHOICES_TYPE, verbose_name="Model type", blank=False, default=CHOICE_BLANK)
    file = models.CharField(max_length=255, verbose_name="Model path", blank=True, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("language-model", args=[str(self.id)])
    
    class Meta:
        indexes = [models.Index(fields=["type"])]
        verbose_name = "Language model"
        verbose_name_plural = "Language models"
