from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
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
            'executor': forms.Select(attrs={'class': 'form-control'}),
            'labels': forms.SelectMultiple(attrs={'size': 6, 'class': 'form-control'}),
        }
