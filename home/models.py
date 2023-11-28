from django.db import models
from django.urls import reverse

# Create your models here.


class Timestamp(models.Model):

    cr_date = models.DateField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        abstract = True
