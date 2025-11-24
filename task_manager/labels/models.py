from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "Метки"
        ordering = ['created_at']