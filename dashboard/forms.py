from django import forms
from .models import Sugerencia

class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['tipo', 'mensaje']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Cuéntanos tu idea o el problema que encontraste...'
            }),
        }