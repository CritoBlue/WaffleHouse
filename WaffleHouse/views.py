from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import  reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User as Auth_User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.generic.edit import CreateView, UpdateView
from .forms import TrabajadorForm, LoginForm, IndexForm, ProductoForm
from .models import IndexActual, Trabajador, Horario, Producto, Pedido

def index(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	context = { "waffleindex" : waffleindex.actual.nombre }
	return render(request, "index.html", context)

@login_required(login_url='login')
def verhorario(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	username = request.user.username
	userobj = Auth_User.objects.get(username=username)
	trabuser = Trabajador.objects.get(user=userobj)

	try:
		qs_horario = Horario.objects.get(trabajador=trabuser)
	except Horario.DoesNotExist:
		qs_horario = None
	
	context = { 
		"waffleindex" : waffleindex.actual.nombre,
		"listahorario" : qs_horario
	}

	return render(request, "horario.html", context)

@user_passes_test(lambda u: u.is_superuser)
def registro(request):
	trabajaform = TrabajadorForm()

	if request.method == 'POST':
		trabajaform = TrabajadorForm(request.POST)
		if trabajaform.is_valid():
			trabajaform.save(commit=True)
			user = Auth_User.objects.latest('date_joined')
			salary = trabajaform.cleaned_data['salario']
			worker = Trabajador(user=user, salario=salary)
			worker.save()
			trabajaform = TrabajadorForm()
		else:
			print(trabajaform.errors)

	waffleindex = IndexActual.objects.latest('actualizado')

	context = {
		"form" : trabajaform,
		"waffleindex" : waffleindex.actual.nombre
	}
	
	return render(request, "registro.html", context)

@user_passes_test(lambda u: u.is_superuser)
def cambiar_index(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	form = IndexForm()
	if request.method == 'POST':
		form = IndexForm(request.POST)
		if form.is_valid():
			nuevo = form.cleaned_data['actual']
			indexobj = IndexActual(actual=nuevo)
			indexobj.save()
			form = IndexForm()
			return redirect('index')
		else:
			print(form.errors)

	context = { 
		"waffleindex" : waffleindex.actual.nombre,
		"form" : form
	}
	return render(request, "cambiar_index.html", context)

@login_required(login_url='login')
def verstock(request):
	waffleindex = IndexActual.objects.latest('actualizado')
	qs_producto = Producto.objects.all()

	context = { 
		"waffleindex" : waffleindex.actual.nombre,
		"productos" : qs_producto
	}

	return render(request, "stock.html", context)

class StockCreate(CreateView):
	model = Producto
	fields = ['descripcion', 'stock', 'precio']
	template_name = 'stock_add.html'
	success_url = reverse_lazy('verstock')

	def get_context_data(self, **kwargs):
		context = super(StockCreate, self).get_context_data(**kwargs)
		waffleindex = IndexActual.objects.latest('actualizado')
		context['waffleindex'] = waffleindex.actual.nombre
		return context

class StockUpdate(UpdateView):
	model = Producto
	fields = ['descripcion', 'stock', 'precio']
	template_name = 'stock_edit.html'
	success_url = reverse_lazy('verstock')
	pk_url_kwarg = 'pk'

	def get_context_data(self, **kwargs):
		context = super(StockUpdate, self).get_context_data(**kwargs)
		waffleindex = IndexActual.objects.latest('actualizado')
		context['waffleindex'] = waffleindex.actual.nombre
		return context

	def get_object(self, queryset=None):
		queryset = Producto.objects.all()
		pk = self.kwargs.get(self.pk_url_kwarg)
		if pk is not None:
			queryset = queryset.filter(pk=pk)
		obj = queryset.get()
		return obj

def delete_stock(request, pk):
	Producto.objects.filter(id=pk).delete()
	return redirect('verstock')

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