import django_filters
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label=_('Статус'))
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label=_('Исполнитель'))
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all(), label=_('Метка'))
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Только свои задачи'),
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_self_tasks(self, queryset, name, value):
        if value and self.request:
            return queryset.filter(author=self.request.user)
        return queryset
