from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro', views.registro, name='registro'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('verhorario', views.verhorario, name='verhorario'),
]