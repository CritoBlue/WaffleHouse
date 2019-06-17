from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User as Auth_User
from .forms import UserForm, TrabajadorForm, LoginForm
from .models import IndexActual, Trabajador

def index(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	context = { "waffleindex" : waffleindex.actual.nombre}
	return render(request, "index.html", context)

def verhorario(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	context = { "waffleindex" : waffleindex.actual.nombre}
	return render(request, "horario.html", context)

def registro(request):
	next = request.GET.get('next')
	userform = UserForm(request.POST or None)
	trabajaform = TrabajadorForm(request.POST or None)
	if userform.is_valid() and trabajaform.is_valid():
		user = userform.save()
		trabajador = trabajaform.save(commit=False)
		trabajador.user = user
		trabajador.save()
		login(request, user)
		if next:
			return redirect(next)
	else:
		userform = UserForm()
		trabajaform = TrabajadorForm()

	waffleindex = IndexActual.objects.latest('actualizado')
	context = {
		"form" : UserForm(),
		"form2" : TrabajadorForm(),
		"waffleindex" : waffleindex.actual.nombre
	}
	return render(request, "registro.html", context)

def login_view(request):
	next = request.GET.get('next')
	form = LoginForm(request.POST or None)
	waffleindex = IndexActual.objects.latest('actualizado')
	context = { "waffleindex" : waffleindex.actual.nombre, "form" : form }

	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect('index')

	return render(request, "login.html", context)

def logout_view(request):
	logout(request)
	return redirect('index')