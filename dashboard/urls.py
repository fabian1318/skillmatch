from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.enviar_sugerencia, name='enviar_sugerencia'),
]