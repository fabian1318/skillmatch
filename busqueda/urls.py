from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar, name='buscar'),
    path('usuario/<int:user_id>/', views.perfil_publico, name='perfil_publico'),
]