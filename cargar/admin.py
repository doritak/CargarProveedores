from django.contrib import admin
from cargar.models import Proveedor, TipoFlete, Transporte

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(TipoFlete)
admin.site.register(Transporte)
