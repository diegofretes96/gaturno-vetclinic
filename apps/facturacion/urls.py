from django.urls import path
from . import views
app_name='facturacion'
urlpatterns=[path('',views.lista,name='lista'),path('nuevo/',views.crear,name='crear'),path('<int:pk>/',views.detalle,name='detalle'),path('<int:pk>/editar/',views.editar,name='editar'),path('<int:pk>/item/',views.agregar_item,name='agregar_item'),path('<int:pk>/item/<int:item_pk>/eliminar/',views.eliminar_item,name='eliminar_item'),path('<int:pk>/cobrar/',views.cobrar,name='cobrar'),path('<int:pk>/imprimir/',views.imprimir,name='imprimir')]
