from django.urls import path
from . import views
app_name='agenda'
urlpatterns=[
    path('',views.lista,name='lista'),
    path('nuevo/',views.crear,name='crear'),
    path('<int:pk>/editar/',views.editar,name='editar'),
    path('<int:pk>/cancelar/',views.cancelar,name='cancelar'),
    path('calendario/',views.calendario,name='calendario'),
    path('json/',views.citas_json,name='citas_json'),
    path('sala-espera/',views.sala_espera,name='sala_espera'),
    path('sala-espera/agregar/',views.agregar_sala,name='agregar_sala'),
    path('sala-espera/<int:pk>/atender/',views.atender,name='atender'),
    path('sala-espera/count/',views.sala_count,name='sala_count'),
]
