from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Имя')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
