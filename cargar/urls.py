from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('proveedor/<int:pk>', views.proveedor_record, name='proveedor'),
    path('delete_proveedor/<int:pk>', views.delete_proveedor, name='delete_proveedor'),
    path('add_proveedor/', views.add_proveedor, name='add_proveedor'),
]