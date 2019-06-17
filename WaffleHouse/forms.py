from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Trabajador

User = get_user_model()

class UserForm(forms.ModelForm):
	username = forms.CharField(label='RUT', max_length=10,required=True)
	email = forms.EmailField(label='Email', required=True)
	password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput, required=True)
	password2 = forms.CharField(label='Confirme Contraseña', widget=forms.PasswordInput, required=True)
	first_name = forms.CharField(label='Nombres', max_length=50, required=True)
	last_name = forms.CharField(label='Apellidos', max_length=50, required=True)

	class Meta:
		model = User
		fields = (
			'username', 
			'email', 
			'first_name', 
			'last_name', 
			'password1', 
			'password2')
	
	def clean_password(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		if password1 != password2:
			raise forms.ValidationError("Las contraseñas no coinciden")
		return password1

	def save(self, commit=True):
	 	user = super().save(commit=False)

	 	user.username = self.cleaned_data['username']
	 	user.email = self.cleaned_data['email']
	 	user.first_name = self.cleaned_data['first_name']
	 	user.last_name = self.cleaned_data['last_name']
	 	password = self.clean_password()
	 	user.set_password(password)

	 	if commit:
	 		user.save()

	 	return user

class TrabajadorForm (forms.ModelForm):
	administrador = forms.BooleanField(label='¿Es Administrador?', widget=forms.HiddenInput)

	class Meta:
		model = Trabajador
		fields = ('salario', 'administrador')

	def save(self, commit=True):
	 	trabajador = super().save(commit=False)
	 	trabajador.user = User.objects.latest('date_joined')
	 	
	 	if administrador:
	 		trabajador.user.is_staff = True
	 		trabajador.user.is_superuser = True

	 	if commit:
	 		trabajador.save()

	 	return trabajador

class LoginForm (forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("El usuario no existe")
			if not user.check_password(password):
				raise forms.ValidationError("Nombre de usuario o contraseña son incorrectos")
			if not user.is_active:
				raise forms.ValidationError("El usuario no está activo")
		return super(LoginForm, self).clean(*args, **kwargs)
