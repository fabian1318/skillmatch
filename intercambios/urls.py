from django.urls import path
from . import views

urlpatterns = [
    path('solicitar/<int:receptor_id>/<int:habilidad_id>/', views.iniciar_solicitud, name='iniciar_solicitud'),
    path('mis-intercambios/', views.listar_intercambios, name='listar_intercambios'),
    path('responder/<int:intercambio_id>/<str:accion>/', views.responder_solicitud, name='responder_solicitud'),
    path('iniciar/<int:intercambio_id>/', views.iniciar_intercambio, name='iniciar_intercambio'),
    path('finalizar/<int:intercambio_id>/', views.finalizar_intercambio, name='finalizar_intercambio'),
    path('calificar/<int:intercambio_id>/', views.calificar_intercambio, name='calificar_intercambio'),
    path('reportar/<int:usuario_id>/', views.reportar_usuario, name='reportar_usuario'),
]