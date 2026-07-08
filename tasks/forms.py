from django import forms
from django.contrib.auth.models import User

from .models import Task


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username


class TaskForm(forms.ModelForm):
    executor = UserModelChoiceField(queryset=User.objects.all(), label='Исполнитель')

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Описание', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'labels': forms.SelectMultiple(attrs={'size': 6, 'class': 'form-control'}),
        }
