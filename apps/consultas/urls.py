from django.urls import path
from . import views
app_name='consultas'
urlpatterns=[
    path('',views.lista,name='lista'),
    path('nuevo/',views.crear,name='crear'),
    path('desde-cita/<int:pk>/',views.nueva_desde_cita,name='nueva_cita'),
    path('<int:pk>/',views.detalle,name='detalle'),
    path('<int:pk>/editar/',views.editar,name='editar'),
    path('<int:pk>/nota/',views.agregar_nota,name='nota'),
    path('<int:pk>/prescripcion/',views.agregar_prescripcion,name='prescripcion'),
    path('<int:pk>/imprimir/',views.imprimir,name='imprimir'),
]
