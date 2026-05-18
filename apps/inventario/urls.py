from django.urls import path
from . import views
app_name='inventario'
urlpatterns=[path('',views.lista,name='lista'),path('nuevo/',views.crear,name='crear'),path('<int:pk>/',views.detalle,name='detalle'),path('<int:pk>/editar/',views.editar,name='editar'),path('movimiento/',views.movimiento,name='movimiento'),path('proveedores/',views.proveedores,name='proveedores'),path('proveedores/nuevo/',views.crear_proveedor,name='crear_proveedor')]
