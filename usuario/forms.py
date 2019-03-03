from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class UserForm(UserCreationForm):

	no_empleado = forms.CharField(max_length = 40, help_text = 'opcional')
	rfc = forms.CharField(max_length = 15)
	edad = forms.IntegerField()
	puesto = forms.CharField(max_length = 200)
	telefono = forms.CharField(max_length = 10)

	class Meta:
		model = User
		fields = ('username','is_superuser', 'first_name', 'last_name', 'no_empleado', 'rfc', 'edad', 'puesto', 'telefono', 'password1', 'password2')
    