from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from openpyxl.pivot.record import Record

from .models import Proveedor, TipoFlete, Transporte


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Ingresa tu Correo Electrónico", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Electrónico'}))
    first_name = forms.CharField(label="Ingresa tu Nombre", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(label="Ingresa tu Apellido", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}))

    # Nuevo campo para seleccionar el grupo
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),  # Cargar todos los grupos disponibles
        label="Selecciona el grupo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'group')

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

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirma Contraseña'
        self.fields['password2'].label = 'Repite tu contraseña'
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Ingresa la misma contraseña para validarla.</small></span>'

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
            group = self.cleaned_data['group']
            user.groups.add(group)  # Asignar el grupo seleccionado al usuario
        return user

# Creo una Form de agregar Proveedores
class AddProveedorForm(forms.ModelForm):
    nombre_proveedor = forms.CharField(label="", required=True,  max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Razón Social Proveedor'}))
    vencimiento = forms.CharField(label="",required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Días de Vencimiento'}))
    nombre_corto = forms.CharField(label="", required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Corto del Proveedor'}))
    rut = forms.CharField(label="", required=True, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'RUT Proveedor'}))
    nombre_vendedor = forms.CharField(label="", required=False,max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre Vendedor'}))
    telefono_vendedor = forms.CharField(label="", required=False,max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono del Vendedor'}))
    correo_vendedor = forms.CharField(label="", required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Vendedor'}))
    correo_vendedor2 = forms.CharField(label="", required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Vendedor_2'}))
    correo_pago = forms.CharField(label="", required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo Pago'}))

    tipo_flete = forms.ModelChoiceField(queryset=TipoFlete.objects.all(), empty_label="Selecciona un tipo de flete", widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'Tipo de Flete'}))
    transporte = forms.ModelChoiceField(queryset=Transporte.objects.all(), empty_label="Nombre del Transporte", widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tipo de Transporte'}))

    class Meta:
        model = Proveedor
        exclude = ("user",)

class ExcelUploadForm(forms.Form):
    archivo = forms.FileField(label="Archivo Excel")
    tipo = forms.ChoiceField(
        choices=[
            ('proveedor', 'Proveedores'),
            ('flete', 'Tipos de Flete'),
            ('transporte', 'Transportes')
        ],
        label="Tipo de dato"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['archivo'].widget.attrs['class'] = 'form-control'
        self.fields['tipo'].widget.attrs['class'] = 'form-select'
