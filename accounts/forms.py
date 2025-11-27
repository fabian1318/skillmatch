from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'carrera')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(forms.ModelForm):
    # NOTA: Hemos eliminado el campo 'nuevas_habilidades' para restringir la creación libre.

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'carrera', 'biografia', 'habilidades_ofrecidas', 'habilidades_buscadas']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'habilidades_ofrecidas': forms.CheckboxSelectMultiple(),
            'habilidades_buscadas': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_fields = ['first_name', 'last_name', 'carrera']
        for field in text_fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})