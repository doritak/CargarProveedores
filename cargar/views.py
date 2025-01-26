from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Proveedor

# Create your views here.
def home(request):
    proveedores = Proveedor.objects.all()

    # validar si el usuario está loggeado (login)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Autentificarse
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenido, has ingresado correctamente..")
            return redirect('home')
        else:
            messages.success(request, "Hay un error en el ingreso.. ")
            return redirect('home')

    return render(request, 'home.html', {'proveedores':proveedores})

# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request, "Hasta luego, has salido de con Logout.. ")
    return redirect('home')

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
            return redirect('home',{'user':username})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form': form})

def proveedor_record(request, pk):
    if request.user.is_authenticated:
        proveedor_record = Proveedor.objects.get(id=pk)
        return render(request, 'record.html', {'proveedor_record': proveedor_record})
    else:
        messages.success(request, "Tiene que acceder primero con Login...")
        return redirect('home')
