from django.db import models
from django.contrib.auth.models import User

class WaffleIndex (models.Model):
	nombre = models.CharField(max_length = 20)
	def __str__(self):
		return self.nombre
	class Meta:
		verbose_name_plural = 'WaffleIndexes'

class IndexActual (models.Model):
	actual = models.ForeignKey(WaffleIndex, on_delete = models.CASCADE)
	actualizado = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		index = self.actual.nombre
		return index
	class Meta:
		verbose_name_plural = 'IndexActual'

class Cliente (models.Model):
	nombre = models.CharField(max_length = 100)
	rut = models.CharField(max_length = 10)
	email = models.EmailField(max_length = 255)
	def __str__(self):
		return self.nombre

class Producto (models.Model):
	descripcion = models.CharField(max_length = 255)
	stock = models.IntegerField()
	precio = models.PositiveIntegerField()
	ultimaReposicion = models.DateTimeField('Última Reposición')
	def __str__(self):
		return self.descripcion

class Pedido (models.Model):
	cliente = models.ManyToManyField(Cliente)
	producto = models.ManyToManyField(Producto)
	cantidad = models.PositiveIntegerField()
	valorTotal = models.PositiveIntegerField()
	fecha = models.DateTimeField(auto_now_add = True)
	def __str__(self):
		return 'Pedido '+ self.id

class Trabajador(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	salario = models.PositiveIntegerField(default=0)
	administrador = models.BooleanField(default=False)

	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name

	class Meta:
		verbose_name_plural = 'Trabajadores'

class Horario (models.Model):
	trabajador = models.OneToOneField(Trabajador, on_delete = models.CASCADE)
	horaEntrada = models.CharField(max_length=5)
	horaSalida = models.CharField(max_length=5)
	diasTrabaja = models.CharField(max_length=20)
	def __str__(self):
		return 'Horario de ' + self.trabajador.user.first_name + ' ' + self.trabajador.user.last_name