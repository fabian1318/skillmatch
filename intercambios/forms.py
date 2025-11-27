from django import forms
from .models import Resena, Reporte

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['estrellas', 'comentario']
        widgets = {
            'estrellas': forms.Select(attrs={'class': 'form-select'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '¿Qué tal fue la experiencia?'}),
        }

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['motivo', 'descripcion']
        widgets = {
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }