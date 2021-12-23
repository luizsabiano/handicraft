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
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do Pedido'}),
        }
        fields = ('deliveryAt', 'delivered', 'description', 'downPayment', 'totalOrder', 'totalPayment', 'client')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # add v-model to each model field
            field.widget.attrs.update({'v-model': name})


class BoxTopForm(forms.ModelForm):

    class Meta:
        model = BoxTop
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control', 'v-model': 'type'}),
            'theme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tema'}),
            'birthdayName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Aniversariante'}),
            'storedIn': forms.FileInput(attrs={'@change': 'previewFiles',
                                               'class': 'form-control',
                                               'required': False,
                                               'placeholder': 'Foto',
                                                'accept': 'image/jpeg, image/png'}),
            'gift': forms.CheckboxInput(attrs={':checked': 'isGift()'})
        }
        fields = ('type', 'theme', 'gift', 'birthdayName', 'amount', 'storedIn')

    def __init__(self, *args, **kwargs):
        super(BoxTopForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # add v-model to each model field
            if name != "storedIn":
                field.widget.attrs.update({'v-model': name})


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'createAt': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        fields = ('createAt', 'type', 'amount', 'downPayment')