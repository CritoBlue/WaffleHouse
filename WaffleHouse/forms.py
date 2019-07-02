from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Trabajador, Producto, WaffleIndex, IndexActual

class UserForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = User
		fields = (
			'username', 
			'email',
			'first_name', 
			'last_name',)

class TrabajadorForm (UserForm):
	salario = forms.IntegerField(label='Salario', required=True)
	class Meta(UserForm.Meta):
		fields = UserForm.Meta.fields + ('salario',)

	def save(self, commit=True):
		trabajador = super().save(commit=False)
		trabajador.user = User.objects.latest('date_joined')
		
		if trabajador.user.is_staff and trabajador.user.is_superuser:
			trabajador.administrador = True

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


class ProductoForm (forms.ModelForm):
	class Meta:
		model = Producto
		fields = {
			'descripcion',
			'stock',
			'precio',
		}

class IndexForm (forms.ModelForm):
	actual = forms.ModelChoiceField(queryset=WaffleIndex.objects.all(), empty_label="Seleccione...")

	class Meta:
		model = IndexActual
		fields = {
			'actual',
		}