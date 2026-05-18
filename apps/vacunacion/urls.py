from django.urls import path
from . import views
app_name='vacunacion'
urlpatterns=[path('',views.lista,name='lista'),path('nuevo/',views.crear,name='crear'),path('<int:pk>/',views.detalle,name='detalle'),path('<int:pk>/editar/',views.editar,name='editar'),path('vacunas/',views.lista_vacunas,name='vacunas'),path('vacunas/nuevo/',views.crear_vacuna,name='crear_vacuna')]
