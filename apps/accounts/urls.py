from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('usuarios/', views.lista, name='lista'),
    path('usuarios/nuevo/', views.crear, name='crear'),
    path('usuarios/<int:pk>/editar/', views.editar, name='editar'),
    path('perfil/', views.perfil, name='perfil'),
]
