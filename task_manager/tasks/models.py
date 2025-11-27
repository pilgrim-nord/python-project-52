from django.db import models

# tasks/models.py

from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author_tasks',
        verbose_name="Автор"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor_tasks',
        verbose_name="Исполнитель",
        null=True, # Исполнитель может быть не назначен
        blank=True
    )
    status = models.ForeignKey(
        'statuses.Status',
        on_delete=models.PROTECT,
        verbose_name="Статус"
    )
    labels = models.ManyToManyField(
        'labels.Label',
        verbose_name="Метки",
        blank=True # Метки могут быть не назначены
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-created_at']