from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_notificaciones, name='listar_notificaciones'),
    path('marcar/<int:notificacion_id>/', views.marcar_como_leida, name='marcar_como_leida'),
]