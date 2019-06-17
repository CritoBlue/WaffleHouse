from django.contrib import admin
from .models import WaffleIndex, IndexActual, Cliente, Producto, Pedido, Trabajador, Horario

# Register your models here.
admin.site.register(WaffleIndex)
admin.site.register(IndexActual)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Trabajador)
admin.site.register(Horario)