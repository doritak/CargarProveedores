from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddProveedorForm, ExcelUploadForm
from .models import Proveedor, TipoFlete, Transporte
import pandas as pd
import logging

from django.db.models import Case, When, Value, IntegerField, Q

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    # validar si el usuario está loggeado (login)
    # username = request.session.get('username')  # Obtiene el nombre desde la sesión

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Autentificarse
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username  # Guarda el nombre en la sesión
            messages.success(request, "Bienvenido, has ingresado correctamente..")
            return redirect('index')
        else:
            messages.success(request, "Hay un error en el ingreso.. ")
            return redirect('index')
    return render(request, 'index.html')


def proveedores(request):
    search_query = request.GET.get('search', '')  # Captura el término de búsqueda
    order = request.GET.get('order', 'asc')       # Captura el orden (asc o desc)

    # Obtiene todos los proveedores
    provee = Proveedor.objects.all()

    # Filtrado por nombre de proveedor o nombre de vendedor
    if search_query:
        provee = provee.filter(
            Q(nombre_corto__icontains=search_query) |  # Búsqueda en nombre del proveedor
            Q(nombre_vendedor__icontains=search_query)  # Búsqueda en nombre del vendedor
        )

    # Anotación para detectar campos vacíos
    provee = provee.annotate(
        is_empty=Case(
            When(nombre_corto='', then=Value(1)),  # Si está vacío, asigna 1
            default=Value(0),  # Si NO está vacío, asigna 0
            output_field=IntegerField()
        )
    )

    # Ordenamiento final
    if order == 'desc':
        provee = provee.order_by('is_empty', '-nombre_corto')  # Vacíos al final en orden descendente
    else:
        provee = provee.order_by('is_empty', 'nombre_corto')   # Vacíos al final en orden ascendente

    return render(request, 'proveedores.html', {
        'proveedores': provee,
        'search_query': search_query,
        'order': order
    })

# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request, "Hasta luego, has salido de con Logout.. ")
    return redirect('index')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username =  form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Te has registrado correctamente!")
            return render(request, 'index.html',{'user':username})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form': form})

def proveedor_record(request, pk):
    if request.user.is_authenticated:
        record = Proveedor.objects.get(id=pk)
        return render(request, 'record.html', {'proveedor_record': record})
    else:
        messages.success(request, "Tiene que acceder primero con Login...")
        return redirect('index')

def delete_proveedor(request,pk):
    if request.user.is_authenticated:
        delete_it = get_object_or_404(Proveedor, id=pk)
        delete_it.delete()
        messages.success(request, "Proveedor eliminado correctamente...")
        return redirect('proveedores')
    else:
        messages.success(request, "Tiene que acceder primero con Login...")
        return redirect('index')

def add_proveedor(request):
    form = AddProveedorForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Proveedor agregado correctamente...")
                return redirect('proveedores')
        return render(request, 'add_proveedor.html', {'form':form})
    else:
        messages.success(request, "Tiene que acceder primero con Login...")
        return redirect('index')

def update_proveedor(request, pk):
    if request.user.is_authenticated:
        proveedor_actual = get_object_or_404(Proveedor, id=pk)
        form = AddProveedorForm(request.POST or None, instance=proveedor_actual)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente...")
            return redirect('proveedor', pk=proveedor_actual.id)
        return render(request, 'update_proveedor.html', {'form': form})
    else:
        messages.success(request, "Tiene que acceder primero con Login...")
        return redirect('index')


def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            tipo = form.cleaned_data['tipo']

            try:
                df = pd.read_excel(archivo)

                if tipo == 'proveedor':
                    Proveedor.insertar_proveedores(df)
                elif tipo == 'flete':
                    TipoFlete.insertar_fletes_desde_excel(archivo)
                elif tipo == 'transporte':
                    Transporte.insertar_transportes_desde_excel(archivo)

                return render(request, 'upload_success.html', {'tipo': tipo})

            except Exception as e:
                logger.error(f"Error al procesar el archivo: {e}")
                return render(request, 'upload_excel.html', {
                    'form': form,
                    'error': f"Error al procesar el archivo: {e}"
                })

    else:
        form = ExcelUploadForm()

    return render(request, 'upload_excel.html', {'form': form})
