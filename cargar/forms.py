from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from openpyxl.pivot.record import Record

from .models import Proveedor

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Ingresa tu Correo Electrónico", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Electrónico'}))
    first_name = forms.CharField(label="Ingresa tu Nombre", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(label="Ingresa tu Apellido", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}))


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['username'].label = 'Ingresa un nombre de usuario'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Se requiere menos de 150 caracteres .. Letras, números y signos como éstos solamente: @/./+/-/_ </small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].label = 'Ingresa una contraseña'
        self.fields['password1'].help_text = '<span class="form-text text-muted"><small>Tu contraseña no puede ser solamente números.<small></span>'
        #self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Tu contraseña no puede ser similar a la de otra persona.</li><li>Tu contraseña debe contener por lo menos 8 carateres.</li><li>Tu contraseña no puede ser una contraseña común.</li><li>Tu contraseña no puede ser solamente números.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirma Contraseña'
        self.fields['password2'].label = 'Repite tu contraseña'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña para validarla.</small></span>'



# Creo una Form de agregar Proveedores
class AddProveedorForm(forms.ModelForm):
    nombre_proveedor = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón Social Proveedor'}))
    vencimiento = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Días de Vencimiento'}))
    nombre_corto = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Corto del Proveedor'}))
    rut = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'RUT Proveedor'}))
    nombre_vendedor = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Vendedor'}))
    telefono_vendedor = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono del Vendedor'}))
    correo_vendedor = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Vendedor'}))
    correo_vendedor2 = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Vendedor_2'}))
    correo_pago = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Pago'}))
    tipo_flete = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tipo de Flete'}))
    transporte = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre del Transporte'}))

    class Meta:
        model = Proveedor
        exclude = ("user",)