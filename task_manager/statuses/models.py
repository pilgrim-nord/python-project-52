from django.db import models
from django.urls import reverse


# Create your models here.
class Status(models.Model):
    name = models.CharField("Имя", max_length=100)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('statuses:list')

    class Meta:
        ordering = ['name']
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'