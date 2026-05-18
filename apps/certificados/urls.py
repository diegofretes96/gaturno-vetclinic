from django.urls import path
from . import views
app_name='certificados'
urlpatterns=[path('',views.lista,name='lista'),path('nuevo/',views.crear,name='crear'),path('<int:pk>/',views.detalle,name='detalle'),path('<int:pk>/imprimir/',views.imprimir,name='imprimir')]
