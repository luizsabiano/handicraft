from django import forms

from order_control.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'required': False})
        }
        fields = ('name', 'phone', 'cakeMaker', 'picture')
