from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from home.models import Timestamp
from language.models import LanguageModel


class TextMsg(models.Model):

    text = models.TextField(blank=True, default='', verbose_name="Message")

    class Meta:
        abstract = True


class AudioMsg(models.Model):

    path = models.FileField(upload_to="system/audio-msgs/", blank=False, default='', verbose_name="Model path")

    class Meta:
        abstract = True


class UserTextMsg(TextMsg, Timestamp):

    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_user', null=True, blank=True, verbose_name="User")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("user-msg", args=[str(self.id)])
    
    class Meta:
        indexes = [models.Index(fields=["user"]), models.Index(fields=["text"])]
        verbose_name = "User text message"
        verbose_name_plural = "User text messages"


class BotTextMsg(TextMsg, Timestamp):

    model = models.ForeignKey(to=LanguageModel, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_language_model', null=True, blank=True, verbose_name="Language model")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("user-msg", args=[str(self.id)])
    
    class Meta:
        indexes = [models.Index(fields=["model"]), models.Index(fields=["text"])]
        verbose_name = "Bot text message"
        verbose_name_plural = "Bot text messages"


class UserAudioMsg(AudioMsg, Timestamp):

    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_user', null=True, blank=True, verbose_name="User")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("user-msg", args=[str(self.id)])
    
    class Meta:
        indexes = [models.Index(fields=["user"])]
        verbose_name = "User audio message"
        verbose_name_plural = "User audio messages"


class BotAudioMsg(AudioMsg, Timestamp):

    model = models.ForeignKey(to=LanguageModel, on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_language_model', null=True, blank=True, verbose_name="Language model")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("user-msg", args=[str(self.id)])
    
    class Meta:
        indexes = [models.Index(fields=["model"])]
        verbose_name = "Bot audio message"
        verbose_name_plural = "Bot audio messages"
