from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField("Имя", max_length=100)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return self.name