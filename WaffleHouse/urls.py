from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro', views.registro, name='registro'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('horario', views.verhorario, name='verhorario'),
    path('producto', views.verstock, name='verstock'),
    path('producto/añadir', views.StockCreate.as_view(), name='add_stock'),
    path('producto/<pk>/modificar', views.StockUpdate.as_view(), name='edit_stock'),
    path('producto/<pk>/eliminar', views.delete_stock, name='delete_stock'),
    path('waffle_index', views.cambiar_index, name='cambiar_index'),
]