from django.urls import path
from . import views
app_name='farmacia'
urlpatterns=[path('',views.lista,name='lista'),path('nuevo/',views.crear,name='crear'),path('<int:pk>/',views.detalle,name='detalle'),path('<int:pk>/item/',views.agregar_item,name='agregar_item'),path('<int:pk>/despachar/',views.despachar,name='despachar')]
