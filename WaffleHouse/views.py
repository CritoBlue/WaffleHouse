from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User as Auth_User
from .forms import UserForm, TrabajadorForm, LoginForm
from .models import IndexActual, Trabajador, Horario
from django.contrib.auth.decorators import user_passes_test, login_required

def index(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	context = { "waffleindex" : waffleindex.actual.nombre}
	return render(request, "index.html", context)

@login_required
def verhorario(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	if request.user.is_authenticated:
		username = request.user.username
	userobj = Auth_User.objects.get(username=username)
	trabuser = Trabajador.objects.get(user=userobj)
	try:
		query_set = Horario.objects.get(trabajador=trabuser)
	except Horario.DoesNotExist:
		query_set = None
	
	context = { 
		"waffleindex" : waffleindex.actual.nombre,
		"listahorario" : query_set
	}
	return render(request, "horario.html", context)

@user_passes_test(lambda u: u.is_superuser)
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