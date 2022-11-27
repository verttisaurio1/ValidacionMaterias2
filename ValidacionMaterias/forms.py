from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from .models import Usuario


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ('email',"idDocente",'NombreDocente','ApellidoPat','ApellidoMat','Cargo',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = ('email','idDocente','NombreDocente','ApellidoPat','ApellidoMat','Cargo',)