from django import forms

from order_control.models import Client, Order, BoxTop, Payment


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'required': False})
        }
        fields = ('name', 'phone', 'cakeMaker', 'picture')


class OrderForm(forms.ModelForm):

    client = forms.ModelChoiceField(queryset=Client.objects.all(), label='Cliente')

    class Meta:
        model = Order
        localize = True,
        widgets = {
            'deliveryAt': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        fields = ('deliveryAt', 'delivered', 'description', 'downPayment', 'totalOrder', 'totalPayment', 'client')


class BoxTopForm(forms.ModelForm):

    class Meta:
        model = BoxTop
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'theme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tema'}),
            'birthdayName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Aniversariante'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição'}),
            'storedIn': forms.FileInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Foto'})
        }
        fields = ('type', 'theme','gift', 'birthdayName', 'amount', 'description', 'storedIn')


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'createAt': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        fields = ('createAt', 'type', 'amount', 'downPayment')