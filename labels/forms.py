from django import forms

from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {'name': 'Имя'}
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
        }
